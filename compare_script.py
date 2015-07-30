#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  This script was created so that one can compare today's weather with yesterday's.
#
#  Creator: Callum Kift
#  email: callumkift@gmail.com
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

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


def getaddress(apiURL, ip):
    """
    Gets location information from IP address
    :param apiURL: URL of api that gives location information
    :param ip: ip address
    :return: json of location information
    """

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


def getweatherhist(lat, long):
    """
    Gets weather history json
    :param lat: Latitude
    :param long: Longitude
    :return: Weather history json
    """

    apiURL = "http://api.openweathermap.org/data/2.5/history/city?lat=%f&lon=%f" % (lat, long)
    u = urllib2.urlopen(apiURL)
    response = u.read()
    return response


def getweatherforecast(lat, long):
    """
    Gets weather forecast json
    :param lat: Latitude
    :param long: Longitude
    :return: Weather forecast json
    """

    apiURL = "http://api.openweathermap.org/data/2.5/forecast?lat=%f&lon=%f" % (lat, long)
    u = urllib2.urlopen(apiURL, timeout=1)
    response = u.read()
    return response


def getweathercurrent(lat, long):
    """
    Gets current weather json
    :param lat: latitude
    :param long: longitude
    :return: Current weather json
    """
    apiURL = "http://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f" % (lat, long)
    u = urllib2.urlopen(apiURL, timeout=1)
    response = u.read()
    return response


if __name__ == '__main__':

    freegeoip = "http://freegeoip.net/json/"

    if internet_on():
        print "Connected"

        pubip = getip()

        location_json_str = getaddress(freegeoip, pubip)
        loc_city, loc_lat, loc_long = getlatlong(location_json_str)

        history_info = getweatherhist(loc_lat, loc_long)
        current_info = getweathercurrent(loc_lat, loc_long)
        forecast_info = getweatherforecast(loc_lat, loc_long)


    else:
        print "Error: Device not connected to internet"
