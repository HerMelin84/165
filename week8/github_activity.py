import os
import re
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from subprocess import check_output
from collections import Counter
from datetime import datetime
import argparse

class cd:
    """manages the current working directory"""
    def __init__(self, path):
        self.path = os.path.expanduser(path)

    def __enter__(self):
        self.sPath = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.sPath)


def is_git(filepath,save):
    #checks if it is a git directory. 
    with cd(filepath):
        if subprocess.call(["git","rev-parse","--git-dir"])==0:
            plot_activity(git_log(),save)
        else:
            print "The filepath: "+filepath+" is not a git directory"


def plot_activity(data,save):
    #iterates through the data and makes it plottable. 
    date_object=[]
    author_object=[]
    print data
    for i in data:
        a=datetime.strptime(i[1], '%a %b %d %H:%M:%S %Y')#does not work on ifi's computers?
        new_date=datetime(a.year,a.month,a.day)
        if i[0] not in author_object:
            author_object.append(i[0])
        if new_date not in date_object:
            date_object.append(new_date)
        
    author_dict=dict()
    for i in data:
        a=datetime.strptime(i[1], '%a %b %d %H:%M:%S %Y') #does not work on ifi's computers?
        new_date=datetime(a.year,a.month,a.day) 
        if i[0] in author_dict:
            indeks = date_object.index(new_date)
            author_dict[i[0]][indeks]+=1
        else:
            count_per_date=[0 for x in xrange(len(date_object))]
            author_dict[i[0]]=count_per_date
            indeks = date_object.index(new_date)
            author_dict[i[0]][indeks]+=1
    print author_dict
    mult_bar=plt.figure()
    ax=plt.subplot(111)
    colorlist=['y','b','r','g','c','m','k','w']
    i=0
    #plots each author as an individual bar in a bar in the plot.
    for key in author_dict:
        ax.bar(date_object,author_dict[key],color=colorlist[i],align='center',label=key)
        i+=1
    ax.xaxis_date()
    ax.set_title('Git repo activity diagram', size=16, weight='bold')
    plt.legend()
    
    if save: #saves to file. 
        plt.savefig(save)
    

def git_log():
    a=subprocess.check_output(["git","log","--date=local"])
    pattern = ".*?Author: (.*?>).*?Date:\s+?(\w+?\s+?\w+?\s+?\w+?\s+?[\w\:]+?\s+?\w+?)\s+?"
    data= re.findall(pattern,a,re.S)
    return data
    
def main(filepath,save):
    is_git(filepath,save)
    



parser = argparse.ArgumentParser(description='Check git activity in given repo')

parser.add_argument('filepath', metavar='f', type=str, default='.',
                   help='the gir-repo')
parser.add_argument("-s",'--save', dest="ifilename", required=False,
                    help="save the plot to the given file", metavar="IFILE")

args=parser.parse_args()
main(args.filepath,args.ifilename)
