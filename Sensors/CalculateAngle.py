'''
Created on 15/09/2013

@author: Daniel Machon
@review: benjamin, johannes
'''

#!/usr/bin/python

import math
from numpy import array
from LookUpTable import LookUpTable


class Calculations:
    
    delta = array([[0,0],[0,0]])
    lookupTable=LookUpTable()   
    #Constructor
    def __init__(self):
        global delta,lookupTable
        pass
    

    def calcAngle(self):                    #Rad=1 for radians
        D = 5
        
        mus1=lookupTable.getAngLen(delta[0][0], delta[0][1])
        mus2=lookupTable.getAngLen(delta[1][0], delta[1][1])
        
        angleY = math.fabs(mus1()[0] - mus2()[0] )

        thetaRad = ((
                     math.sqrt(
                               math.pow(mus1()[1], 2) +
                               math.pow(mus2()[1], 2) -
                               (2*lookupTable.getCos(angleY) * mus1()[1]*mus2()[1]))
                     )/D) * math.fabs(delta[0][1]-delta[1][1])
                     
        return thetaRad , math.fabs((mus1()[1]+mus2()[1])/2)
            
    def updateMatrix(self, newDelta):
        delta=newDelta
        pass
    
def main(): 
 
    app = Calculations()
    app.calcAngle(1,1,1,2,1)
    

if __name__ == '__main__':
    main()