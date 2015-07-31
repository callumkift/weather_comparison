#!/usr/bin/env python
"""
Methods that visualise the weather data.
"""

import json
import unitconverter as uc
import datetime as dt


def getcurrentinfo(current_json):
    """
    Extracts data from current weather json
    :param current_json: JSON of current weather
    :return: list of current weather info
                [time, weather_description, temperature, wind_speed, sunrise, sunset, pressure, humidity]
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
    :param history_json: history json
    :return: list of datetimes and temperatures
                [time, temperature]
    """

    historyinfo = json.loads(history_json)

    ndata = historyinfo["cnt"]
    histdatetemp = []

    for i in range(ndata):
        htime = (historyinfo["list"])[i]["dt"]
        htemp = (historyinfo["list"])[i]["main"]["temp"]
        histdatetemp.append([htime, htemp])

    return histdatetemp


def getforecastinfo(forecast_info):
    """
    Extracts next 24hrs of forecast json
    :param forecast_info:  forecast json
    :return: list of forecast data
                [time, weather_description, temperature, wind_speed, rain_fall]
    """

    forecastinfo = json.loads(forecast_info)

    ndata = forecastinfo["cnt"]
    now = dt.datetime.now()
    secsinday = 60 * 60 * 24


    foreinfo = []

    for i in range(ndata):
        forerain = (forecastinfo["list"])[i]["rain"]
        forewd = ((forecastinfo["list"])[i]["weather"])[0]["description"]
        foretime = uc.datetimeconverter((forecastinfo["list"])[i]["dt"])
        foretemp = uc.temperatureconverter((forecastinfo["list"])[i]["main"]["temp"])
        forewind = (forecastinfo["list"])[i]["wind"]["speed"]

        if len(forerain) == 0:
            forerain = 0.0
        else:
            forerain = forerain["3h"]

        diffindays = (foretime - now).total_seconds() /secsinday

        if diffindays < 1.0:
            foreinfo.append([foretime, forewd, foretemp, forewind, forerain])


    # keys = []
    #
    # for key in forecastinfo:
    #     keys.append(key)
    #
    # for i in range(len(keys)):
    #     print keys[i], "\n", forecastinfo[keys[i]], "\n"

    return foreinfo
