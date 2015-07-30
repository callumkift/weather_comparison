#!/usr/bin/env python
"""
Methods that visualise the weather data.
"""

import json


def printcurrent(current_json):
    """
    Extracts data from current weather json
    :param current_json: JSON of current weather
    :return:
    """

    weatherinfo = json.loads(current_json)

    time = weatherinfo["dt"]
    wd = (weatherinfo["weather"][0])["description"]
    temp = weatherinfo["main"]["temp"]
    pressure = weatherinfo["main"]["pressure"]
    humidity = weatherinfo["main"]["humidity"]
    windspeed = weatherinfo["wind"]["speed"]
    sunrise = weatherinfo["sys"]["sunrise"]
    sunset = weatherinfo["sys"]["sunset"]

    print time
    print wd
    print temp
    print pressure
    print humidity
    print windspeed
    print sunrise
    print sunset

    return
