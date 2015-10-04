#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import weather
import cPickle as pickle

def test41():
    """
    Checks wether the file islost.html from 'http://www.islostarepeat.com/' is equal to 'http://www.islostarepeat.com/'.
    """
    assert weather.get_html('http://www.islostarepeat.com/',0)==open('islost.html','r').read().decode('utf-8')

