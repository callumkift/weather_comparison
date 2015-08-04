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
        # if i == 0:
        #     print (historyinfo["list"])[i]
        #     print "\n"
        htime = uc.datetimeconverter((historyinfo["list"])[i]["dt"])
        hwdes = (historyinfo["list"])[i]["weather"][0]["description"]
        htemp = uc.temperatureconverter((historyinfo["list"])[i]["main"]["temp"])
        hwspe = (historyinfo["list"])[i]["wind"]["speed"]
        hrain = "n/a"
        histdatetemp.append([htime, hwdes, htemp, hwspe, hrain])

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
    """
    Organises data to plot
    :param hist_list: list of history data
    :param curr_list: list of current data
    :param fore_list: list of forecast data
    :return:
    """

    output_file("wc.html", title="Weather Comparison")
    plot_hf = histfore(hist_list, fore_list)

    show(plot_hf)
    return


def histfore(histlist, forelist):
    """
    Organises plot that compares weather history and forecast
    :param histlist: list of history data
    :param forelist: list of forecast data
    :return: plot information
    """
    htime, hwd, htemp, hwspeed, hrain = zip(*histlist)
    ftime, fwd, ftemp, fwspeed, frain = zip(*forelist)
    htime, ftime = overlaptimes(htime, ftime)

    hsource = ColumnDataSource(
        data=dict(
            time=htime,
            temp=htemp,
            wdes=hwd,
            wspe=hwspeed,
            rain=hrain
        )
    )

    fsource = ColumnDataSource(
        data=dict(
            time=ftime,
            temp=ftemp,
            wdes=fwd,
            wspe=fwspeed,
            rain=frain
        )
    )

    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover"
    p = figure(title="Weather Comparison", x_axis_label="Time", y_axis_label=r"Temperature", x_axis_type="datetime",
               tools=TOOLS)

    p.line(htime, htemp, source=hsource, legend="Yesterday", color="blue", line_width=1, alpha=0.3)
    p.line(ftime, ftemp, source=fsource, legend="Today", color="red", line_width=1)
    p.circle(ftime, ftemp, source=fsource, legend="Today", color="red")
    p.legend.orientation = "bottom_left"

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict(
        [("Temperature", "@temp"), ("Description", "@wdes"), ("Windspeed (m/s)", "@wspe"),
         ("Rain (mm)", "@rain")])

    return p


def overlaptimes(htime, ftime):
    """
    Overlaps history and forecast times, so that they are easier to compare
    :param htime: list of history data times
    :param ftime: list of forecast data times
    :return: history and forecast time lists are overlapped
    """
    oneday = 24
    secsinhour = 60 * 60
    fmintime = ftime[0]

    hdates = [oneday + ((time - fmintime).total_seconds() / secsinhour) for time in htime]
    fdates = [(time - fmintime).total_seconds() / secsinhour for time in ftime]

    ht = [fmintime + dt.timedelta(hours=hour) for hour in hdates]
    ft = [fmintime + dt.timedelta(hours=hour) for hour in fdates]

    return ht, ft
