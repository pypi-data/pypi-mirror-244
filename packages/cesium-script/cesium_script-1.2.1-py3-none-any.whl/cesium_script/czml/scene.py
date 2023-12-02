import itertools
import logging
import uuid

import spiceypy as sp
from czml3 import Document, Packet, Preamble
from czml3.enums import (
    HorizontalOrigins,
    InterpolationAlgorithms,
    LabelStyles,
    ReferenceFrames,
    VerticalOrigins,
)
from czml3.properties import (
    Billboard,
    Color,
    Label,
    Material,
    Model,
    Orientation,
    Path,
    Polyline,
    PolylineMaterial,
    Position,
    PositionList,
    SolidColorMaterial,
)

from .sensor import custom, rectangular
from .util import (
    generate_cartesians,
    generate_html_table,
    generate_unit_quaternion,
    get_body_data,
    get_cartograhic_radians,
    get_illumination,
    get_n_colors,
    get_positions,
    get_quaternions,
    sizeof_fmt,
)

juice_desc = "here a description"
seconds_in_hour = 3600
czml_fixed_size = 17351
czml_step_size = 1880
# Empiric value
czml_max_recommended = 1e7


def get_max_number_of_steps():
    """
    Returns:
        number_of_steps (int): Maximun number of step for a safe CZML
    """
    return (czml_max_recommended - czml_fixed_size) / czml_step_size


def get_czml_expected_size(nsteps):
    """Returns the expected size of the file in bytes

    Args:
        nsteps (int): number of steps

    Returns:
        size (int): Expected size of the file in bytes
    """
    return czml_fixed_size + czml_step_size * nsteps


def get_step_number(start, end, step_size):
    """Return the required number of steps to cover the period

    Args:
        start (float): ephemeris start time
        end (float): ephemeris end time
        step_size (int): step size in seconds
    Returns:
        steps (int): Number of steps
    """
    return int((end - start) / step_size)


def get_step_size(start, end, step_number):
    """Return the step size to cover the period with step_number

    Args:
        start (float): ephemeris start time
        end (float): ephemeris end time
        steps (int): number of steps
    Returns:
        step_size (int): step size in seconds
    """
    return int((end - start) / step_number)


def get_recommended_step_size(start, end):
    """Return the step size to cover the period with a size safe CZML
    Args:
        start (float): ephemeris start time
        end (float): ephemeris end time

    Returns:
        step_size (int): step size in seconds
    """
    recommended = get_step_size(start, end, get_max_number_of_steps())
    return recommended if recommended else 1


def generate_solar_panel(ets, saa_id="JUICE_SA+Y", sa_base_id="JUICE_SA+Y_ZERO"):
    """Generates for a list of ephemeris times the solar panel position as a rotations along  Y-Axis

    Args:
        ets (list float): List of spice ephemeris time
        saa_id (str, optional): The solar panel SPICE frame name. Defaults to 'JUICE_SA+Y'.
        sa_base_id (str, optional): The base (0 rotation) solar panel SPICE frame name. Defaults to 'JUICE_SA+Y_ZERO'.

    Returns:
        rotation (list float): A list of rotations in degrees
    """
    numbers = []
    for et in ets:
        mx = sp.pxform(sa_base_id, saa_id, et)
        rad_x, rad_y, rad_z = sp.m2eul(mx, 3, 2, 1)
        numbers.append(f"{sp.et2utc(et, 'ISOC', 0)}Z")
        numbers.append(rad_y * sp.dpr() * 10)
    return numbers


def generate_articulations(ets):
    """Generates the CZML articulations that model the JUICE solar panels behaviour for a
    a list of dates

    Args:
        ets (list float): List of spice ephemeris time

    Returns:
        articulation (object): CZML object with
    """

    articulations = {}

    articulations["SolarPanelPy PanelRotation"] = {
        "epoch": f"{sp.et2utc(ets[0], 'ISOC', 0)}Z",
        "number": generate_solar_panel(ets),
    }

    articulations["SolarPanelMy PanelRotation"] = {
        "epoch": f"{sp.et2utc(ets[0], 'ISOC', 0)}Z",
        "number": generate_solar_panel(ets, "JUICE_SA-Y", "JUICE_SA-Y_ZERO"),
    }

    return articulations


