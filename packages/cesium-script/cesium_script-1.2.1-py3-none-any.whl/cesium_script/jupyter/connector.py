import io
import os

import requests

from cesium_script.util.http import parse_request_body


def send_geojson_file(body, filename, cesium_host):
    """Retrieves a URL that points to a cesium viewer instance that
    displays the geojson file passed as input

    Args:
        body (str): the central body
        filename (str): the path to the filename
        cesium_host (str): URL of the cesium server

    Returns:
        url (str): the viewer URL
    """
    handler = open(filename, "rb")
    return __send_file("geojson", body, handler, cesium_host)


def send_geojson_content(body, content, cesium_host):
    """Retrieves a URL that points to a cesium viewer instance that
    displays the geojson represented by the string passed as input

    Args:
        body (str): the central body
        content (str): the string with the geojson serialization
        cesium_host (str): URL of the cesium server

    Returns:
        url (str): the viewer URL
    """
    handler = io.StringIO(content)
    return __send_file("geojson", body, handler, cesium_host)


def send_czml_file(body, filename, cesium_host):
    """Retrieves a URL that points to a cesium viewer instance that
    displays the czml file passed as input

    Args:
        body (str): the central body
        filename (str): the path to the filename
        cesium_host (str): URL of the cesium server

    Returns:
        url (str): the viewer URL
    """
    handler = open(filename, "rb")
    return __send_file("czml", body, handler, cesium_host)


def send_czml_content(body, content, cesium_host):
    """Retrieves a URL that points to a cesium viewer instance that
    displays the czmlo represented by the string passed as input

    Args:
        body (str): the central body
        content (str): the string with the czml serialization
        cesium_host (str): URL of the cesium server

    Returns:
        url (str): the viewer URL
    """
    handler = io.StringIO(content)
    return __send_file("czml", body, handler, cesium_host)


def __send_file(request_type, body, handler, cesium_host):
    url = f"{cesium_host}/upload/"
    files = {"upload_file": handler}
    r = requests.post(url, files=files)
    if r.status_code == 200:
        params = parse_request_body(r.content)
        session_id = os.path.basename(params.get("upload_file.path", ""))
        return __build_viewer_url(request_type, body, session_id, cesium_host)
    raise RuntimeError("File cannot be uploaded")


def __build_viewer_url(request_type, body, session_id, cesium_host):
    return f"{cesium_host}/cesium/?{request_type}={session_id}&body={body}"
