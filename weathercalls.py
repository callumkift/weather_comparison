#!/usr/bin/env python

import urllib2


def getweatherhist(lat, long):
    """
    Gets weather history json
    :param lat: Latitude
    :param long: Longitude
    :return: Weather history json
    """

    try:
        apiURL = "http://api.openweathermap.org/data/2.5/history/city?lat=%f&lon=%f" % (lat, long)
        u = urllib2.urlopen(apiURL, timeout=2)
        response = u.read()
        return response
    except urllib2.URLError as e:
        pass
    return False


def getweatherforecast(lat, long):
    """
    Gets weather forecast json
    :param lat: Latitude
    :param long: Longitude
    :return: Weather forecast json
    """

    try:
        apiURL = "http://api.openweathermap.org/data/2.5/forecast?lat=%f&lon=%f" % (lat, long)
        u = urllib2.urlopen(apiURL, timeout=2)
        response = u.read()
        return response
    except urllib2.URLError as e:
        pass
    return False

def getweathercurrent(lat, long):
    """
    Gets current weather json
    :param lat: latitude
    :param long: longitude
    :return: Current weather json
    """

    try:
        apiURL = "http://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f" % (lat, long)
        u = urllib2.urlopen(apiURL, timeout=2)
        response = u.read()
        return response
    except urllib2.URLError as e:
        pass
    return False