def get_track_features(sc, body, positions, ets, start_utc, end_utc, radius, step):
    """Creates a CZML the contextual information of the S/C (position and attitude) including:
        3D visualization
        ground-track information
        Sun illumination
    in CZML format suitable for its visualizacion in the JUICE SOC cesium tool

    Args:
        mk_path (str): path to the metakernel
        start_utc (str): scene start using UTC scale and ISO format (e.g. 2032-07-02T14:22:25Z)
        end_utc (str): scene end using UTC scale and ISO format (e.g. 2032-07-02T14:22:25Z)
        step (int): step used for scene calculations
        body (str): Orbiting body

    Returns:
        filename (str): the path of the CZML file
    """
    track_features = []
    palette_size = 12
    colors = get_n_colors(palette_size)
    pvec = None
    for index in range(0, len(positions) - 1):
        dist = sp.vnorm(positions[index])
        alt = dist - radius
        phase, incdnc, emiss, svec = get_illumination(
            ets[index], sc, body, positions[index]
        )
        if index == 0:
            pvec = svec
        else:
            gt_velocity = sp.vsep(svec, pvec) * radius / step
            pvec = svec
            track_features.append(
                Packet(
                    id=f"ground_track_{index}",
                    name=f"ground_track_{index}",
                    availability=f"{start_utc}/{end_utc}",
                    polyline=Polyline(
                        width=3,
                        positions=PositionList(
                            cartographicRadians=list(
                                itertools.chain(
                                    *get_cartograhic_radians(
                                        body, positions[index : index + 2]
                                    )
                                )
                            )
                        ),
                        material=PolylineMaterial(
                            solidColor=SolidColorMaterial.from_list(
                                colors[index % palette_size]
                            )
                        ),
                        clampToGround=True,
                    ),
                    properties={
                        "groundtrack": {"boolean": True},
                        "distance": {"number": dist},
                        "altitude": {"number": alt},
                        "gt_velocity": {"number": gt_velocity},
                        "emission": {"number": emiss * sp.dpr()},
                        "phase": {"number": phase * sp.dpr()},
                        "incidence": {"number": incdnc * sp.dpr()},
                    },
                    description=generate_html_table(
                        {
                            "Epoch": sp.et2utc(ets[index], "ISOC", 0),
                            "Distance (km)": f"{dist:.2f}",
                            "Altitude (km)": f"{alt:.2f}",
                            "Groundtrak velocity (km/s)": f"{gt_velocity:.2f}",
                            "Phase Angle (deg)": f"{phase  * sp.dpr() :.2f}",
                            "Emission Angle (deg)": f"{emiss  * sp.dpr() :.2f}",
                            "Incidence Angle (deg)": f"{incdnc  * sp.dpr() :.2f}",
                        }
                    ),
                )
            )
    return track_features


def check_date_format(utc_user):
    utc = utc_user
    if utc[-1] != "Z":
        utc += "Z"
        message = f"The date must be time zoned. Automatic conversion to Z zone. {utc}"
        logging.warning(message)
    return utc


