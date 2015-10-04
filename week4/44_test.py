#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import weather
import cPickle as pickle
    

def test44(capfd):
    weather.weather_update(u'Hannestad',15,0)
    out, err = capfd.readouterr()
    assert "Retrieving data for cache" in out
    #Making dummy file
    weather.weather_update(u'Hannestad',15,0)
    
    cache=pickle.load(open('cached_data.p','r+b'))
    data = cache[u'Hannestad0']
    tmp = data[0:10] #splitting the data
    expired_timestamp=int(tmp)-21600     #Making the timestamp expire(Subtracting 1 day)
    tmp = str(expired_timestamp) + data[10:12] #concatenating the data again
    cache[u'Hannestad0']=tmp
    pickle.dump(cache,open('cached_data.p','wb')) #writing it to the dummy file
    weather.weather_update(u'Hannestad',15,0) #Do the weather call again. This also makes a new dummy file, a correct one.
    cache=pickle.load(open('cached_data.p','r+b')) #reading it again.
    data = cache[u'Hannestad0']
    tmp = data[0:10] #splitting the data
    assert expired_timestamp != tmp #check expired one is replaced
    weather.weather_update(u'Hannestad',15,0) #Do the weather call again
    cache=pickle.load(open('cached_data.p','r'))
    data = cache[u'Hannestad0']
    new_tmp = data[0:10] #splitting the data
    assert new_tmp == tmp #check expired one is replaced
