import logging
import math

import geojson
import spiceypy as sp
from geojson import Feature, FeatureCollection
from planetary_coverage import TourConfig
from planetary_coverage.trajectory.fovs import FovsCollection
from shapely import LineString, Polygon
from shapely.ops import split, transform, unary_union

from cesium_script.util.decorator import timer_func


def create_configuration(kernels, body):
    """Creates a TourConfig object describing the JUICE trajectory around the
    body using the SPICE kernel set.

    Args:
        kernels (list of str): List of kernel paths
        body (str): Name of the body.

    Returns:
        configuration (TourConfig): The TourConfig object describing the JUICE
        trajectory around the body derived from
    """
    config = TourConfig(spacecraft="JUICE", target=body, kernels=kernels)
    return config


# @timer_func
def process_observation(config, start, end, fov, rate, base=5):
    """
    Creates a list of geojson features containing the geometry of the footprints
    of an instrument observation.

    Args:
        config (TourConfig): _description_
        start (str): Observation start
        end (str): Observation end
        fov (str): Field of view used by the instrument
        rate (int): If rate present and its value is -1, the meaning is to get
                    a single feature for the whole period.
                    If rate present and its value is 0, the meaning is to get
                    a feature corresponding to a single exposure at start time
                    If rate present and its value > 0, the meaning is to get
                    several features corresponding to the merge of exposures
                    along rate seconds. The number of features will be the
                    duration in seconds divide by rate.
        base (int): Defines the sample step used for the shape calculations, the
                    default is 5 seconds that is the recommended for on-the-fly
                    representations as its value affects linearly to the
                    performance time!

    Returns:
        features (list of geojson.Feature): lists of features
    """
    logging.info(f"Processing {start} {end} {fov} - base step: {base} seconds")
    inst_traj = config[start:end:f"{base} sec"].new_traj(instrument=fov)
    return __get_features(inst_traj, rate / base, base)


@timer_func
def __avoid_nan(number):
    return -1 if math.isnan(number) else number


@timer_func
def __get_sample(inst_traj, obs_index):
    """Gets the geometric properties of a certain sample

    Args:
        inst_traj (InstrumentTrajectory): Instrument trajectory object
        obs_index (int): The sample index

    Returns:
        properties (dict): The geometric properties
    """
    properties = {}
    properties.setdefault("utc", sp.et2utc(inst_traj.ets[obs_index], "ISOC", 0))
    properties.setdefault("Phase Angle (deg)", __avoid_nan(inst_traj.phase[obs_index]))
    properties.setdefault(
        "Incidence Angle (deg)", __avoid_nan(inst_traj.inc[obs_index])
    )
    properties.setdefault("Emission Angle (deg)", __avoid_nan(inst_traj.emi[obs_index]))
    properties.setdefault("Altitude (km)", __avoid_nan(inst_traj.slant[obs_index]))
    properties.setdefault(
        "Pixel scale (km/pix)", __avoid_nan(inst_traj.pixel_scale[obs_index])
    )
    properties.setdefault("fov", inst_traj.observer.name)
    properties.setdefault("observation", True)
    properties.setdefault("altitude", __avoid_nan(inst_traj.slant[obs_index]))
    properties.setdefault("emission", __avoid_nan(inst_traj.emi[obs_index]))
    properties.setdefault("phase", __avoid_nan(inst_traj.phase[obs_index]))
    properties.setdefault("incidence", __avoid_nan(inst_traj.inc[obs_index]))
    return properties


def __reset_force():
    return 0, 360, 0


@timer_func
def __polygon_cross_anti_meridian(polygon, delta):
    polygon = transform(
        lambda lon, lat: (lon if lon > 180 else lon + 360, lat), polygon
    )
    meridian = LineString([[360, -90], [360, 90]])
    split_polygons = split(polygon, meridian)
    if len(split_polygons.geoms) == 2:
        left = split_polygons.geoms[0]
        right = split_polygons.geoms[1]
        left = transform(lambda lon, lat: (lon - delta, lat), left)
        right = transform(lambda lon, lat: (lon + delta, lat), right)
        return left, right
    return []


