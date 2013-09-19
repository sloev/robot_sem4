'''
Created on Sep 11, 2013

@author: johannes
@review: johannes, benjamin
'''
import MouseInput
from CalculateAngle import Calculations


class MyClass(object):
    '''
    classdocs
    '''
    miceSensors = MouseInput()
    calculator=Calculations()

    def __init__(self):
        global calculator
        '''
        Constructor
        '''
        
        #miceSensors.update()
        angLen=calculator.calcAngle()
        angle=angLen()[0]
        length=angLen()[1]
        pass
    
    def computeAngle(self):
        