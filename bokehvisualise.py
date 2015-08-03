#!/usr/bin/env python
"""
Methods that create an interactive visualisation of the weather data.
"""

import json
import unitconverter as uc
from collections import OrderedDict
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource


def interactiveplot(history_json, current_json, forecast_json):

    histdata = extracthistory(history_json)
    t, temp = zip(*histdata)

    # output to static HTML file
    output_file("hist.html", title="line plot example")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(t, temp, line_width=2)

    # show the results
    show(p)

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
        histdatetemp.append([htime, uc.temperatureconverter(htemp)])

    return histdatetemp