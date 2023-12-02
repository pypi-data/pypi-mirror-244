import re


def __parse_content_disposition(row):
    pattern = re.compile('Content-Disposition: form-data; name="(.*)"')
    match = pattern.match(row)
    if match:
        return match.group(1)
    return None


def __parse_field(fields, parameters):
    name = __parse_content_disposition(fields[1])
    if name:
        parameters[name] = fields[3]


def parse_request_body(content):
    """The method extracts the form-data key/values stored in a HTTP request body
    Args:
        content (list of bytes): the raw body of an http request
    Returns:
        parameters (dictionary): name/value of the form-data parameters
    """
    parameters = {}
    response = content.decode("utf-8")
    fields = response.split("\r\n")
    for index in range(0, len(fields), 4):
        __parse_field(fields[index : index + 4], parameters)
    return parameters
