#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib
import weather

def test41():
    """
    Checks wether the file islost.html from 'http://www.islostarepeat.com/' is equal to 'http://www.islostarepeat.com/'.
    """
    testfile = urllib.URLopener()
    testfile.retrieve("http://www.islostarepeat.com/", "islost.html")
    assert weather.get_html('http://www.islostarepeat.com/',0)==open('islost.html','r').read().decode('utf-8')

