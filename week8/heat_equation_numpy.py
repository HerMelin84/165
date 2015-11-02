from matplotlib import pyplot
from math import sin,pi
import numpy as np

def solve(n,m,t0,t1,dt,nu,f,verbose):
    """
    takes in the arguments needed to calculate the heat diffusion.
    includes verbose mode. 
    """
    if verbose:
        print "calculation from {0} to {1} with dt={2}".format(t0,t1,dt,f)
    if not isinstance(f,np.ndarray):
        f1=f
        f=np.zeros((m,n))
        f.fill(f1)
    u=np.zeros((m,n))
    u_new=np.zeros((m,n))
    t=float(t0)
    if verbose:
        print "Starts the calculations"
    while(t<t1):
        u[1:-1,1:-1]=u_new[1:-1,1:-1]= u[1:-1,1:-1] + \
        dt*(nu*u[:-2,1:-1] + nu*u[1:-1,:-2] - \
            4*nu*u[1:-1,1:-1]+nu*u[1:-1,2:] + nu*u[2:,1:-1] +f[1:-1,1:-1]) 
        t=t+dt
    if verbose:
        print "Finished the timestep calculation"
    return u_new

def heat_source(n,m,nu):
    #heat source data
    f=np.zeros((m,n))
    for j in xrange(m):
        for i in xrange(n):
            f[j,i]=nu*((2*np.pi/(n-1))**2 + (2*np.pi/(m-1))**2)*np.sin(2*np.pi/(m-1)*j)\
                     *np.sin(2*np.pi/(n-1)*i)
    return f



def analytic(n,m):
    #analytic solution
    analytic_u=np.zeros((m,n))
    for j in xrange(m):
        for i in xrange(n):
            analytic_u[j,i]=sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)
    return analytic_u

def main(n,m,t0,t1,dt,nu,f,plot,verbose,test,save):
    if test:
        if verbose:
            print "Running tests"
        analytic_u =analytic(n,m)
        f=heat_source(n,m,nu)
        u_new=solve(n,m,t0,t1,dt,nu,f,verbose)
        if verbose:
            err = (abs(u_new - analytic_u)).max()
            print err
    else:
        u_new=solve(n,m,t0,t1,dt,nu,f,verbose)
    if(plot):
        fig, ax=pyplot.subplots()
        cax=ax.imshow(u_new,interpolation='nearest',cmap=pyplot.cm.Greys_r)
        cbar=fig.colorbar(cax)
        pyplot.tight_layout()
        pyplot.show()
        if save:
            if verbose:
                print "Saves the plot as numpy_plot.png"
            pyplot.savefig('numpy_plot.png')
    return u_new

if __name__ == "__main__":
    print "use 'python heat_equation_ui.py' instead"
