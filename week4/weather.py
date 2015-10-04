#!/usr/bin/python
# -*- coding:utf-8 -*-
#######IMPORTS############

from datetime import datetime
from dateutil.relativedelta import relativedelta
import cPickle as pickle
import re
import urllib2
import time
import os
###ERROR MESSAGES###
BROKEN_LINK_ERROR= "HTTPError: The link to the xml file was broken.\nCould not fetch weather data!"
URL_ERROR = "URLError: You do not seem to have an internet connection!"

def get_html(link,location):
    """ Retrieves the file from the given link. 
    Returns the file as a str.
    
    catches urllib2.HTTPError,ValueError, urllib2.URLError
    
    Keyword arguments:
    link -- the link to the file to be retrieved.
    location(string) - the location(place in the world) which is given in weather_update() 
    """

    try:
        testfile = urllib2.urlopen(link.encode('utf-8'))
        unicode_text = testfile.read().decode('utf-8')
        testfile.close()
        return unicode_text
    except urllib2.HTTPError:
        return BROKEN_LINK_ERROR
    except ValueError:
        return 0
    except urllib2.URLError:
        return URL_ERROR

def create_xml_link_lists(html,patterns,location):
    """
    Creates a list of xml-links, returns list which will be less than 100 in length. 

    Keyword arguments: 
    html -- the weather data containing all the xml-links. 
    patterns -- the patterns to be used for regex.
    location -- the name of the location, where weatherdata will be fetched.  

    Returns:
    list of xml-links, max 100 elements, empty if none found. 
    """
    if location=='blank':
        url_list=re.findall(patterns,html)
    else:
        url_list=re.findall(patterns[0],html) if re.findall(patterns[0],html) else (re.findall(patterns[1],html) if re.findall(patterns[1],html) else re.findall(patterns[2],html))
    if len(url_list)>100:
        print "The number of results exceeded 100, first 100 was returned."
        return url_list[:100]
    else:
        return url_list

def find_xml_links(location,data):
    """
    This function creates the different regex patterns and send them to the create_xml_link_lists function.
    Keyword arguments: 
    html -- the weather data containing all the xml-links. 
    patterns -- the patterns to be used for regex.
    location -- the name of the location, where weatherdata will be fetched.  

    Returns list of xml_link created in create_xml_link_lists
    """
    if location=='blank': #specifying the pattern
        pattern='.+(http:.*.xml?)'
        return create_xml_link_lists(data,pattern,location)
    else:
        if '*' in location: #specifying the pattern
            location_n=location.replace("*",".*?");
            patterns=['\d+\s?'+location_n+'\s?\w+?\s.+xml\thttp:.*.xml\t(http:.*.xml)', #Stad
                      '\d+\s\w+?\s\d+?\s\w+\s\w+\s\w+\s'+location_n+'\s.+xml\thttp:.*.xml\t(http:.*.xml)', #Kommune
                      '\d+\s\w+?\s\d+?\s\w+\s\w+\s\w+\s\w+\s'+location_n+'\s?\w+?\s?\w+?\s.+?http:.*xml\thttp:.*.xml\t(http:.*.xml)'] #Fylke.
            return create_xml_link_lists(data,patterns,location)
        else:
            patterns=['\d+\s'+location+'\t.+?xml\thttp:.*.xml\t(http:.*.xml)', #Stad
                      '\d+\s\w+?\s\d+?\s\w+\s\w+\s\w+\s'+location+' \d.+?xml\thttp:.*.xml\t(http:.*.xml)', #Kommune
                      '\d+\s\w+?\s\d+?\s\w+\s\w+\s\w+\s\w+\s'+location+'\s.+?xml\thttp:.*.xml\t(http:.*.xml)']#Fylke
            return create_xml_link_lists(data,patterns,location)

