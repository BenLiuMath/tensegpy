import numpy as np
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self,pcoords):
        self.coords = pcoords;
        self.idNum = None;
        
    def __str__(self):
        return "vert:"+self.coords.__str__();
    def __repr__(self):
        return self.__str__();
    
class Strut:
    def __init__(self,v1,v2,stiffness=1.0,restLeng=None):
        self.v1 = v1;
        self.v2 = v2;
        self.stiffness = stiffness;
        if restLeng is None:
            self.restLeng = np.sqrt( np.sum((self.v1.coords - self.v2.coords)**2.) );
        else:
            self.restLeng = restLeng;
            
    def getLeng(self):
        return self.restLeng;

class StrutNodeStructure:
    def __init__(self):
        self.verts = [];
        self.struts = [];
        
    def addVerts(self,pcoords):
        vshape = pcoords.shape;
        if vshape[0]==3: # requires reshape
            pcoords = pcoords.T;
            Nverts = vshape[1];
        elif vshape[1]==3:
            Nverts = vshape[0];
        else:
            raise ValueError("Vertices matrix of wrong dimensions!");

        myverts = [];
        for vv in pcoords:
            myverts.append(Vertex(vv));
        self.verts.extend(myverts);
        return myverts;
            
    # pstruts should be a list of lists-of-length-2
    def addStruts(self,*args,**kwargs):
        
        #print(kwargs);
        #
        pstiffness = 1.0;
        if 'stiffness' in kwargs:
            pstiffness = kwargs['stiffness'];
        
        if len(args)==1: # list of struts
            newstruts = [];
            for strutverts in args[0]:
                mystrut = Strut( strutverts[0], strutverts[1], stiffness=pstiffness);
                newstruts.append(mystrut);
            self.struts.extend( newstruts );
            return args[0];
        elif len(args)==2:
            v1s = args[0];
            v2s = args[1];
            if len(v1s)==len(v2s):
                newstruts = [];
                for jj in range(len(v1s)):
                    mystrut = Strut( v1s[jj],v2s[jj], stiffness=pstiffness);
                    newstruts.append( mystrut );
                self.struts.extend(newstruts);
                return newstruts;
            else:
                raise ValueError("Dimension mismatch. Expected lists to be of same length");
        
        
        #self.struts.extend(pstruts);
    
    def getVertsXYZ(self):
        return np.array([v.coords for v in ralph.verts]).T;
    def setVertsXYZ(self,XYZ):
        for jj in np.arange(len(self.verts)):
            self.verts[jj].coords = XYZ[:,jj];
            
    def divulge(self):
        vertNum = 0;
        
        vertArray = np.zeros(shape=(0,3))
        for vert in self.verts:
            vertArray = np.vstack( (vertArray,vert.coords) );
            vert.idNum = vertNum;
            vertNum += 1;
        
        springList = [[strut.v1.idNum, strut.v2.idNum, strut.getLeng(), strut.stiffness] for strut in self.struts];
        springList = np.array(springList);
        
        return vertArray,springList;
        
        
    def plotverts(self,color='k',labelVerts=False):
        allverts = np.array([]).reshape(0,3);
        ax = plt.gca();
        for (jj,vert) in enumerate(self.verts):
            mycoords = vert.coords;
            allverts = np.vstack( (allverts,np.atleast_2d(mycoords)) );
            if labelVerts:
                ax.text(mycoords[0],mycoords[1],mycoords[2],'%d'%jj,color='red');
        plt.plot(allverts[:,0],allverts[:,1],allverts[:,2],'ko');
        
    def plotstruts(self,color='k'):
        for strut in self.struts:
            v1 = strut.v1.coords;
            v2 = strut.v2.coords;
            xyz = np.vstack( (v1,v2) );
            plt.plot(xyz[:,0],xyz[:,1],xyz[:,2],'k',linewidth=np.log10(strut.stiffness+1.0));
    
    def plot(self,color='k',labelVerts=False):
        self.plotverts(color=color,labelVerts=labelVerts);
        self.plotstruts(color=color);
		
def plotSpringMassSystem(verts,springList,detail=0,ax=None):
    verts = verts.reshape( (-1,3) );
    if ax is None:
        ax = plt.gca();
    if detail==0:
        inds1 = springList[:,0].astype('int');
        inds2 = springList[:,1].astype('int');

        mynans = np.full( (springList.shape[0]), float('nan') );

        XX = np.vstack( (verts[inds1,0],verts[inds2,0],mynans) ).T.flatten();
        YY = np.vstack( (verts[inds1,1],verts[inds2,1],mynans) ).T.flatten();
        ZZ = np.vstack( (verts[inds1,2],verts[inds2,2],mynans) ).T.flatten();

        ax.plot(XX,YY,ZZ,'k');
    elif detail==1:
        for spring in springList:
            coords = verts[spring[0:2].astype('int'),:];
            currlen = coords[0,:]-coords[1,:]; currlen = np.sqrt(np.dot(currlen,currlen));
            mylw = np.log10(spring[3]+10.);
            myc = 'g';
            if currlen < spring[2]:
                myc = (0.6,0,0);
            ax.plot(coords[:,0],coords[:,1],coords[:,2],'k',linewidth=mylw,color=myc);