#!/usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import urllib2
import sys
import cgi
import time
import os

def get_html(link):
    try:
        testfile = urllib2.urlopen(link)
        unicode_text = testfile.read().decode('utf-8')
        return unicode_text
    except ValueError:
        return 0


def create_list(html,pattern,stadnamn):
    if stadnamn=='blank':
        url_list=re.findall(pattern,html)
    else:
        url_list=re.findall(pattern[0],html) if re.findall(pattern[0],html) else (re.findall(pattern[1],html) if re.findall(pattern[1],html) else re.findall(pattern[2],html))
    if len(url_list) >100:
        return url_list[:100]
    else:
        return url_list

def finn_xml(arg):
    stadnamn=arg
    html=get_html("http://fil.nrk.no/yr/viktigestader/noreg.txt")
    url_list=[]
    if stadnamn=='blank':
        pattern='.+(http:.*.xml?)'
        return create_list(html,pattern,stadnamn)
    else:
        if '*' in stadnamn:
            patterns=['\d+\s?'+stadnamn.encode('utf-8')+'\s.+xml\thttp:.*.xml\t(http:.*.xml)',
                      '\d+\s\w+?\s'+stadnamn.encode('utf-8')+'\s.+xml\thttp:.*.xml\t(http:.*.xml)',
                      '.+'+stadnamn.encode('utf-8')+'\s.+?(http:.*xml\thttp:.*.xml\t(http:.*.xml)']
            return create_list(html,patterns,stadnamn)
        else:
            patterns=['\d+\s'+stadnamn.encode('utf-8')+'\s\d.+?xml\thttp:.*.xml\t(http:.*.xml)',
                      '\d+\s\w+?\s'+stadnamn.encode('utf-8')+'\s\d.+?xml\thttp:.*.xml\t(http:.*.xml)',
                      '.+'+stadnamn.encode('utf-8')+'\s.+?xml\thttp:.*.xml\t(http:.*.xml)']
            return create_list(html,patterns,stadnamn)
def start(arg):
    if arg=='' or arg=='*':
        xml_list= finn_xml('blank')
        print xml_list

    else:
        xml_list= finn_xml(arg.title().decode('utf-8'))
        xml = get_html(xml_list[0].encode('utf-8')) if xml_list else "empty"
        return xml



def getForcast(arg):
    a= datetime.now().strftime('%Y-%m-%d') if int(time.strftime("%H"))<18 else datetime.now() + relativedelta(days=1)
    print a
    xml=start(arg)
    pattern='<tabular>.+?from="%sT(.+?)"\sto=".+?(\d+\:\d+\:\d+)".*?<symbol.*?name="(\w+\s\w+).+?precipitation value="(\d\.?\d?)".+?mps="(\d\.?\d?).+?"\svalue="(\d\.?\d?).+?"' %a
    b= re.findall(pattern,xml,re.S)
    print b


class lazy:
    timestamp= time.strftime("%m:%dT%H")
    
    def __init__(self,arg):
        self.arg=arg
        self.filename=arg+'cache.txt'
        self.buffer = open(filename,'w+').read()
        if os.stat(filename).st_size==0:
            buffer.write(timestamp+'\n'+start())
        

    def __call__(self,arg):
        if arg in self.buffer:
            return self.buffer[arg]
        retval=self.func(arg)
        self.buffer[arg]=retval
        return retval
    def __get__(self,obj):
        if buffer_age():
            return buffer

    def buffer_age():
        with open (filename) as f:
            first_line =f.readline()
            if int(first_line.date[:2])<int(timestamp[:2]):
                #update
            elif int(first_line.date[3:5])<int(timestamp[3:5]):
                #update
            elif int(first_line.date[6:])<int(timestamp[6:])-6:
                print "update"


            
        with open ('testcache.txt') as f:
            first_line =f.readline()
            if int(first_line.date[:2])<int(timestamp[:2]):
                #update
            elif int(first_line.date[3:5])<int(timestamp[3:5]):
                #update
            elif int(first_line.date[6:])<int(timestamp[6:])-6:
                print "update"
