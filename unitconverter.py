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
