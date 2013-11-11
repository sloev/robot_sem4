'''
Created on 11/11/2013

@author: Daniel Machon
'''

from IR_Sensors import IR_Sensors_Controller
import math

class ChaosTest(object):
    
     


    def __init__(self):
        #self.sensor = IR_Sensors_Controller()
        pass
    
    
    '''
        Do cool stuff
    '''
    def __call__(self, testSample):
        #sample = self.sensor.multiChannelReadCm([0x08, 0x09, 0x0A], 1)
        sample = testSample
        angles = self.calcAngles(sample)
        print angles
        self.checkAngles(angles)
        
       
    '''
        Calculate angle A and B in the triangle created by left and front sensor
    '''
    def calcAngles(self, sample):
        c = math.sqrt(math.pow(sample[0], 2) + math.pow(sample[2], 2))
        A = math.degrees(math.acos(sample[0]/c))
        B = 180 - (90+A)
        return [A, B]
    
    
    '''
        Check if the robot is placed in the correct angle
    '''
    def checkAngles(self, angles):
        if(60 < angles[0] < 70):
            if(25 < angles[1] < 30):
                print "Facing the right way"
                return 1
        else:
            print "We are off course!"
            return 0
       
       
def main():
    test = ChaosTest()
    test([15,0,30])
    test([19,0,29])
    test([10,0,30])
    test([15,0,15])
    

if __name__ == '__main__':
    main() 
        
        
        
        
        