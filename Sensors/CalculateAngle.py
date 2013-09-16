'''
Created on 15/09/2013

@author: Daniel Machon
'''

#!/usr/bin/python

import math

class Calculations:


    #Constructor
    def __init__(self):
        pass

    def calcAngle(self,x1, y1, x2, y2, Rad):                    #Rad=1 for radians
        D = 5
        alphaLeft = math.atan(y1/x1)                        #Radians
        alphaRight = math.atan(y2/x2)                        #Radians
        arcLengthLeft = math.fabs((x1/y1)/math.sin(alphaLeft));
        arcLengthRight = math.fabs((x2/y2)/math.sin(alphaRight));
        angleY = math.fabs(alphaLeft - alphaRight);

        thetaRad = ((math.sqrt(math.pow(arcLengthLeft, 2)+            #Radians
        math.pow(arcLengthRight, 2)-(2*math.cos(angleY)*arcLengthLeft*
        arcLengthRight)))/D)*math.fabs(y2-y1);

        thetaDeg = math.degrees(thetaRad)                    #Convert to degrees

        if(Rad):
            print(str(thetaRad))
        else:
            print(str(thetaDeg))

def main(): 
 
    app = Calculations()
    app.calcAngle(1,1,1,2,1)
    

if __name__ == '__main__':
    main()