def generate_czml(start_utc_user, end_utc_user, step_size, body="ganymede"):
    """Creates the contextual information of the S/C (position and attitude) including:
    3D visualization
    ground-track information
    Sun illumination
    in CZML format suitable for its visualizacion in the JUICE SOC cesium tool

    Args:
        start_utc (str): scene start using UTC scale and ISO format (e.g. 2032-07-02T14:22:25Z)
        end_utc (str): scene end using UTC scale and ISO format (e.g. 2032-07-02T14:22:25Z)
        step_size (int): step size in seconds used for scene calculations
        body (str): Orbiting body

    Returns:
        filename (str): the path of the CZML file
    """
    start_utc = check_date_format(start_utc_user)
    end_utc = check_date_format(end_utc_user)

    et_start = sp.utc2et(start_utc[:-1])
    et_end = sp.utc2et(end_utc[:-1])
    suggested_step_size = get_recommended_step_size(et_start, et_end)
    if step_size is None:
        message = f"Using recommended step {suggested_step_size} seconds"
        logging.info(message)
        print(message)
        step_size = suggested_step_size

    num_steps = get_step_number(et_start, et_end, step_size)
    message = f"Number of steps: {num_steps}; Step size: {step_size} seconds"
    logging.info(message)
    expected_czml_size = get_czml_expected_size(num_steps)
    message = f"Expected size of file {sizeof_fmt(expected_czml_size)}"
    logging.info(message)

    if expected_czml_size > 1.5 * czml_max_recommended:
        message = f"File size bigger than the recommended one. Consider using a step size of {suggested_step_size} s "
        logging.warning(message)

    et_start = sp.utc2et(start_utc[:-1])
    ets = [et_start + delta for delta in range(0, num_steps * step_size, step_size)]
    juice_positions = get_positions(ets, "JUICE", body)
    juice_quaternions = get_quaternions(ets, "JUICE_SPACECRAFT", "IAU_" + body)
    sun_positions = get_positions(ets, "SUN", body)
    radius, f = get_body_data(body)

    end_utc = sp.et2utc(ets[-1], "ISOC", 0) + "Z"

    juice_id = str(uuid.uuid1())

    clock = {
        "interval": f"{start_utc}/{end_utc}",
        "currentTime": start_utc,
        "multiplier": 20,
        "range": "LOOP_STOP",
        "step": "SYSTEM_CLOCK_MULTIPLIER",
    }

    doc = Document(
        [
            Preamble(clock=clock),
            Packet(
                id=juice_id,
                name="JUICE",
                description="Juice Spacecraft",
                availability=f"{start_utc}/{end_utc}",
                properties={"spacecraft": {"string": "JUICE"}},
                path=Path(
                    width=0.5,
                    leadTime=20.0 if body.lower() == "jupiter" else None,
                    trailTime=20.0 if body.lower() == "jupiter" else None,
                    material=Material(
                        solidColor=SolidColorMaterial.from_list([255, 255, 255])
                    ),
                    show=False,
                ),
                label=Label(
                    text="JUICE_SC",
                    show=False,
                    fillColor=Color.from_list([0, 255, 0]),
                    outlineColor=Color.from_list([0, 0, 0]),
                    horizontalOrigin=HorizontalOrigins.LEFT,
                    font="11pt Lucida Console",
                    style=LabelStyles.FILL_AND_OUTLINE,
                    outlineWidth=2,
                    verticalOrigin=VerticalOrigins.CENTER,
                ),
                billboard=Billboard(
                    image="data:image/png;base64,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",
                    scale=1,
                    show=False,
                ),
                model=Model(
                    show=True,
                    gltf="/assets/models/juice_low_resolution_v06.glb",
                    minimumPixelSize=128,
                ),
                position=Position(
                    interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
                    interpolationDegree=5,
                    referenceFrame=ReferenceFrames.FIXED,
                    epoch=start_utc,
                    cartesian=generate_cartesians(juice_positions, step_size),
                ),
                orientation=Orientation(
                    interpolationAlgorithm=InterpolationAlgorithms.LINEAR,
                    interpolationDegree=1,
                    epoch=start_utc,
                    unitQuaternion=generate_unit_quaternion(
                        juice_quaternions, step_size
                    ),
                ),
            ),
            Packet(
                id="sun",
                name="SUN",
                availability=f"{start_utc}/{end_utc}",
                position=Position(
                    interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
                    interpolationDegree=5,
                    referenceFrame=ReferenceFrames.FIXED,
                    epoch=start_utc,
                    cartesian=generate_cartesians(sun_positions, step_size),
                ),
            ),
            rectangular(
                parent=juice_id,
                name="janus",
                color=[0, 0, 255, 34],
                start_utc=start_utc,
                end_utc=end_utc,
                x_half_angle=0.011257373675363,
                y_half_angle=0.015001,
            ),
            rectangular(
                parent=juice_id,
                name="navcam-1",
                color=[255, 0, 0, 34],
                start_utc=start_utc,
                end_utc=end_utc,
                x_half_angle=0.035,
                y_half_angle=0.035,
            ),
            rectangular(
                parent=juice_id,
                name="navcam-2",
                color=[255, 0, 0, 34],
                start_utc=start_utc,
                end_utc=end_utc,
                x_half_angle=0.035,
                y_half_angle=0.035,
            ),
            rectangular(
                parent=juice_id,
                name="jmc-1",
                color=[230, 230, 250, 34],
                start_utc=start_utc,
                end_utc=end_utc,
                x_half_angle=23.25 * sp.rpd(),
                y_half_angle=23.25 * sp.rpd(),
            ),
            rectangular(
                parent=juice_id,
                name="jmc-2",
                color=[230, 230, 250, 34],
                start_utc=start_utc,
                end_utc=end_utc,
                x_half_angle=23.25 * sp.rpd(),
                y_half_angle=23.25 * sp.rpd(),
            ),
            custom(
                parent=juice_id,
                name="uvs",
                color=[0, 127, 0, 34],
                start_utc=start_utc,
                end_utc=end_utc,
                cartesian_list=[
                    -0.0654031044274081,
                    0.0008708943631663,
                    0.997858544821993,
                    -0.0654031044274081,
                    -0.0008708943631663,
                    0.997858544821993,
                    0.0619195296276383,
                    -0.0008708943631663,
                    0.998080764965291,
                    0.0619194588007405,
                    -0.0017453257076200,
                    0.998079623306677,
                    0.0654030296158094,
                    -0.0017453257076200,
                    0.997857403417567,
                    0.0654030296158094,
                    0.0017453257076200,
                    0.997857403417567,
                    0.0619194588007405,
                    0.0017453257076200,
                    0.998079623306677,
                    0.0619195296276383,
                    0.0008708943631663,
                    0.998080764965291,
                ],
            ),
            *get_track_features(
                "juice",
                body,
                juice_positions,
                ets,
                start_utc,
                end_utc,
                radius,
                step_size,
            ),
        ]
    )
    logging.info("CZML generated")
    return doc
