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

class lazy:
    timestamp= time.strftime("%m:%dT%H")
    def __init__(self,func):
        self.func = func
        self.buffer = open('yrcache.txt','w+').read()
        if os.stat('yrcache.txt').st_size==0:
            buffer.write(timestamp+'\n'+get_html("http://fil.nrk.no/yr/viktigestader/noreg.txt"))
        

    def __call__(self,arg):
        if arg in self.buffer:
            return self.buffer[arg]
        retval=self.func(arg)
        self.buffer[arg]=retval
        return retval
    def __get__(self,obj):
        if()

