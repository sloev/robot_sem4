'''
Created on Oct 2, 2013

@author: Daniel Machon
'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' This class is a decorator. Its purpose is to return the position '
' status of the stepper motor in printed text. The decorator takes '
' the getFullStatus2 method, decorates it, and prints the result in' 
' a more understandable way.                                       '
'                                                                  '
' The decorator can be used on the getFullStatus1 method, by using ' 
' the following syntax:                                            '
'                                                                  '
'@TMCStatus222                                                     '
'getFullStatus1()                                                  '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


import smbus
import logging

class PositionStatus():
   

    'Constructor'
    def __init__(self, f):
        self.bus = smbus.SMBus(1)
        self.logger = logging.getLogger("robot.PosotionStatus")
        self.setData(f)
     
    'Makes the object callable'    
    def __call__(self):
        print self.getActPos()
        print self.getTagPos()

    'Fetch data from original function'    
    def setData(self, f):
        self.data = f(self)
        self.actPos1 = self.data[2]
        self.actPos2 = self.data[3]
        self.tagPos1 = self.data[4]
        self.tagPos2 = self.data[5]
     
    'Convert actual position to decimal number'    
    def getActPos(self):
        return "Actual position is: " + str((self.actPos1<<8) | self.actPos2)
    
    'Convert target position to decimal number'
    def getTagPos(self):
        return "Target position is: " + str((self.tagPos1<<8) | self.tagPos2)
 
'Test function' 
@PositionStatus 
def getFullStatus2(self):
    r = [0x00, 0x00, 0x02, 0x0F, 0xFF, 0xFF]
    return r
    
def main():
    getFullStatus2()
    
    
if __name__ == '__main__':
    main()
       
        