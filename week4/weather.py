#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import urllib2
import sys
def get_html(link):
    try:
        testfile = urllib2.urlopen(link)
        html = testfile.read()
        return html.split('\n')
    except ValueError:
        return 0


def create_list(html,patterns,stadnamn):
    url_list=[]
    for line in html:
        if stadnamn=='*':
            url_list.append(re.match(patterns[0],line).group(1))
            continue
        elif stadnamn in line:
            if re.match(patterns[0],line) != None:
                url_list.append(re.match(patterns[0],line).group(1))
            elif re.match(patterns[1],line) != None:
                url_list.append(re.match(patterns[1],line).group(1))
            else:
                url_list.append(re.match(patterns[2],line).group(1))
                
    if len(url_list) >100:
        return url_list[:100]
    else:
        return url_list

def finn_xml(arg):
    stadnamn=arg
    html=get_html(sys.argv[1])
    url_list=[]
    if stadnamn=='*':
        patterns=['.+(http:.*.xml?)']
        create_list(html,patterns,stadnamn)
    else:
        if '*' in stadnamn:
            patterns=['\d+\s?'+stadnamn+'\s.+?(http:.*?.xml?)',
                      '\d+\s\w+?\s'+stadnamn+'\s.+?(http:.*?.xml?)',
                      '.+'+stadnamn+'\s.+?(http:.*?.xml?)']
            return create_list(html,patterns,stadnamn)
        else:
            patterns=['\d+\s?'+stadnamn+'\t.+?(http:.*?.xml?)',
                      '\d+\s\w+?\s'+stadnamn+'\s.+?(http:.*?.xml?)',
                      '.+'+stadnamn+'\s.+?(http:.*?.xml?)']
            return create_list(html,patterns,stadnamn)


xml_list= finn_xml(sys.argv[2])

print xml_list
