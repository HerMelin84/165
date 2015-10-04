#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import weather
import cPickle as pickle

def test42():
    weather.weather_update(u'Hannestad',15,0) #To create the bufferfile, easy access
    return_link=u'http://www.yr.no/place/Norway/Østfold/Sarpsborg/Hannestad/forecast.xml'
    cache=pickle.load(open('cached_data.p','r'))
    assert weather.find_xml_links(u'Hannestad',cache['viktigesteder0'])[0]==return_link
