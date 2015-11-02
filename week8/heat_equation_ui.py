import argparse
import os.path
import timeit
import numpy as np
import heat_equation as normal_solution
import heat_equation_numpy as np_solution
import heat_equation_weave as c_solution


#!/usr/bin/env python


def wrapper(func,n,m,t0,t1,dt,nu,f,plot,verbose,test,save):
    """
    Wrapper function for when i need to use the timeit.
    """
    def wrapped():
        return func(n,m,t0,t1,dt,nu,f,plot,verbose,test,save)
    return wrapped


def is_valid_file(parser, arg):
    return open(arg, 'w+')  # return an open file handle

#Running the numpy solution
def run_numpy(n,m,t0,t1,dt,nu,f,plot,verbose,test,time,save,ofilename,ifilename):
    
    if ifilename:                              #Reads data from file
        with open(ifilename,'r+') as file:
            data=file.read()
        data=data.split(',')                   #Must have ',' as delimiter. Easy to crash.
        if len(data)==7:                       #Must have all the data,
            n=int(data[0]);m=int(data[1]);t0=int(data[2]);t1=int(data[3])
            dt=float(data[4]);nu=float(data[5]);f=float(data[6])
        else:
            print "The file must contain all the data."
            return
    if time:                                   #if -time is called
        wrapped=wrapper(np_solution.main,n,m,t0,t1,dt,nu,f,False,False,test,save)
        num=10
        time=timeit.timeit(wrapped,number=num)        
        print "Average run time is {0} in after {1} runs.".format(time/num,num)
    else:
        u_new=np_solution.main(int(n),int(m),int(t0),int(t1),float(dt),float(nu),float(f),plot,verbose,test,save)
        if ofilename:                          #writes data to file
            np.savetxt(ofilename, u_new, delimiter=',')
            
#Running the c solution
def run_c(n,m,t0,t1,dt,nu,f,plot,verbose,test,time,save,ofilename,ifilename):
    if ifilename:                              #Reads data from file
        with open(ifilename,'r+') as file:
            data=file.read()
        data=data.split(',')                   #Must have ',' as delimiter. Easy to crash.
        if len(data)==7:                       #Must have all the data,
            n=int(data[0]);m=int(data[1]);t0=int(data[2]);t1=int(data[3])
            dt=float(data[4]);nu=float(data[5]);f=float(data[6])
        else:
            print "The file must contain all the data."
            return

    if time:                                   #if -time is called
        wrapped=wrapper(c_solution.main,int(n),int(m),int(t0),int(t1),float(dt),float(nu),float(f),False,False,test,save)
        num=10
        time=timeit.timeit(wrapped,number=num)      
        print "Average run time is {0} in after {1} runs.".format(time/num,num)
    else:
        u_new=c_solution.main(int(n),int(m),int(t0),int(t1),float(dt),float(nu),float(f),plot,verbose,test,save)
        if ofilename:                          #writes data to file
            np.savetxt(ofilename, u_new, delimiter=',')



#Running the normal solution
def run_normal(n,m,t0,t1,dt,nu,f,plot,verbose,test,time,save,ofilename,ifilename):
    if ifilename:                              #Reads data from file
        with open(ifilename,'r+') as file:
            data=file.read()
        data=data.split(',')                   #Must have ',' as delimiter. Easy to crash.
        if len(data)==7:                       #Must have all the data,
            n=int(data[0]);m=int(data[1]);t0=int(data[2]);t1=int(data[3])
            dt=float(data[4]);nu=float(data[5]);f=float(data[6])
        else:
            print "The file must contain all the data."
            return

    if time:                                   #if -time is called
        feedback=raw_input("This will take a LONG time, are you sure about this?[y/n]")
        if feedback=='y' or feedback=='yes':
            wrapped=wrapper(normal_solution.main,int(n),int(m),int(t0),int(t1),float(dt),float(nu),float(f),False,False,test)
            num=5
            time=timeit.timeit(wrapped,number=num)        
            print "Average run time is {0} in after {1} runs.".format(time/num,num)
        else:
            print "Exiting..."
    else:
        u_new=normal_solution.main(int(n),int(m),int(t0),int(t1),float(dt),float(nu),float(f),plot,verbose,test,save)
        if ofilename:                          #writes data to file
            with ofilename as file:
                file.writelines('\t'.join(str(j) for j in i) + '\n' for i in u_new)
         
parser = argparse.ArgumentParser(description='Calculate the heat equation')




parser.add_argument('-n',dest='n',metavar='n',nargs='?' ,default=50,required=False,
                    help="rectangle size x (default=50)")

parser.add_argument('-m',dest='m',metavar='m',nargs='?' ,default=100,required=False,
                    help="rectangle size y (default=100)")

parser.add_argument('-t0',dest='t0',metavar='t0',nargs='?',default=0,required=False,
                    help="Calcutation start time (default=0)")

parser.add_argument('-t1',dest='t1',metavar='t1',nargs='?' ,default=1000,required=False,
                    help="Calcutation stop time (default=1000)")

parser.add_argument('-dt',dest='dt',metavar='dt',nargs='?' ,default=0.1,required=False,
                    help="Calculation timestep (default=0.1)")

parser.add_argument('-nu',dest='nu',metavar='nu',nargs='?' ,default=1.0,required=False,
                    help="Calculation diffusion coefficient (default=1)")

parser.add_argument('-f',dest='f',metavar='f',nargs='?' ,default=1,required=False,
                    help="Calculation heat source (default=1)")


parser.add_argument('-t','--test',help="Calculates a test against an analytic solution with a given heat_source formula.",action="store_true")


#Run with numpy
parser.add_argument('-np','--numpy', dest='accumulate', action='store_const',
                    const=run_numpy, default=run_normal,
                    help='numpy solution (default is very slow)')

#Run with c
parser.add_argument('-c','--c', dest='accumulate', action='store_const',
                    const=run_c, default=run_normal,
                    help='c solution (default is very slow)')
#plot
parser.add_argument('-p','--plot',help="Plot (default=False)",action="store_true")
#verbose mode
parser.add_argument('-v','--verbose',help="prints out what the program does (default=False)",
                    action="store_true")
#timeit mode
parser.add_argument('-time','--timeit',help="Uses timeit module to print the time used. Plotting wil be disabled.",
                    action="store_true")
#save plot mode
parser.add_argument('-s','--save',help="Save the plot as a png(tmp_x.png). x being the solution",
                    action="store_true")
#read from file
parser.add_argument("-i", dest="ifilename", required=False,
                    help="input file with data", metavar="IFILE")
#save data to file. 
parser.add_argument("-o", dest="ofilename", required=False,
                    help="output file with the final solution", metavar="OFILE",
                    type=lambda x: is_valid_file(parser, x))

args=parser.parse_args()
if args.verbose and not args.timeit:
    print "verbosity turned on"

args.accumulate(args.n,args.m,args.t0,args.t1,args.dt,args.nu,args.f,args.plot,args.verbose,args.test,args.timeit,args.save,args.ofilename,args.ifilename)

