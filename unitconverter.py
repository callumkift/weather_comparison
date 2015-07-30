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
    return temp_kelvin - zerokelvin
