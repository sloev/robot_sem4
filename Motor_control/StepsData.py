'''
Created on Nov 7, 2013

@author: johannes
'''
import math
class StepsData():
    '''
    classdocs
    '''


    def __init__(self,stepMode):
        self.stepMode=stepMode
        '''
        Constructor
        '''
        self.stepsPrCm=[0,0,0,0]
        self.stepsPrRadians=[0,0,0,0]
        self.stepsPr90=[0,0,0,0]
        self.stepsPr180=[0,0,0,0]
        
        '1/8 stepmode'
        self.stepsPrCm[2]=177
        self.stepsPrRadians[2]=808.5071
        self.stepsPr90[2]=int(self.stepsPrRadians*(math.pi/2))
        self.stepsPr180[2]=int(self.stepsPrRadians*math.pi)
        
        
    def radiansToSteps(self,radians):
        return int(self.stepsPrRadians[self.stepMode]*radians)
    
    def stepsToCm(self,steps):
        return steps/self.stepsPrcm[self.stepMode]
    
    def cmToSteps(self,cm):
        return int(self.stepsPrCm[self.stepMode]*cm)
    
    def getStepsPr90(self):
        return self.stepsPr90[self.stepMode]
    
    def getStepsPr180(self):
        return self.stepsPr180[self.stepMode]        
        

        
    