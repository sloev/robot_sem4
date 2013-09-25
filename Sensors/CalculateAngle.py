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

class Calculations:
    

    #Constructor
    def __init__(self):
        self.delta = array([[0,0],[0,0]])
        self.lookupTable=LookUpTable()   
        pass
    

    def calcAngle(self,newDelta):                    
        delta=newDelta
        
        D = 5
        
        mus1=self.lookupTable.getAngLen(delta[0][0], delta[0][1])
        mus2=self.lookupTable.getAngLen(delta[1][0], delta[1][1])

        #if isinstance(mus1, Mouse) and isinstance(mus2, Mouse):
        try:
            print("both mice are mice") 
            angleY = math.fabs(mus1.getAngle() - mus2.getAngle() )
 
            thetaRad = ((
                         math.sqrt(
                                   math.pow(mus1.getLength(), 2) +
                                   math.pow(mus2.getLength(), 2) -
                                   (2* self.lookupTable.getCos(angleY) * mus1.getLength()*mus2.getLength()))
                     )/D) * math.fabs(delta[0][1] - delta[1][1])
                      
            print "angle="+str(thetaRad) +" len="+ str(math.fabs((mus1.getLength()+mus2.getLength())/2))
                     
        #else:
        except:
            print("both mice are not mice")
            
def main(): 
 
    app = Calculations()
    app.calcAngle(1,1,1,2,1)
    

if __name__ == '__main__':
    main()