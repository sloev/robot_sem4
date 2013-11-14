'''
Created on 14/11/2013

@author: Daniel Machon
'''

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This module is used to calibrate the robot while making a turn.       '
It's a two step calibration: one when initializing a turn, and one    '     
when a 90 turn around its own axis has been made.                     '
                                                                      '
        A successfull calibration will result in the robot facing     '
        parallel with the side wall it wants to move along when       '
        entering a turn.                                              '
        If no side walls are available when ending a turn, a          '    
        succesfull turn is when the robot is creating a 90 degree     ' 
        angle between its center point and the back wall.             '
                                                                      '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


'''
Definitions
'''
Vin1                    =   0x08
Vin2                    =   0x09
Vin3                    =   0x0A 

leftTurn                =   [0, 1, 1]
rightTurn               =   [1, 0, 1]
deadEnd                 =   [1, 1, 0]
dilemmaFR               =   [1, 0, 0]
dilemmaFL               =   [0, 1 ,0]


'''
Imports
'''

from Motor_control.DualMotorController import DualMotorController
from IR_Sensors.IR_Sensors_Controller import IR_Sensors_Controller 


class Calibrate():
    
    walls = [0, 0, 0]
    
    def __init__(self):
        self.sensors = IR_Sensors_Controller(0x20)
        self.motors = DualMotorController(0x60, 0x61)
        self.motors.hardStop()
        self.motors.getFullStatus1()
        self.motors.setOtpParam()
        self.motors.setMotorParams(1, 0, 1, 1)
    
    def __call__(self, walls):
        channels = self.checkTurnConditions(walls)
        self.initializeTurn(channels)
    
    def checkTurnConditions(self, walls):         
        if(walls==leftTurn):                     
            channels = [Vin2, Vin3]
        elif(walls==rightTurn):                   
            channels = [Vin1, Vin3]
        elif(walls==deadEnd):
            channels = [Vin1, Vin2]
        elif(walls==dilemmaFR):
            channels = [Vin1]
        elif(walls==dilemmaFL):
            channels = [Vin2]
        return channels
            
    
    def initializeTurn(self, channels):
        lastSample = [65, 65]
        sample = self.sensors.multiChannelReadCm(channels, 3)
        print sample
        
        while(self.checkSample(sample, lastSample)):
            self.motors.setMotorParams(0, 0, 1, 1)
            self.motors.setPosition(32768, 32768)
            lastSample = sample
            sample = self.sensors.multiChannelReadCm(channels, 5)
            print sample
        
        self.motors.hardStop()
        print 'Done calibrating start of turn'
            
        
    def checkSample(self, sample, lastSample):
        print "lastSample = " + str(lastSample)
        print "newSample = " + str(sample)
        if(sample[0] < lastSample[0] or sample[1] < lastSample[1]):
            print 'New sample was smaller'
            return 1
        else:
            print 'New sample was larger'
            return  0
    
    
    def turn(self):
        pass
    
    def endTurn(self):
        pass
    
    
    
def main():
    rightTest = Calibrate()
    rightTest([1, 0, 1])

if __name__ == '__main__':
    main()
    