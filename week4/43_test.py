#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import weather
import cPickle as pickle


def test43():
    """
    >>> cache = pickle.load(open('cached_data.p','r'))
    
    >>> -50 <= int(weather.get_forcast('Hannestad',cache['viktigesteder0'],12,False)[0][0][-1].encode('utf-8')) < 50 
    True
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
