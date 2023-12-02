"""The sensor package collects the definition of sensor to be displayed as part of the spacecraft in the CZML scene
"""

from .juice_offsets import map_offsets


def sensor(sensor_type):
    def common(name, parent, start_utc, end_utc, **kwargs):
        return {
            "name": name,
            "parent": parent,
            "availability": f"{start_utc}/{end_utc}",
            "position": {"reference": f"{parent}#position"},
            "orientation": {"reference": f"{parent}#orientation"},
        }

    def child_sensor(color, **kwargs):
        return {
            "show": True,
            "showIntersection": True,
            "showEnvironmentIntersection": True,
            "showLateralSurfaces": False,
            "showEllipsoidSurfaces": True,
            "showEllipsoidHorizonSurfaces": False,
            "showDomeSurfaces": False,
            "showThroughEllipsoid": False,
            "intersectionColor": {"rgba": [0, 145, 0, 255]},
            "lateralSurfaceMaterial": {"solidColor": {"color": {"rgba": color}}},
            "intersectionWidth": 1,
        }

    def sensor_generic(function):
        def wrapper(*args, **kwargs):
            func = function(*args, **kwargs)
            properties = map_offsets.get(kwargs["name"], {})
            properties["sensor"] = {"boolean": True}
            return common(**kwargs) | {
                sensor_type: child_sensor(**kwargs) | func,
                "properties": properties,
            }

        return wrapper

    return sensor_generic


@sensor("agi_rectangularSensor")
def rectangular(
    x_half_angle=0,
    y_half_angle=0,
    name=None,
    parent=None,
    start_utc=None,
    end_utc=None,
    color=None,
):
    """Generates a rectangular pyramid sensor volume taking into account occlusion of an ellipsoid, i.e., the globe.
    Parameters:
        x_half_angle (float): The X half angle in radians
        y_half_angle (float): The Y half angle in radians
        name (str): Sensor name
        parent (str): Spacecraft id that holds the sensor
        start_utc (str): Date with the start of the sensor availability using UTC scale and expressed in ISOC format (e.g. 2023-04-14T12:43:00Z)
        end_utc (str): Date with the end of the sensor availability using UTC scale and expressed in ISOC format (e.g. 2023-04-14T12:43:00Z)
        color (list int): Color RGBA formated as a list of integers between 0 and 127 (e.g. [127, 0 , 0, 66])
    Returns:
        sensor (object): a python object representing the sensor
    """
    return {"xHalfAngle": x_half_angle, "yHalfAngle": y_half_angle}


@sensor("agi_customPatternSensor")
def custom(
    cartesian_list=None,
    name=None,
    parent=None,
    start_utc=None,
    end_utc=None,
    color=None,
):
    """Generates a custom sensor volume taking into account occlusion of an ellipsoid, i.e., the globe.
    Parameters:
        cartesian_list (list float): The list of directions defining the custom sensor expressed in cartesian coordinates.
        name (str): Sensor name
        parent (str): Spacecraft id that holds the sensor
        start_utc (str): Date with the start of the sensor availability using UTC scale and expressed in ISOC format (e.g. 2023-04-14T12:43:00Z)
        end_utc (str): Date with the end of the sensor availability using UTC scale and expressed in ISOC format (e.g. 2023-04-14T12:43:00Z)
        color (list int): Color RGBA formated as a list of integers between 0 and 127 (e.g. [127, 0 , 0, 66])
    Returns:
        sensor (object): a python object representing the sensor
    """
    return {"directions": {"unitCartesian": cartesian_list}}
