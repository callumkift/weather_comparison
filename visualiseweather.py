#!/usr/bin/env python
"""
Methods that visualise the weather data.
"""

import json
import unitconverter as uc


def getcurrentinfo(current_json):
    """
    Extracts data from current weather json
    :param current_json: JSON of current weather
    :return:
    """

    weatherinfo = json.loads(current_json)

    time = uc.datetimeconverter(weatherinfo["dt"])  # .strftime("%H:%M")
    wd = (weatherinfo["weather"][0])["description"]
    temp = uc.temperatureconverter(weatherinfo["main"]["temp"])  # degrees
    pressure = weatherinfo["main"]["pressure"]  # hPa
    humidity = weatherinfo["main"]["humidity"]  # %
    windspeed = int(weatherinfo["wind"]["speed"])  # m / s
    sunrise = uc.datetimeconverter(weatherinfo["sys"]["sunrise"])  # .strftime("%H:%M")
    sunset = uc.datetimeconverter(weatherinfo["sys"]["sunset"])  # .strftime("%H:%M")

    return [time, wd, temp, windspeed, sunrise, sunset, pressure, humidity]


def gethistoryinfo(history_json):
    """
    Extracts datetime and temperature from history json
    :param history_json: history json data
    :return: list of datetimes and temperatures
    """

    historyinfo = json.loads(history_json)

    ndata = historyinfo["cnt"]
    histdatetemp = []

    for i in range(ndata):
        htime = (historyinfo["list"])[i]["dt"]
        htemp = (historyinfo["list"])[i]["main"]["temp"]
        histdatetemp.append([htime, htemp])

    return histdatetemp