def find_xml_data(location,data):
    """
    This function find xml files from yrs websites.
    

    Keyword arguments: 
    location -- the name of the location, where weatherdata will be fetched.  
    data -- the html file containing all the xml-links and places. Get it from cached_data.p or get_html 
    
    Returns a list with all xml-files from yrs website if a match for the location is found.
    If a link is broker, BROKEN_LINK_ERROR is printed and '0' returned. 
    If there were any errors with the url, URL_ERROR is printed and '0' returned.
    """
 
    if location=='' or location=='*':
        xml_list= find_xml_links('blank',data)
        xml=[lazy_data(xml_list[i],location,i) for i in xrange(0,len(xml_list)) if xml_list]                
        return xml
    else:
        xml_list= find_xml_links(location,data)
        xml = [lazy_data(xml_list[i],location,i) for i in xrange(0,len(xml_list)) if xml_list ]
        if BROKEN_LINK_ERROR in xml:
            print BROKEN_LINK_ERROR #if broken link
            return xml
        elif URL_ERROR in xml:
            print URL_ERROR
            return xml
        return xml



def get_forcast(location,data,hour,next_day):
    """
    Function used by weather_update() to get weather data.
    
    Checks if hour is before current time. If it is, it find the data for tomorrow at the same time. Else today at that time.1
    Uses regex to find name, time from and to, weather summary, rain value, wind speed, and temperature.
    
    returns a list of xml data if it finds anything, else 0.
    """
    #checks what time interval are looked for
    if 0 <= hour < 6:
        date=datetime.now().strftime('%Y-%m-%dT') if not next_day else str((datetime.now() + relativedelta(days=1)).strftime('%Y-%m-%dT'))+"00:00:00"
    elif 6 <= hour < 12:
        date=datetime.now().strftime('%Y-%m-%dT') if not next_day else str((datetime.now() + relativedelta(days=1)).strftime('%Y-%m-%dT'))+"06:00:00"
    elif 12 <= hour <18:
        date=datetime.now().strftime('%Y-%m-%dT') if not next_day else str((datetime.now() + relativedelta(days=1)).strftime('%Y-%m-%dT'))+"12:00:00"
    else:
        date=datetime.now().strftime('%Y-%m-%dT') if not next_day else str((datetime.now() + relativedelta(days=1)).strftime('%Y-%m-%dT'))+"18:00:00"
    
    xml=find_xml_data(location,data) #gets xml-files in a list
    pattern_pt1='<name>(.*?)</name>.+?'
    pattern_pt2='<tabular>.+?from="(%s.*?)"\sto=".+?(\d+\:\d+\:\d+)".*?<symbol.*?name="(\w+\s\w+).+?' %date
    pattern_pt3='precipitation value="(\d\.?\d?)".+?mps="(\d\.?\d?).+?"\svalue="(\d\.?\d?).+?"'
    pattern= pattern_pt1+pattern_pt2+pattern_pt3
    try:
        return [re.findall(pattern,xml[i],re.S) for i in xrange(0,len(xml))]
    except TypeError:
        return 0
        
 
def weather_update(location,hour,minute):
    """
    Function that fetches weatherdata from yr.no.
    
    This function is using a lazy-function for cache/buffering. It will fetch new data if it is outdated(6 hours). 
    If this happens, it will use extra time. 

    prints out the data in this format:
    2015-10-05 12:27
    Hannestad: Clear sky, rain:0 mm, wind: 2.7 mps, temp: 11 deg C
    
    Keyword arguments:
    location -- the name of the location, where weatherdata will be fetched.  
    hour -- the our where weatherdata will be fetched.
    minute -- the minute 

    returns nothing

    Example:
    weather_update('Hannestad',12,00)
    """
    try:
        re.match("^[a-åA-Å\* ]*$",location.encode('utf-8'))
    except UnicodeDecodeError:
        print "Locations with unicode characters/special characters need to be given as:"
        print "u'location with unicode character'"
        print "Example: weather_update(u'Årdal',12,0)"
        return
    except AttributeError:
        print "The location needs to be a string, blank('') or '*'."
        print "Example: weather_update('*',12,0)"
        return
    if re.match("^[a-åA-Å\* ]*$",location.encode('utf-8')) == None:
        print "Location must be a string! Cannot contain numbers"
    else:
        data=lazy_data("http://fil.nrk.no/yr/viktigestader/noreg.txt","viktigesteder",0) 
        current_hour=time.strftime("%H")
        current_minute=time.strftime("%M")
        #checks wether the hour given is earlier or later than current time.
        if int(hour)>int(current_hour) or (int(hour)==int(current_hour) and int(minute)>int(current_minute)):
            next_day=False
        else:
            next_day=True
        weather_data=get_forcast(location,data,hour,next_day) #gets weatherdata
         
        if weather_data: # checks if there is any weatherdata.
            for s in weather_data:
                if s:  # checks if any data is from a broken link(empty) 
                    date=s[0][1][:10] #gets the date
                    minute=time.strftime('%M') #gets the minutes
                    clock=str(hour)+':'+minute # catenates to a timestamp
                    print "{0} {1}".format(date,clock)
                    print "{0}: {1}, rain:{2} mm, wind: {3} mps, temp: {4} deg C".format(s[0][0].encode('utf-8'),s[0][3],s[0][4],s[0][5],s[0][6])                    
        else:
            print "Could not find a place called {0}".format(location.encode('utf-8'))


