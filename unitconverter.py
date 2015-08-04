#!/usr/bin/env python
"""
Methods that convert weather data.
"""

import datetime as dt


def datetimeconverter(uf_dt):
    """
    Takes a unix timestamp and returns datetime format
    :param uf_dt: Unix timestamp
    :return: datetime format
    """

    return dt.datetime.fromtimestamp(uf_dt)


def temperatureconverter(temp_kelvin):
    """
    Converts temperature from kelvin to degrees
    :param temp_kelvin: temperature in kelvin
    :return: temperature in degrees
    """

    zerokelvin = 273.15
    return int(temp_kelvin - zerokelvin)


def winddirection(wind_deg):
    """
    Takes the wind direction in degrees and returns the direction (N, NE, E, etc)
    :param wind_deg: wind direction in degrees
    :return: wind direction in compass style
    """
    if wind_deg > 337.5 or wind_deg < 22.5:
        wind_dir = "N"
    elif wind_deg > 22.5 and wind_deg < 67.5:
        wind_dir = "NE"
    elif wind_deg > 67.5 and wind_deg < 112.5:
        wind_dir = "E"
    elif wind_deg > 112.5 and wind_deg < 157.5:
        wind_dir = "SE"
    elif wind_deg > 157.5 and wind_deg < 202.5:
        wind_dir = "S"
    elif wind_deg > 202.5 and wind_deg < 247.5:
        wind_dir = "SW"
    elif wind_deg > 247.5 and wind_deg < 292.5:
        wind_dir = "W"
    elif wind_deg > 292.5 and wind_deg < 337.5:
        wind_dir = "NW"

    return wind_dir
