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
    visdata(histdata, currdata, foredata)

    return


def extracthistory(history_json):
    """
    Extracts datetime and temperature from history json
    :param history_json: history json
    :return: list of datetimes and temperatures
                [time, weather_description, temperature, wind_speed, wind_direction, rain_fall]
    """

    historyinfo = json.loads(history_json)

    ndata = historyinfo["cnt"]
    histdatetemp = []

    for i in range(ndata):
        # if i == 0:
        #     print (historyinfo["list"])[i]
        #     print "\n"
        htime = uc.datetimeconverter((historyinfo["list"])[i]["dt"])
        hwdes = ((historyinfo["list"])[i]["weather"][0]["description"]).lower()
        htemp = uc.temperatureconverter((historyinfo["list"])[i]["main"]["temp"])
        hwspe = int((historyinfo["list"])[i]["wind"]["speed"])
        hwdir = uc.winddirection((historyinfo["list"])[i]["wind"]["deg"])
        hrain = "n/a"

        histdatetemp.append([htime, hwdes, htemp, hwspe, hwdir, hrain])

    return histdatetemp


def extractcurrent(current_json):
    """
    Extracts data from current weather json
    :param current_json: JSON of current weather
    :return: list of current weather info
                [time, weather_description, temperature, wind_speed, sunrise, sunset, pressure, humidity]
    """

    weatherinfo = json.loads(current_json)
    
    city = weatherinfo["name"] + ", " + weatherinfo["sys"]["country"]
    time = uc.datetimeconverter(weatherinfo["dt"])  # .strftime("%H:%M")
    wd = (weatherinfo["weather"][0])["description"]
    temp = uc.temperatureconverter(weatherinfo["main"]["temp"])  # degrees
    pressure = weatherinfo["main"]["pressure"]  # hPa
    humidity = weatherinfo["main"]["humidity"]  # %
    windspeed = int(weatherinfo["wind"]["speed"])  # m / s
    winddir = uc.winddirection(weatherinfo["wind"]["deg"])
    sunrise = uc.datetimeconverter(weatherinfo["sys"]["sunrise"])
    sunset = uc.datetimeconverter(weatherinfo["sys"]["sunset"])

    return [time, city, wd, temp, windspeed, winddir, sunrise, sunset, pressure, humidity]


def extractforecast(forecast_json):
    """
    Extracts next 24hrs of forecast json
    :param forecast_json:  forecast json
    :return: list of forecast data
                [time, weather_description, temperature, wind_speed, wind_direction, rain_fall]
    """

    forecastinfo = json.loads(forecast_json)

    ndata = forecastinfo["cnt"]
    firsttime = uc.datetimeconverter((forecastinfo["list"])[0]["dt"])
    secsinday = 60 * 60 * 24

    foreinfo = []

    for i in range(ndata):

        forewd = (((forecastinfo["list"])[i]["weather"])[0]["description"]).lower()
        foretime = uc.datetimeconverter((forecastinfo["list"])[i]["dt"])
        foretemp = uc.temperatureconverter((forecastinfo["list"])[i]["main"]["temp"])
        forewind = int((forecastinfo["list"])[i]["wind"]["speed"])
        forewdir = uc.winddirection((forecastinfo["list"])[i]["wind"]["deg"])

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
            foreinfo.append([foretime, forewd, foretemp, forewind, forewdir, forerain])

    return foreinfo


def visdata(hist_list, curr_list, fore_list):
    """
    Organises data to plot
    :param hist_list: list of history data
    :param curr_list: list of current data
    :param fore_list: list of forecast data
    :return:
    """
    print_c = currdat(curr_list)
    plot_hf = histfore(hist_list, fore_list)
    output_file("wc.html", title="Weather Comparison")
    show(plot_hf)
    return


def currdat(clist):
    """
    Prints current weather info
    :param clist: list of weather info
    :return:
    """

    print "Date: %s" %clist[0].strftime("%d-%m-%y")
    print "Time: %s" %clist[0].strftime("%H:%M:%S")
    print "Place: %s" %clist[1]
    print "Description: %s" %clist[2]
    print "Temperature: %.1f" %clist[3]
    print "Wind speed: %d m/s" %clist[4]
    print "Wind direction: %s" %clist[5]
    print "Sunrise: %s" %clist[6].strftime("%H:%M:%S")
    print "Sunset: %s" %clist[7].strftime("%H:%M:%S")
    print "Pressure: %s hPa" %clist[8]
    print "Humidity: %s%%" %clist[9]

    return


def histfore(histlist, forelist):
    """
    Organises plot that compares weather history and forecast
    :param histlist: list of history data
    :param forelist: list of forecast data
    :return: plot information
    """
    htime, hwd, htemp, hwspeed, hwdir, hrain = zip(*histlist)
    ftime, fwd, ftemp, fwspeed, fwdir, frain = zip(*forelist)
    htime, ftime = overlaptimes(htime, ftime)

    hsource = ColumnDataSource(
        data=dict(
            time=htime,
            temp=htemp,
            wdes=hwd,
            wspe=hwspeed,
            wdir=hwdir,
            rain=hrain
        )
    )

    fsource = ColumnDataSource(
        data=dict(
            time=ftime,
            temp=ftemp,
            wdes=fwd,
            wspe=fwspeed,
            wdir=fwdir,
            rain=frain
        )
    )

    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover"
    p = figure(title="Weather Comparison", x_axis_label="Time", y_axis_label=r"Temperature", x_axis_type="datetime",
               tools=TOOLS)

    linewidth = 1  # linewidth of plot
    alpha = 0.3  # fade of history data

    p.line(htime, htemp, source=hsource, legend="Yesterday", color="blue", line_width=linewidth, alpha=alpha)
    p.line(ftime, ftemp, source=fsource, legend="Today", color="red", line_width=linewidth)
    p.circle(ftime, ftemp, source=fsource, legend="Today", color="red")
    p.legend.orientation = "bottom_left"

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict(
        [("Temperature", "@temp"), ("Description", "@wdes"), ("Wind speed (m/s)", "@wspe"), ("Wind direction", "@wdir"),
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
