#!/usr/bin/env python
"""
Methods that create an interactive visualisation of the weather data.
"""

import json
import unitconverter as uc
import datetime as dt
from collections import OrderedDict
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource


def interactiveplot(history_json, current_json, forecast_json):
    """
    Method that calls all other methods (controls) for the interactive plot.
    :param history_json: JSON of weather history
    :param current_json: JSON of current weather
    :param forecast_json: JSON of weather forecast
    :return:
    """
    histdata = extracthistory(history_json)
    currdata = extractcurrent(current_json)
    foredata = extractforecast(forecast_json)
    drawgraph(histdata, currdata, foredata)

    return


def extracthistory(history_json):
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


def extractcurrent(current_json):
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


def extractforecast(forecast_json):
    """
    Extracts next 24hrs of forecast json
    :param forecast_json:  forecast json
    :return: list of forecast data
                [time, weather_description, temperature, wind_speed, rain_fall]
    """

    forecastinfo = json.loads(forecast_json)

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


def drawgraph(hist_list, curr_list, fore_list):
    htime, htemp = zip(*hist_list)

    ctime = curr_list[0]; cwd = curr_list[1]; ctemp = curr_list[2]; cwspeed = curr_list[3]
    csrise = curr_list[4]; csset = curr_list[5]; cpress = curr_list[6]; chum = curr_list[7]
    ftime, fwd, ftemp, fwspeed, frain = zip(*fore_list)

    htime, ftime = overlaptimes(htime, ftime)

    # output to static HTML file
    output_file("wc.html", title="Weather Comparison")

    # create a new plot with a title and axis labels
    p = figure(title="Weather Comparison", x_axis_label="Time", y_axis_label="Temperature")

    # add a line renderer with legend and line thickness
    p.line(htime, htemp, color="blue", line_width=2, alpha=0.3)
    p.line(ftime, ftemp, color="red", line_width=2)

    # show the results
    show(p)
    return


def overlaptimes(htime, ftime):


    oneday = 24
    secsinhour = 60 * 60
    fmintime = ftime[0]

    hdates = [oneday + ((time - fmintime).total_seconds() / secsinhour) for time in htime]
    fdates = [(time - fmintime).total_seconds() / secsinhour for time in ftime]

    ht = [fmintime + dt.timedelta(hours=hour) for hour in hdates]
    ft = [fmintime + dt.timedelta(hours=hour) for hour in fdates]

    return ht, ft