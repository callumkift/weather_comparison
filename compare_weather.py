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

import getlocation as gl
import weathercalls as wc
import bokehvisualise as bv

if __name__ == '__main__':
    if gl.internet_on():
        pubip = gl.getip()
        location_json_str = gl.getaddress(pubip)
        loc_city, loc_lat, loc_long = gl.getlatlong(location_json_str)

        print "Location identified"

        history_info = wc.getweatherhist(loc_lat, loc_long)
        current_info = wc.getweathercurrent(loc_lat, loc_long)
        forecast_info = wc.getweatherforecast(loc_lat, loc_long)

        print "All weather info retrieved.\n"

        bv.interactiveplot(history_info, current_info, forecast_info)
    else:
        print "\nError: Cannot connect, please check internet connection.\n"
