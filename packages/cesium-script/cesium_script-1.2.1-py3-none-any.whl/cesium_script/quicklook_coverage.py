"""The script creates the contextual information of the S/C (position and attitude) including:
    3D visualization
    ground-track information
    Sun illumination
    in CZML format suitable for its visualizacion in the JUICE SOC cesium tool
"""

import argparse
import logging
import sys
from itertools import chain

from spiceypy.utils.exceptions import SpiceyError

from cesium_script.geojson.observations import (
    create_configuration,
    dump_file,
    process_observation,
)
from cesium_script.util.format import clean_utc
from cesium_script.util.observation_csv import read_observation_csvfile


def generate(mk_path, ck_kernels, body, csv_file, split, base):
    """Create a geojson file(s) loadable by a given JUICE Cesium scenario with the features containing
        the geometry of the footprints of an instrument timeline.

    Args:
        mk_path (str): path to the metakernel
        ck_kernels (list of str): list of additional ck kernels
        body (str): Orbiting body
        csv_file (str): path to the csv file
        split (bool): split by instrument
    Returns:
        filename (str): the path(s) of the generated file
    """

    observations = read_observation_csvfile(csv_file)

    kernels = [mk_path]
    kernels.extend(ck_kernels)
    config = create_configuration(kernels, body)

    feature_map = {}
    for obs in observations:
        features = feature_map.get(obs.fov, [])
        features.extend(
            process_observation(
                config, obs.start, obs.end, obs.fov, obs.get_rate(), base
            )
        )
        feature_map[obs.fov] = features

    observations_start = clean_utc(min(observations, key=lambda obs: obs.start).start)
    observations_end = clean_utc(max(observations, key=lambda obs: obs.end).end)
    scene_id = f"jui_{body.lower()[:3]}_{observations_start}_{observations_end}"
    filenames = []

    if split:
        for fov in feature_map:
            filenames.append(
                __dump_features(feature_map[fov], f"{scene_id}_{fov.lower()}.geojson")
            )
    else:
        all_features = list(chain(*feature_map.values()))
        filenames.append(__dump_features(all_features, f"{scene_id}_all.geojson"))

    return filenames


def __dump_features(features, filename):
    dump_file(features, filename)
    logging.info(f"{filename} generated")
    return filename


def cli(args=None):
    """Process command line arguments."""

    parser = argparse.ArgumentParser(
        description="Create a geojson file(s) loadable by a given JUICE Cesium scenario with the features containing the geometry of the footprints of an instrument timeline."
    )
    parser.add_argument(
        "-mk", "--metakernel", type=str, help="the path to metakernel", required=True
    )
    parser.add_argument(
        "-b", "--body", type=str, help="Central body name. eg: Europa", required=True
    )
    parser.add_argument(
        "-c",
        "--ck_kernels",
        type=str,
        nargs="+",
        help="list of additional ck kernels",
        default=[],
    )
    parser.add_argument(
        "-f",
        "--file",
        type=argparse.FileType("r"),
        help="Path to the CSV file",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--split",
        action="store_true",
        help="Generate files split by instrument (default: false)",
    )

    parser.add_argument(
        "-bs",
        "--base_step",
        type=int,
        default=5,
        help=(
            "Defines the sample step used for the shape calculations, the"
            " default is 5 seconds that is the recommended for on-the-fly"
            " representations as its value affects linearly to the"
            " performance time!"
        ),
    )

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s[%(levelname)s] %(message)s",
    )

    args = parser.parse_args()

    try:
        generate(
            args.metakernel,
            args.ck_kernels,
            args.body,
            args.file,
            args.split,
            args.base_step,
        )
    except SpiceyError:
        logging.exception("SpiceyPy error")
