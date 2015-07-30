#!/usr/bin/env python

import urllib2
import json

def internet_on():
    """
    Method to check if connected to internet.
    :return: Boolean
    """

    try:
        site_check = "http://google.com/"
        urllib2.urlopen(site_check, timeout=1)
        return True
    except urllib2.URLError as e:
        pass
    return False


def getip():
    """
    Method gets device IP address.
    :return: ip address
    """

    return urllib2.urlopen('http://ip.42.pl/raw').read()


def getaddress(ip):
    """
    Gets location information from IP address
    :param apiURL: URL of api that gives location information
    :param ip: ip address
    :return: json of location information
    """

    apiURL = "http://freegeoip.net/json/"
    url = "{}{}".format(apiURL, ip)
    u = urllib2.urlopen(url, timeout=1)
    response = u.read()
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