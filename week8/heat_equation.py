from matplotlib import pyplot
from math import sin,pi
import copy
def evolve_func(n,m,t0,t1,dt,f,nu,verbose):
    """
    takes in the arguments needed to calculate the heat diffusion.
    includes verbose mode. 
    """
    if verbose:
        print "Calculations from {0} to {1} with dt={2}".format(t0,t1,dt)
    if not isinstance(f,list):
        f1=f
        f=[[f1 for i in xrange(n)] for j in range(m)]
        
    u=[[0 for i in xrange(n)] for j in range(m)]
    u_new=[[0 for i in xrange(n)] for j in range(m)]
    t=t0
    while(t<t1):
        for i in xrange(0,m-1):
            for j in xrange(0,n-1):
                u_new[i][j]= u[i][j] + dt*(nu*u[i-1][j] + nu*u[i][j-1] \
                                           - 4*nu*u[i][j] + nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])
        u=u_new
        t=t+dt
    return u_new

def analytic(n,m):
    #analytic solution
    analytic_u=[[0 for i in xrange(n)] for j in range(m)]
    for j in xrange(m-1):
        for i in xrange(n-1):
            analytic_u[j][i]=sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)
    return analytic_u

def heat_source(n,m,nu):
    #heat source data
    f=[[0 for i in xrange(n)] for j in range(m)]
    for j in xrange(m-1):
        for i in xrange(n-1):
            f[j][i]=nu*((2*pi/(n-1))**2 + (2*pi/(m-1))**2)*sin(2*pi/(m-1)*j)\
                     *sin(2*pi/(n-1)*i)
    return f

def main(n,m,t0,t1,dt,nu,f,plot,verbose,test,save):
    
    if test:
        if verbose:
            print "Running tests"
        analytic_u=analytic(n,m)
        f=heat_source(n,m,nu)
        u_new=evolve_func(n,m,t0,t1,dt,f,nu,verbose)
        if verbose:
            print "Calculates the data from the analytical approach, then the heat source data, then data from my approach."
            maxerr=0
            err=[[0 for i in xrange(n)] for j in range(m)]
            for i in xrange(m):
                for j in xrange(n):
                    err[i][j] = u_new[i][j] - analytic_u[i][j]
                    maxerr=max(maxerr,err[i][j])
                    
            print "The maximum error, or difference, is: {0}".format(maxerr)
    else:
        u_new=evolve_func(n,m,t0,t1,dt,f,nu,verbose)
        
    if(plot):
        fig, ax=pyplot.subplots()
        cax=ax.imshow(u_new,interpolation='nearest',cmap=pyplot.cm.Greys_r)
        cbar=fig.colorbar(cax)
        pyplot.tight_layout()
        pyplot.show()
        if save:
            if verbose:
                print "Saves the plot as normal_plot.png"
            pyplot.savefig('normal_plot.png')
    return u_new
if __name__ == "__main__":
    print "use 'python heat_equation_ui.py' instead"
