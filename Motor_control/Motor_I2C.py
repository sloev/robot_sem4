'''
Created on Sep 23, 2013

@author: Daniel Machon
'''

'''
Motor commands:        Description:                                        ByteCode:

GetFullStatus1:        Returns complete status of the chip                 0x81 
GetFullStatus2:        Returns actual, target and secure position          0xFC 
GetOTPParam:           Returns OTP parameter                               0x82 
GotoSecurePosition:    Drives motor to secure position                     0x84 
HardStop:              Immediate full stop                                 0x85 
ResetPosition:         Sets actual position to zero                        0x86 
ResetToDefault:        Overwrites the chip RAM with OTP contents           0x87 
RunInit:               Reference Search                                    0x88 
SetMotorParam:         Sets motor parameter                                0x89 
SetOTPParam:           Zaps the OTP memory                                 0x90 
SetPosition:           Programmers a target and secure position            0x8B 
SoftStop:              Motor stopping with deceleration phase              0x8F
'''


''' 
StepMode parameter:         Mode: 
        
00                          Half Stepping 
01                          1/4 Stepping 
10                          1/8 Stepping
11                          1/16 Stepping
'''  


import smbus
import time as time

#Motor commands:        ByteCode:    Description:                                        

cmdGetFullStatus1     = 0x81       # Returns complete status of the chip 
cmdGetFullStatus2     = 0xFC       # Returns actual, target and secure position 
cmdGetOTPParam        = 0x82       # Returns OTP parameter        
cmdGotoSecurePosition = 0x84       # Drives motor to secure position 
cmdHardStop           = 0x85       # Immediate full stop 
cmdResetPosition      = 0x86       # Sets actual position to zero   
cmdResetToDefault     = 0x87       # Overwrites the chip RAM with OTP contents   
cmdRunInit            = 0x88       # Reference Search              
cmdSetMotorParam      = 0x89       # Sets motor parameter      
cmdSetOTPParam        = 0x90       # Zaps the OTP memory    
cmdSetPosition        = 0x8B       # Programmers a target and secure position 
cmdSoftStop           = 0x8F       # Motor stopping with deceleration phase 

class Motor_I2C:
    '''

/    Stepper motor driver module.
    '''


    def __init__(self, devAddress):
        self.devAddress = devAddress
        self.bus = smbus.SMBus(1)
        self.lrun=3
        self.lhold=2
        
        '''Status of circuit and stepper motor'''
    def getFullStatus1(self):
        response = self.bus.read_i2c_block_data(self.devAddress, cmdGetFullStatus1, 11)
        #response1 = self.bus.read_i2c_block_data(self.devAddress, 0x81, 11)
        return response
        
        '''Status of the position of the stepper motor'''
    def getFullStatus2(self):
        response = self.bus.read_i2c_block_data(self.devAddress, cmdGetFullStatus2)
        #response = self.bus.write_byte(self.devAddress, 0xFC)
        return response
        
        '''Read OTP *One-Time Programmable) memory''' 
    def getOTPParam(self):
        response = self.bus.write_byte(self.devAddress, cmdGetOTPParam)
        #response = self.bus.write_byte(self.devAddress, 0x82)
        return response
    
    def goToSecurePosition(self):
        pass
    
    def hardStop(self):
        self.bus.write_byte(self.devAddress, cmdHardStop)
        #self.bus.write_byte(self.devAddress, 0x85)
    
    def resetPosition(self):
        self.bus.write_byte(self.devAddress, cmdResetPosition)
        #self.bus.write_byte(self.devAddress, 0x86)
    
    def resetToDefault(self):
        self.bus.write_byte(self.devAddress, cmdResetToDefault)
        #self.bus.write_byte(self.devAddress, 0x87)
 
    def runInit(self,position1, position2):
        position1=self.toTwoBytes(position1)
        position2=self.toTwoBytes(position2)
        #byteCode = [0xFF, 0xFF, 0x80, 0x00, 0x50, 0xAA, 0x10]
        byteCode = [0xFF, 0xFF, 0x80, position1[0],position1[1],position2[0],position2[1]]              
        self.bus.write_i2c_block_data(self.devAddress, cmdRunInit, byteCode) 
        #self.bus.write_i2c_block_data(self.devAddress, 0x88, byteCode) 
        
        '''Set the stepper motor parameters in the RAM:
          
           Byte 1: 0xFF
           Byte 2: 0xFF
           Byte 3: 7-4=Coil peak current value (Irun), 3-0=Coil hold current value (Ihold) 
           Byte 4: 7-4=Max velocity, 3-0=Min velocity
           Byte 5: 7-5=Secure position, 4=Motion direction, 3-0=Acceleration
           Byte 6: 7-0=Secure position of the stepper motor
           Byte 7: 4=Acceleration shape, 3-2=Stepmode      
        '''          
    def setMotorParam(self,direction, maxVelocity, minVelocity): 
        byte3=self.lrun<<4 | self.lhold<<0
        byte4=minVelocity<<0 | maxVelocity << 4
        byte5=0x88 | direction<<4
        #byteCode = [0xFF, 0xFF, 0x32, 0x32, 0x88, 0x00, 0x08]
        byteCode = [0xFF, 0xFF, byte3, byte4, byte5, 0x00, 0xc]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetMotorParam, byteCode)
        #self.bus.write_i2c_block_data(self.devAddress, 0x89, byteCode)   
    
        '''Drive the motor to a given position relative to 
           the zero position, defined in number of half or micro steps, 
           according to StepMode[1:0] value:
           
           Byte 1: 0xFF
           Byte 2: 0xFF
           Byte 3: 
           Byte 4: 
        ''' 
        
        '''Zap the One-Time Programmable memory'''  
    def setOTPParam(self):
        byteCode = [0xFF, 0xFF, 0xFB, 0xD5]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetOTPParam, byteCode)
        #self.bus.write_i2c_block_data(self.devAddress, 0x90, byteCode)
        
        
        '''Drive the motors to a given position in number of
           steps or microsteps:
        '''   
    def setPosition(self, position):
        position=self.toTwoBytes(position)
        
        byteCode = [0xFF, 0xFF, position[0],position[1]]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetPosition, byteCode)
        #self.bus.write_i2c_block_data(self.devAddress, 0x8B, byteCode)
    
    def softStop(self):
        self.bus.write_byte(self.devAddress, cmdSoftStop)
        #self.bus.write_byte(self.devAddress, 0x8F)
              
    def writeToMotor(self, value):
        self.bus.write_i2c_block_data(self.devAddress, 0x00, 0x00)
    
    def driveAngle(self):
        pass
    
    '''toTwoBytes returns a list with two ints maximum value 255
    '''
    def toTwoBytes(self,temp):
        a,b=divmod(temp,0x100)
        return [a,b]
    
    '''to metoder til at satte torque for drift og stilstand lrun/lhol
    '''
    def setLrun(self,lrun):
        self.lrun=lrun
    
    def setLhold(self,lhold):
        self.lhold=lhold
    
    
