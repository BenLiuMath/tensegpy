import numpy as np
# Functions to produces matrices that perform rotations in three dimensions.
def rotZ(th):
    c = np.cos(th);
    s = np.sin(th);
    A = np.array([[c,-s,0],[s,c,0],[0,0,1]]);
    return A;
def rotX(th):
    c = np.cos(th);
    s = np.sin(th);
    A = np.array([[1,0,0],[0,c,-s],[0,s,c]]);
    return A;
def rotY(th):
    c = np.cos(th);
    s = np.sin(th);
    A = np.array([[c,0,-s],[0,1,0],[s,0,c]]);
    return A;