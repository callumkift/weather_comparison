#!/usr/bin/env python
"""
Methods that get location data of the device.
"""

import urllib2
import json


def internet_on():
    """
    Method to check if connected to internet.
    :return: Boolean
    """
    while True:
        try:
            site_check = "http://google.com/"
            urllib2.urlopen(site_check, timeout=1)
            break
        except urllib2.URLError as e:
            pass
    return


def getip():
    """
    Method gets device IP address.
    :return: ip address
    """
    while True:
        try:
            ipadd = urllib2.urlopen('http://ip.42.pl/raw').read()
            break
        except urllib2.URLError as e:
            pass
    return ipadd


def getaddress(ip):
    """
    Gets location information from IP address
    :param apiURL: URL of api that gives location information
    :param ip: ip address
    :return: json of location information
    """
    while True:
        try:
            apiURL = "http://freegeoip.net/json/"
            url = "{}{}".format(apiURL, ip)
            u = urllib2.urlopen(url, timeout=1)
            response = u.read()
            break
        except urllib2.URLError as e:
            pass
    return response


def getlatlong(loc_json_str):
    """
    Extracts latitude and longitude
    :param loc_json_str: Location JSON string
    :return:
    """

    loc_dict = json.loads(loc_json_str)
    loc = loc_dict["city"] + ", " + loc_dict["country_code"]
    lat = loc_dict["latitude"]
    long = loc_dict["longitude"]
    return loc, lat, long