def main():
    motor1 = Motor_I2C(0x60)
    motor2 = Motor_I2C(0x61)

#    motor.getFullStatus1()
#    motor.setOTPParam()
#     motor1.resetToDefault()  
#     motor2.resetToDefault()  
#     time.sleep(2)
#     
#     motor1.hardStop()
#     motor2.hardStop()
#     time.sleep(2)
#     
#     motor1.getFullStatus1()
#     motor1.getFullstatus2()
#     
#     time.sleep(1)
#     
#     motor2.getFullStatus1()
#     motor2.getFullstatus2()
#     time.sleep(2)
#         
    motor1.setOTPParam()
    motor2.setOTPParam()
    #time.sleep(2)
    
    motor1.setMotorParam(0,3,2)
    motor2.setMotorParam(1,3,2)
    #time.sleep(2)
    position=1000
    
    returner=motor2.getFullStatus2()
    print("beforeINIT\nintpos="+str(position)+"extpos="+str(int(returner[2]<<8 | returner[3]<<0)))
    
    motor1.runInit(300,600)  
    motor2.runInit(300,600)  
    #time.sleep(2)
    returner=motor2.getFullStatus2()
    print("afterinit\nintpos="+str(position)+"extpos="+str(int(returner[2]<<8 | returner[3]<<0)))
    
    motor1.setPosition(position)
    position=100
    motor2.setPosition(position)
    time.sleep(5)
    
    returner=motor2.getFullStatus2()
    print("aftersetpos\nintpos="+str(position)+"extpos="+str(int(returner[2]<<8 | returner[3]<<0)))
    
    for i in range(0,100):
        returner=motor2.getFullStatus2()
        position+=100
        motor2.setPosition(position)
        print(str(int(returner[0]))+"\t"+str(int(returner[1]))+"\t"+str(int(returner[2]))+"\t"+str(int(returner[3]))+"\t"+str(int(returner[4]))+"\t"+str(int(returner[5]))+"\t"+str(int(returner[6]))+"\t"+str(int(returner[7]))+"\t"+str(int(returner[8])))
        print(hex(returner[0])+"\t"+hex(returner[1])+"\t"+hex(returner[2])+"\t"+hex(returner[3])+"\t"+hex(returner[4])+"\t"+hex(returner[5])+"\t"+hex(returner[6])+"\t"+hex(returner[7])+"\t"+hex(returner[8]))

        time.sleep(0.1)
    
    
   
#    motor.resetToDefault()   
#    motor.hardStop()
#    motor.getFullStatus1()    

if __name__== '__main__':
    main()
       
        
