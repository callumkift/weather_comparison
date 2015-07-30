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


if __name__ == '__main__':

    if internet_on():
        print "Connected"
    else:
        print "Error: Device not connected to internet"

