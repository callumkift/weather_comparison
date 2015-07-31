#!/usr/bin/env python
"""
Methods that obtain weather data from online.
"""
import urllib2


def getweatherhist(lat, long):
    """
    Gets weather history json
    :param lat: Latitude
    :param long: Longitude
    :return: Weather history json
    """
    while True:
        try:
            apiURL = "http://api.openweathermap.org/data/2.5/history/city?lat=%f&lon=%f" % (lat, long)
            u = urllib2.urlopen(apiURL, timeout=2)
            response = u.read()
            break
        except urllib2.URLError as e:
            pass
    return response


def getweatherforecast(lat, long):
    """
    Gets weather forecast json
    :param lat: Latitude
    :param long: Longitude
    :return: Weather forecast json
    """
    while True:
        try:
            apiURL = "http://api.openweathermap.org/data/2.5/forecast?lat=%f&lon=%f" % (lat, long)
            u = urllib2.urlopen(apiURL, timeout=2)
            response = u.read()
            break
        except urllib2.URLError as e:
            pass
    return response


def getweathercurrent(lat, long):
    """
    Gets current weather json
    :param lat: latitude
    :param long: longitude
    :return: Current weather json
    """
    while True:
        try:
            apiURL = "http://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f" % (lat, long)
            u = urllib2.urlopen(apiURL, timeout=2)
            response = u.read()
            break
        except urllib2.URLError as e:
            pass
    return response
