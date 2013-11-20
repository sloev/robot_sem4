'''
Created on 11/11/2013

@author: Daniel Machon
'''


''''''''''''''''''''''''''''''''''''''
'    Test code for turn calibration   '
'    Did not work!                    '
''''''''''''''''''''''''''''''''''''''


from IR_Sensors.IR_Sensors_Controller import IR_Sensors_Controller
import math

class ChaosTest():
    
     
    def __init__(self):
        self.sensor = IR_Sensors_Controller(0x20)
        
    
    
    '''
        Do cool stuff
    '''
    def __call__(self):
        sample = self.sensor.multiChannelReadCm([0x08, 0x09, 0x0A], 1)
        sample = sample
        angles = self.calcAngles(sample)
        print angles
        self.checkAngles(angles)
        
       
    '''
        Calculate angle A and B in the triangle created by the robot + 
        left- and front sensor point of reflection
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
        if(60 < angles[0] < 65):
            if(25 < angles[1] < 28):
                print "Facing the right way"
                return 1
        elif(65 < angles[0]):
            print "Facing the right way, slightly more left"
            return 1
        else:
            print "We are off course!"
            return 0
       
       
def main():
    test = ChaosTest()
    test()
    

if __name__ == '__main__':
    main() 
        
        
           