def extreme_temperatures():
    """
    Function that finds the coldest and the warmest locations in norway.(at this point only among the 100 first on yr's site')
    
    prints out the max and min value on the format:
    Grøvet has the max temperature in norway at 12
    Demma has the max temperature in norway at 10
    
    Uses regex to find it temperature and place among the xml_files.
    
    returns nothing. 
    """
    data=lazy_data("http://fil.nr k.no/yr/viktigestader/noreg.txt","viktigesteder",0) #fetch data from cache or web
    xml_list=find_xml_data(u'*',data) # retreive xml_list
    tmrw_date_and_time=str((datetime.now() + relativedelta(days=1)).strftime('%Y-%m-%dT'))+'12:00:00' #13:00 tomorrow
    pattern='<name>(.*?)</name>.+?<tabular>.+?from="%s"\sto=.+?celsius"\svalue="(\d\.?\d?).+?".*' %tmrw_date_and_time #regex patter
    temperatures=[] #temperatures
    locations=[] #locations
    #creates a list of temperatures and locations
    location_and_temp = [re.findall(pattern,xml_list[i],re.S) for i in xrange(0,len(xml_list)) if re.findall(pattern,xml_list[i],re.S)] 
    for data in location_and_temp:
        locations.append(data[0][0])
        temperatures.append(data[0][1])
        
    max_temp = max(temperatures) 
    min_temp = min(temperatures)
    
    print "{0} has the max temperature in norway at {1}".format(locations[temperatures.index(max_temp.encode('utf-8'))].encode('utf-8'),max_temp)
    print "{0} has the max temperature in norway at {1}".format(locations[temperatures.index(min_temp.encode('utf-8'))].encode('utf-8'),min_temp)

class lazy:
    """
    lazy buffer class.
    saves xml and html data in a file, called 'cached_data.p'. Use cPickler to open it. Keys are name of a place ending with an int.
    if only one result, its 0, else 1,2,3.. up to 100.

    __call__ checkes if the file has been created, if not creates it. Then checks if the location is cached in the file.
    if it is, it returns it. Else computes it and adds it to the cache. Also checks if it is outdated, if it is fetches new data
    and puts it in the file. 

    cache_aged check if the cache is "outdated" or not. In this implementation, it is assumed outdated if it is longer than 6 hours since 
    last time it fetched the data. 
    """
    def __init__(self,func):
        self.func=func
        self.cache={}

    def __call__(self,link,location,i):
        
        if not os.path.isfile('cached_data.p'): #checks if the cache file exists
            open('cached_data.p','a').close()
        else:
            self.cache=pickle.load(open('cached_data.p','r+b')) 
        if location+str(i) in self.cache and not self.cache_aged(location,i): #checks if it is cached and not outdated
            print "Retrieving data for cache"
            return self.cache[location+str(i)]
            
        timestamp = int(time.mktime(time.localtime()))+21600 #timestamp for 6 hours
        retval=self.func(link,location) # getting the url-files
        self.cache[location+str(i)]=str(timestamp)+retval #adding the timestamp at the front of the url-data
        pickle.dump(self.cache,open('cached_data.p','r+b')) #write to cache file
        return retval 

    def cache_aged(self,location,i):
        timestamp = time.mktime(time.localtime())
        #checks if thestamp is outdated.
        if int(self.cache[location+str(i)][:10])<(int(timestamp)): 
            return True
        else:
            return False    



lazy_data = lazy(get_html)