@timer_func
def __get_interception(traj, npts=4):
    fovs = FovsCollection(traj, npts)
    lon = fovs.rlonlat[1]
    lat = fovs.rlonlat[2]
    return lon, lat


@timer_func
def __get_features(inst_traj, rate, base, dump_limit=120):
    """Creates a list of geojson features containing the geometry of the footprints
    of an instrument observation.

    Args:
        inst_traj (InstrumentTrajectory): The object with the instrument trajectory
        rate (int): see process_observation
        base (int): see process_observation
        dump_limit(int): maximum allowed longitude amplitude

    Returns:
        features (list of geojson.Feature): lists of features
    """

    lon, lat = __get_interception(inst_traj)
    n_obs, n_pts = lon.shape
    features = []
    shapely_list = []

    if rate == -1:
        rate = n_obs

    force_dump, minx_group, maxx_group = __reset_force()
    # Traverse all the samples
    for obs_index in range(n_obs):
        if not __skip(obs_index, base, rate):
            polygon = __create_polygon(lon, lat, obs_index, n_pts)
            if polygon.is_valid:
                minx, _, maxx, _ = polygon.bounds
                minx_group = min(minx, minx_group)
                maxx_group = max(maxx, maxx_group)
                dist_x = abs(maxx_group - minx_group)
                shapely_list.append(polygon)
                force_dump = dist_x > dump_limit
            else:
                shapely_list.extend(__polygon_cross_anti_meridian(polygon, 0.001))

        # if rate is 0 a snapshot is generated
        if rate == 0:
            properties = __get_sample(inst_traj, obs_index)
            break

        # Merge and dump the collected snapshots
        if (obs_index != 0 and (obs_index % rate == 0)) or force_dump:
            properties = __get_sample(inst_traj, obs_index)
            __append_feature(features, shapely_list, properties)
            shapely_list = []
            force_dump, minx_group, maxx_group = __reset_force()

    # Append the last bundle
    if len(shapely_list) > 0:
        properties = __get_sample(inst_traj, obs_index)
        __append_feature(features, shapely_list, properties)
    logging.info(f"  Total {len(features)} features")
    return features


def __skip(index, base, rate):
    return rate < 0 and (index % rate) != 0


@timer_func
def __create_polygon(lon, lat, obs_index, n_pts):
    """Creates a shapely.Polygon corresponding to the ring of the projected fov of an
    observation sample.

    Args:
        lon (float [][]): array of the indexed longitude by observation and corner position
        lat (float [][]): array of the indexed latitudes by observation and corner position
        obs_index (int): the observation index
        n_pts (int): number of points of the ring

    Returns:
        polygon (shapely.Polygon): the corresponding polygon to the lon,lat ring
    """
    ring = []
    for point_index in range(n_pts):
        ring.append((lon[obs_index][point_index], lat[obs_index][point_index]))
    return Polygon(ring)


@timer_func
def __append_feature(features, shapely_list, properties):
    """Appends to the feature list passed as input a new feature. The new
    feature has the geometry result the merge of the snapshot polygons
    passed as argument and the input properties.

    Args:
        features (list of geojson.Feature): lists of features
        shapely_list (list of shapely.Polygon): the polygon snapshots merge
        to build-up the geometry of the new feature
        properties (dict): properties associated to the new feature
    """
    if len(shapely_list) > 0:
        union = unary_union(shapely_list)
        union = union.simplify(0.01)
        union = union.normalize()

        snapshot_sh = Feature(geometry=union, properties=properties)
        features.append(snapshot_sh)
        minx, _, maxx, _ = union.bounds
        dist_x = abs(maxx - minx)
        utc = properties.get("utc", "")
        logging.info(
            f"   - {utc} feature with {len(shapely_list):} items (Long. Ext. {dist_x:.2f} deg)"
        )


def dump_file(features, filename):
    """Dumps the list of features in syntax valid GeoJSON file

    Args:
        features (list of geojson.Feature): list of features
        filename (str): filename
    """
    feature_collection = FeatureCollection(features)
    with open(filename, "w") as geojson_file:
        geojson.dump(feature_collection, geojson_file)
