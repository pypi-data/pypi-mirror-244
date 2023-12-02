def clean_utc(utc_str):
    """Cleans up a date string to get a timestamp string in minutes for filenames

    Args:
        utc_str (str): Time zoned ISOC formatted UTC date

    Returns:
        timestamp (str): Timestamp
    """
    return utc_str.replace(":", "").replace("-", "")[:13]
