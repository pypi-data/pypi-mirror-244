"""Collection of utilities and auxiliary functions to create the czml content
"""

import colorsys

import spiceypy as sp


def get_n_colors(n=5):
    """Generates a palette of n colors expressed as a list of RGB arrays

    Args:
        n (int, optional): The number of colors to be generated. Defaults to 5.

    Returns:
        colors: list of rgb arrays: a list of RGB arrays reprensenting colors
    """
    hsv_tuples = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    hex_out = []
    for rgb in hsv_tuples:
        rgb = [int(x * 255) for x in colorsys.hsv_to_rgb(*rgb)]
        hex_out.append(rgb)
    return hex_out


def get_body_data(body):
    """Returns the radius and the flatness of the body

    Args:
        body (str): NAIF id of the body

    Returns:
        radii, flatness (float, float): a
    """
    n, radii = sp.bodvrd(body, "RADII", 3)
    if n == 1:
        f = 0
    else:
        re = radii[0]
        rp = radii[1]
        f = (re - rp) / re
    return radii[0], f


def get_lon_lat(rectan, f, radius):
    """Convert from rectangular coordinates to geodetic coordinates.

    Args:
        rectan (list float): Rectangular coordinates of a point.
        re (float): Equatorial radius of the reference spheroid.
        f (float): Flattening coefficient.
    Returns:
        geodetic coords (tuple): Geodetic longitude (radians), Geodetic latitude (radians), Altitude above reference spheroid
    """
    lon, lat, alt = sp.recgeo(rectan, radius, f)
    return (lon, lat, alt)


def get_cartograhic_radians(body, spoints):
    """Convert from a list of rectangular coordinates to geodetic coordinates.

    Args:
        body (str): Name of the body
        spoints (list float): List of rectangular coordinates
    Returns:
        geodetic coords (tuple): Geodetic longitude (radians), Geodetic latitude (radians) of the points
    """
    radius, f = get_body_data(body)
    return [get_lon_lat(point, f, radius) for point in spoints]


def get_positions(ets, target, body):
    """Return the list of positions of a target relative to a body corresponding to the input list of dates

    Args:
        ets (list float): list of ephemeris times
        target (str): target object
        body (str): reference body

    Returns:
        _type_: Return the position of a target body relative to an observing body
    """
    pos, lt = sp.spkpos(target, ets, "IAU_" + body, "NONE", body)
    return pos


def get_illumination(et, sc, body, position):
    """Return the illumination angles (phase, solar incidence, and emission) at a specified time of a target body

    Args:
        et (float): list of ephemeris times
        sc (str): spacecraft
        body (str): reference body
        position (list float): ray direction vector
    Returns:
        illumination (tuple): the illumination angles (phase, solar incidence, and emission)
    """
    method = "ELLIPSOID"
    frame = "IAU_" + body
    spoint, trgepc, srfvec = sp.sincpt(
        method, body, et, frame, "NONE", sc, frame, sp.vminus(position)
    )
    trgepc, srfvec, phase, incdnc, emssn = sp.ilumin(
        method, body, et, frame, "NONE", sc, spoint
    )

    return phase, incdnc, emssn, srfvec


def get_quaternions(ets, frame, body):
    """Return the list of quaternion that transforms position vectors from one specified frame to another at a specified epochs.

    Args:
        ets (list float): list of ephemeris times
        frame (str): frame
        body (str): reference body

    Returns:
        quaternions (list of quaternions): SPICE quaternion list
    """
    quaternions = []
    for ct in ets:
        matrix = sp.pxform(frame, body, ct)
        quat = sp.m2q(matrix)
        quaternions.append(quat)
    return quaternions


def generate_cartesians(positions, step=None):
    """Formats the list of SPICE cartesian positions (km) into a Cesium (timed) list of cartesian positions (m)

    Args:
        positions (list position): list of SPICE positions (km)
        step (float, optional): step used if the list is relative timed. Defaults to None.

    Returns:
        cartesian_list (object): (timed) list of cartesian positions
    """
    km_to_m = 1e3
    cartesians = []
    for index, position in enumerate(positions):
        if step:
            ct = index * step
            cartesians.append(ct)
        cartesians.append(position[0] * km_to_m)
        cartesians.append(position[1] * km_to_m)
        cartesians.append(position[2] * km_to_m)
    return cartesians


def generate_unit_quaternion(quaternions, step):
    """Formats the list of SPICE quaternions into a Cesium timed list of quaternions

    Args:
        quaternions (list position): list of SPICE quaternions
        step (float): step used for the quaternion generations

    Returns:
        quaternion_list (object): Timed list of CZML quaternions
    """

    unit_quaternion = []
    for index, quaternion in enumerate(quaternions):
        ct = index * step
        unit_quaternion.append(ct)
        unit_quaternion.append(quaternion[1])
        unit_quaternion.append(quaternion[2])
        unit_quaternion.append(quaternion[3])
        unit_quaternion.append(quaternion[0])
    return unit_quaternion


def generate_html_table(properties):
    """Returns the HTML Table representation of a key, value map

    Args:
        properties (map): key/value map

    Returns:
        html_content (str): HTML Table
    """

    html = '<table class="groundtrack-table">'
    for key, value in properties.items():
        html += f"<tr><th>{key}</th><td>{value}</td></tr>"
    html += "</table>"
    return html


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
