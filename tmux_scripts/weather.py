#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import urllib2
import re
import ast
import os
import json
import datetime
from dateutil import parser
import sys


WD = os.path.join(os.path.dirname(__file__), 'weather_data.json')
CITY_URLS = {
    # add your city url here
    'bucharest': 'http://www.accuweather.com/en/ro/bucharest/287430/weather-forecast/287430',
    'berlin': 'http://www.accuweather.com/en/de/berlin/10178/weather-forecast/178087',
    'lisbon': 'http://www.accuweather.com/en/pt/lisbon/274087/weather-forecast/274087',
    'london': 'http://www.accuweather.com/en/gb/london/ec4a-2/weather-forecast/328328'
}


def _check_if_update_is_needed(weather_data, city, interval=1200):
    """Checks if weather update is needed.

    :param weather_data: str
    :param city: str
    :param interval: int
    :returns bool
    """
    if not os.path.isfile(weather_data):
        with open(weather_data, 'w') as f:
            f.write('{}')
        return True
    try:
        with open(weather_data, 'r') as infile:
            data = json.load(infile)[city]
        last_updated = parser.parse(data['updated'])
        time_diff = datetime.datetime.now() - last_updated
        if datetime.timedelta.total_seconds(time_diff) >= interval:
            return True
        else:
            return False
    except KeyError:
        return True

def write_weather_data(url, weather_data_file, city):
    """Dumps data to json.

    :param url: str
    :param weather_data_file: str
    :param city: str
    """
    if _check_if_update_is_needed(weather_data_file, city):
        html = urllib2.urlopen(url).read()
        weather_info = re.sub(
            '"', "'", re.findall(r"(?:acm_RecentLocationsCarousel\.push\()(.*})", html)[0])
        weather_dict = ast.literal_eval(re.sub(r"(\w+)(?=:')", r"'\1'", weather_info))
        weather_dict['updated'] = str(datetime.datetime.now())
        with open(weather_data_file, 'r+') as f:
            data = json.load(f)
            data[city] = weather_dict
            f.seek(0)
            json.dump(data, f, indent=4)

def return_weather_data(weather_data_file, city):
    """Returns city name, current temperature and condition.

    :param weather_data_file: str
    :param city: str
    :returns weather_info: str
    """
    with open(weather_data_file, 'r') as data_file:
        weather = json.load(data_file)[city]
        weather_info = '%s: %s %s' % (weather['name'].split(',')[0],
                                      weather['temp'] + '°'.decode('UTF-8'),
                                      weather['text'])
    return weather_info

def main(cities):
    x = ''
    for i in cities:
        write_weather_data(CITY_URLS[i.lower()], WD, i)
        x += ' | ' + return_weather_data(WD, i).encode('UTF-8')
    print x.lstrip(' | ')

if __name__ == '__main__':
    main(sys.argv[1:])
