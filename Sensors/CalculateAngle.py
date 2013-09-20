'''
Created on 15/09/2013

@author: Daniel Machon
@review: benjamin, johannes
'''

#!/usr/bin/python

import math
from numpy import array
from LookUpTable import LookUpTable
from Mouse import Mouse
delta = array([[0,0],[0,0]])
lookupTable=LookUpTable()   

class Calculations:
    

    #Constructor
    def __init__(self):
        pass
    

    def calcAngle(self,newDelta):                    
        delta=newDelta
        
        D = 5
        
        mus1=lookupTable.getAngLen(delta[0][0], delta[0][1])
        print (mus1.toString)

        mus2=lookupTable.getAngLen(delta[1][0], delta[1][1])
        angleY = math.fabs(mus1[0] - mus2[0] )

        thetaRad = ((
                     math.sqrt(
                               math.pow(mus1[1], 2) +
                               math.pow(mus2[1], 2) -
                               (2* lookupTable.getCos(angleY) * mus1[1]*mus2[1]))
                     )/D) * math.fabs(delta[0][1] - delta[1][1])
                     
        print "angle="+thetaRad +" len="+ math.fabs((mus1[1]+mus2[1])/2)
                     
        #return thetaRad , math.fabs((mus1()[1]+mus2()[1])/2)
            
def main(): 
 
    app = Calculations()
    app.calcAngle(1,1,1,2,1)
    

if __name__ == '__main__':
    main()