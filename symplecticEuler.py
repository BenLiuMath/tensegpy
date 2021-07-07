import numpy as np
def symplecticEuler(dXdt,dVdt,tspan,X0,V0):
    Nsteps = len(tspan)-1;
    Nvars = np.prod(X0.shape);
    X = X0;
    V = V0;
    Xsave = np.zeros( (Nvars,1+Nsteps) );
    Vsave = 0.*Xsave;
    Xsave[:,0] = X.reshape(Nvars);
    Vsave[:,0] = V.reshape(Nvars);
    for kk in range(Nsteps):
        dt = tspan[kk+1]-tspan[kk];
        X += dt*dXdt(X,V);
        V += dt*dVdt(X,V);
        Xsave[:,1+kk] = X.reshape(Nvars);
        Vsave[:,1+kk] = V.reshape(Nvars);
    return Xsave,Vsave;