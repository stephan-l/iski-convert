#!/usr/bin/python
# coding=UTF-8

"""
Convert html saved from iSki tracker website to gpx format to import
any application or service such QLandkarteGT, Endomondo, slopes, etc.

inspired by vicziani/iski-convert.py

Need to install the following packages:

$ pip install pytz
$ pip install tzlocal

Usage:

Share your day and get URL like:
https://share.iski.cc/shares/share_iski/tracks/XYZ1234?lang=en
Download the data:
https://share.iski.cc/shares/share_iski/tracks/XYZ1234/geometry.json?lang=en
$ iski-convert.py <input-file> <date>
Example
$ iski-convert.py geometry.json 2024-03-01

Background:

There is no export function on iSki tracker website, but the html source
contains a link to the time, coordinates, profile in different format.
This script converts it to gpx that is a common GPS data format for software
applications.

The script use the locale timezone and convert the dates to UTC, because
the GPS format defines date in Coordinated Universal Time (UTC) using
ISO 8601 format. The Z at the end of the dates is the zone designator for
the zero UTC offset.

Works as of March 2024
Stephan Liell
"""

import sys
import json
from datetime import datetime, timedelta

import pytz  # $ pip install pytz
from tzlocal import get_localzone  # $ pip install tzlocal


def toisoformat(f, basedate):
    local_tz = get_localzone()
    d = datetime(basedate.year, basedate.month, basedate.day, tzinfo=local_tz)
    d = d + timedelta(milliseconds=f)
    d = d.astimezone(pytz.utc)
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def parsebasedate(line):
    basedate = datetime.strptime(line, "%Y-%m-%d")
    return basedate


if len(sys.argv) != 3:
    print("Usage: iski-convert.py <input-file> <date>")
    exit()

d = sys.argv[2]
basedate = parsebasedate(d)

print(
    """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>

<gpx xmlns="http://www.topografix.com/GPX/1/1" creator="byHand" version="1.1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
	<trk>
		<trkseg>""")

with open(sys.argv[1], 'r') as f:
    data = json.load(f)

for line in data['path']:
    print(
        "             <trkpt lon=\"", line['lng'], "\" lat=\"", line['lat'], "\">",
        "\n                 <ele>", line['elevation'], "</ele>",
        "\n                 <time>", toisoformat(float(line['time']), basedate), "</time>",
        "\n             </trkpt>", sep='')

print(
    """		</trkseg>
	</trk>
</gpx>""")
