import numpy as np
import weave
from math import sin,pi
from matplotlib import pyplot

def solve(n,m,t0,t1,dt,nu,f,verbose):
    """
    takes in the arguments needed to calculate the heat diffusion.
    includes verbose mode. 
    """
    if verbose:
        print "Calculation from {0} to {1} with dt={2}".format(t0,t1,dt)
    if not isinstance(f,np.ndarray):
        f1=f
        f=np.zeros((m,n))
        f.fill(f1)

    u=np.zeros((m,n))
    u_new=np.zeros((m,n))
    t=float(t0)
    expr = """
    int i;
    int j;
    while(t<t1){
    for(i=0;i<100;i++){
    for(j=0;j<50;j++){
    u_new(i,j)=u(i,j) + dt*(nu*u(i-1,j) + nu*u(i, j-1) - 4*nu*u(i, j) + nu*u(i,j+1) + nu*u(i+1, j) + f(i, j));
    }
  }
    u=u_new;
    t=t+dt;

  }"""
    if verbose:
        print "Uses weaves inline function to run the program in c for performance";
    weave.inline(expr, ['n','m','u','u_new','nu','dt','t','t1','f'], type_converters=weave.converters.blitz, compiler='gcc')
    if verbose:
        print "Returns the numpy array with the calculations"
    return u_new

def analytic(n,m):
    #analytic solution
    analytic_u=np.zeros((m,n))
    for j in xrange(m):
        for i in xrange(n):
            analytic_u[j,i]=sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)
    return analytic_u

def heat_source(n,m,nu):
    #heat source data
    f=np.zeros((m,n))
    for j in xrange(m):
        for i in xrange(n):
            f[j,i]=nu*((2*np.pi/(n-1))**2 + (2*np.pi/(m-1))**2)*np.sin(2*np.pi/(m-1)*j)\
                     *np.sin(2*np.pi/(n-1)*i)
    return f

def main(n,m,t0,t1,dt,nu,f,plot,verbose,test,save):
    if test:
        analytic_u =analytic(n,m)
        f=heat_source(n,m,nu)
        u_new=solve(n,m,t0,t1,dt,nu,f,verbose)
        if verbose:
            print "Calculates the data from the analytical approach, then the heat source data, then data from my approach."
            err = (abs(u_new - analytic_u)).max()
            print "The maximum error, or difference, is: {0}".format(err)
    else:
        u_new=solve(n,m,t0,t1,dt,nu,f,verbose)
    if plot:
        if verbose:
            print "Plots the data from my approach"
        fig, ax=pyplot.subplots()
        cax=ax.imshow(u_new,interpolation='nearest',cmap=pyplot.cm.Greys_r)
        cbar=fig.colorbar(cax)
        pyplot.tight_layout()
        pyplot.show()
        if save:
            if verbose:
                print "Saves the plot as c_plot.png"
            pyplot.savefig('c_plot.png')
    return u_new
if __name__ == "__main__":
    print "use 'python heat_equation_ui.py' instead"
