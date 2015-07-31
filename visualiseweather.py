#!/usr/bin/env python
"""
Methods that visualise the weather data.
"""

import json
import unitconverter as uc
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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
        histdatetemp.append([uc.datetimeconverter(htime), uc.temperatureconverter(htemp)])

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
    firsttime = uc.datetimeconverter((forecastinfo["list"])[0]["dt"])
    secsinday = 60 * 60 * 24

    foreinfo = []

    for i in range(ndata):

        forewd = ((forecastinfo["list"])[i]["weather"])[0]["description"]
        foretime = uc.datetimeconverter((forecastinfo["list"])[i]["dt"])
        foretemp = uc.temperatureconverter((forecastinfo["list"])[i]["main"]["temp"])
        forewind = (forecastinfo["list"])[i]["wind"]["speed"]

        try:
            forerain = (forecastinfo["list"])[i]["rain"]
            if len(forerain) == 0:
                forerain = 0.0
            else:
                forerain = forerain["3h"]
        except KeyError as e:
            forerain = 0.0

        diffindays = (foretime - firsttime).total_seconds() / secsinday

        if diffindays < 1.0:
            foreinfo.append([foretime, forewd, foretemp, forewind, forerain])

    return foreinfo


def plotweathercompare(history_list, forecast_list):
    """
    Plots today's forecast and yesterday's history
    :param history_list: list of weather history data
    :param forecast_list: list of weather forecast data
    :return:
    """

    histtime, histtemp = zip(*history_list)
    foretime, forewd, foretemp, forewind, forerain = zip(*forecast_list)

    fmintime = foretime[0]
    fmaxtime = foretime[-1]
    oneday = 24
    secsinhour = 60 * 60

    hdates = [oneday + ((time - fmintime).total_seconds() / secsinhour) for time in histtime]
    fdates = [(time - fmintime).total_seconds() / secsinhour for time in foretime]

    hdates = [fmintime + dt.timedelta(hours=hour) for hour in hdates]
    fdates = [fmintime + dt.timedelta(hours=hour) for hour in fdates]

    htmax = np.amax(histtemp)
    htmin = np.amin(histtemp)
    ftmax = np.amax(foretemp)
    ftmin = np.amin(foretemp)

    if htmax > ftmax:
        tempaxismax = htmax
    else:
        tempaxismax = ftmax

    if htmin < ftmin:
        tempaxismin = htmin
    else:
        tempaxismin = ftmin

    fig, ax1 = plt.subplots()
    plt.suptitle("Forecast Comparison")

    ax1.plot(hdates, histtemp, "ro-", label="Yesterday")
    ax1.plot(fdates, foretemp, "go-", label="Today")
    ax1.set_xlabel(r"Time")
    ax1.set_ylabel(r"Temperature $(^{o}C)$")
    ax1.set_xlim(fmintime, fmaxtime)
    ax1.set_ylim(tempaxismin - 1, tempaxismax + 1)
    ax1.xaxis.set_major_formatter(mdates.HourLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax1.legend(loc=1)

    ax2 = ax1.twinx()
    ax2.vlines(fdates, 0.0, forerain, 'b')
    ax2.set_ylim(0.0, np.max(forerain) + 0.05)
    ax2.set_ylabel(r"Rainfull $(mm)$", color="b")
    for tl in ax2.get_yticklabels():
        tl.set_color('b')

    plt.show()
    return
