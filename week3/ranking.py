#!/usr/bin/env python
# -*- coding: utf-8 -*-
def get_cpu():
    f = open('data.log','r')
    cpu_dict = {}
    for line in f:
        if 'CPU' in line:
            arr=line.split()
            if not arr[1] in cpu_dict:
                cpu_t=[float(arr[-1])]
                cpu_dict[arr[1]]=cpu_t
            else:
                cpu_t.append(float(arr[-1]))
    for name in cpu_dict:
        print "Test name: %s" %name
        print "CPU time:  %.1f s (min)" %min(cpu_dict[name])
        print " %15.1f s (avg)" %(sum(cpu_dict[name])/float(len(cpu_dict[name])))
        print " %15.1f s (max)" %max(cpu_dict[name])
get_cpu()

