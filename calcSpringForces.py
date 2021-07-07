import numpy as np
from calcSquaredDists import *
def calcSpringForces(nodes,springList):
    dists = np.sqrt(calcSquaredDists(nodes));
    
    Forces = np.zeros(nodes.shape);
    for spring in springList:
        v1 = int(spring[0]);
        v2 = int(spring[1]);
        restleng = spring[2];
        stiffness = spring[3];
        
        separation = dists[v1][v2];
        displacementLeng = separation - restleng;
        
        displacementVector = nodes[v2,:]-nodes[v1,:];
        displacementVector = displacementVector / np.dot(displacementVector,displacementVector);
        F = -stiffness*displacementLeng * displacementVector;
        Forces[v2,:] += F;
        Forces[v1,:] -= F;
    return Forces;