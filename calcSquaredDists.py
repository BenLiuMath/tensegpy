import numpy as np
def calcSquaredDists(nodes):
    squareddists = np.zeros(nodes.shape[0]);
    for dim in range(3):
        squareddists = squareddists + (np.atleast_2d(nodes[:,dim]).T - nodes[:,dim])**2.;
    return squareddists;