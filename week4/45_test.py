#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import weather
import cPickle as pickle

def test45():
    cache=pickle.load(open('cached_data.p','r'))
    #checking if the temperature is between -50 and 50.
    assert -50< float(weather.get_forcast(u'Hannestad',cache['viktigesteder0'],15,False)[0][0][-1]) <= 50    

