"""The script creates the contextual information of the S/C (position and attitude) including:
    3D visualization
    ground-track information
    Sun illumination
    in CZML format suitable for its visualizacion in the JUICE SOC cesium tool
"""

import argparse
import logging
import sys

import spiceypy as sp
from spiceypy.utils.exceptions import SpiceyError

from cesium_script.czml.scene import generate_czml
from cesium_script.util.format import clean_utc


def generate(mk_path, ck_kernels, start_utc, end_utc, step, body):
    """Creates the contextual information of the S/C (position and attitude) including:
    3D visualization
    ground-track information
    Sun illumination
    in CZML format suitable for its visualizacion in the JUICE SOC cesium tool

    Args:
        mk_path (str): path to the metakernel
        ck_kernels (list of str): list of additional ck kernels
        start_utc (str): scene start using UTC scale and ISO format (e.g. 2032-07-02T14:22:25Z)
        end_utc (str): scene end using UTC scale and ISO format (e.g. 2032-07-02T14:22:25Z)
        step (int): step used for scene calculations
        body (str): Orbiting body

    Returns:
        filename (str): the path of the CZML file
    """

    sp.kclear()
    sp.furnsh(mk_path)

    for ck_kernel in ck_kernels:
        sp.furnsh(ck_kernel)
        message = f"{ck_kernel} loaded"
        logging.info(message)

    doc = generate_czml(start_utc, end_utc, step, body)
    scene_id = f"jui_{body.lower()[:3]}_{clean_utc(start_utc)}_{clean_utc(end_utc)}"
    filename = f"{scene_id}.czml"
    with open(filename, "w") as file:
        doc.dump(file, indent=2)

    message = f"{filename} generated"
    logging.info(message)
    return filename


def cli(args=None):
    """Process command line arguments."""

    parser = argparse.ArgumentParser(
        description="Creates a CZML file containing the contextual information of the S/C (position and attitude)"
    )
    parser.add_argument(
        "-mk", "--metakernel", type=str, help="the path to metakernel", required=True
    )
    parser.add_argument(
        "-b", "--body", type=str, help="Central body name. eg: Europa", required=True
    )
    parser.add_argument(
        "-st",
        "--start_utc",
        type=str,
        help="Scene start using UTC scale and ISO format (e.g. 2032-07-02T14:22:25Z)",
        required=True,
    )
    parser.add_argument(
        "-et",
        "--end_utc",
        type=str,
        help="Scene end using UTC scale and ISO format (e.g. 2032-07-02T19:32:17Z)",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--step",
        type=int,
        help="Step size for SPICE calculations in seconds. Optional - The tool will decide the step size.",
        default=None,
    )

    parser.add_argument(
        "-c",
        "--ck_kernels",
        type=str,
        nargs="+",
        help="list of additional ck kernels",
        default=[],
    )

    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s[%(levelname)s] %(message)s",
    )

    try:
        generate(
            args.metakernel,
            args.ck_kernels,
            args.start_utc,
            args.end_utc,
            args.step,
            args.body,
        )
    except SpiceyError as e:
        logging.error(e.short)
        logging.error(e.message)
