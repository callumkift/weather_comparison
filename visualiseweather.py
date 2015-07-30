#!/usr/bin/env python
"""
Methods that visualise the weather data.
"""

import json
import unitconverter as uc


def printcurrent(current_json):
    """
    Extracts data from current weather json
    :param current_json: JSON of current weather
    :return:
    """

    weatherinfo = json.loads(current_json)

    time = uc.datetimeconverter(weatherinfo["dt"]).strftime('%H:%M')
    wd = (weatherinfo["weather"][0])["description"]
    temp = uc.temperatureconverter(weatherinfo["main"]["temp"])  # degrees
    pressure = weatherinfo["main"]["pressure"]  # hPa
    humidity = weatherinfo["main"]["humidity"]  # %
    windspeed = weatherinfo["wind"]["speed"]  # m / s
    sunrise = uc.datetimeconverter(weatherinfo["sys"]["sunrise"]).strftime('%H:%M:%S')
    sunset = uc.datetimeconverter(weatherinfo["sys"]["sunset"]).strftime('%H:%M:%S')

    print "time: ", time
    print "weather description: %s" % wd
    print "temperature: %f" % temp
    print "pressure: ", pressure
    print "humidity: ", humidity
    print "wind speed: %f" % windspeed
    print "sunrise: ", sunrise
    print "sunset: ", sunset

    return
