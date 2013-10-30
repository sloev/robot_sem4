'''
Created on Oct 1, 2013

@author: Daniel Machon
'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' This class is a decorator. Its purpose is to return the status   '
' of the stepper motor in printed text. The decorator takes the    '
' getFullStatus1 method, decorates it, and prints the result in a  '
' more understandable way.                                         '
'                                                                  '
' The decorator can be used on the getFullStatus2 method, by using ' 
' the following syntax:                                            '
'                                                                  '
'@TMCStatus222                                                     '
'getFullStatus1()                                                  '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#import smbus
import logging
import os

class TMC222Status(object):

    '''Constructor'''    
    def __init__(self, f):
        try:
            os.remove("/home/pi/robot_sem4/robot.log")
        except OSError:
            pass
        
        self.logger = logging.getLogger('tmc222status')
        self.logger.setLevel(logging.INFO)
        
        fh = logging.FileHandler('tmc222status.log')
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s/%(name)s/%(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
            
        self.f = f
 #       self.bus = smbus.SMBus(1)
        self.logger = logging.getLogger("robot.TMC222Status")
        self.logger.info("TMC222Status Decorator initialized!")
        self.logger.info("Decorating function " + self.f.__name__ + "\n")
        self.setData(f)

    '''Called after the class is instantiated
       Makes the object callable'''        
    def __call__(self):
        self.getMotorStatus(self.left)
        self.getMotorStatus(self.right)
        
        
    def getMotorStatus(self, data):
        string =""
        string += "|"+str(len(self.data)) + " bytes received from slave located at "+str(data[0])+"|"+"\n"
        string += "|Bytes read from register " + str(hex(data[1])) +"|"+"\n"
        string += "|IRun is " + str((data[2] & 0xF0) >> 4) + " " + "and IHold is " + str(data[1] & 0x0F)+"|"+"\t"
        string +=  "|VMax is " + str((data[3] & 0xF0) >> 4) + " " + "and VMin is " + str(data[3] & 0x0F)+"|"+""
        self.logger.info(string)
        self.getStat1(data[4])
        self.getStat2(data[5])
        self.getStat3(data[6])
        
        
        
    '''Retrieve data from the original function'''    
    def setData(self, f):
        self.data = f(self)
        self.left = self.data[0]
        self.right = self.data[1]
        
        
     
    '''Manipulate data from the stat1 byte'''    
    def getStat1(self, byte):
        string = ""
        data = byte
        accShape = (data >> (8-1)) & 1
        stepMode = (data >> 7-1) & 11
        shaft = (data >> 5-1) & 1
        ACC = (data >> 1-1) & 1111
        
        if(accShape==0):
            string += "|Robot is accelerating|"+"\t"
        else: 
            string +="|Robot is decelerating|"+"\t"
            
        if(stepMode==00):
            string += "|Stepmode is 1/2 steps|"+"\t"
        elif(stepMode==01):
            string += "|Stepmode is 1/4 steps|"+"\t"
        elif(stepMode==10):
            string += "|Stepmode is 1/8 steps|"+"\t"
        elif(stepMode==11):
            string += "|Stepmode is 1/16 steps|"+"\t"    
        if(shaft==0):
            string += "|Robot is moving forward|"+"\n"
        else:
            string += "|Robot is moving backwards|"+"\n"
            
        self.logger.info(string)
        
            
    '''Manipulate data from the stat2 byte'''        
    def getStat2(self, byte):
        string = ""
        data = byte
        vddReset = (data >> (8-1)) & 1
        stepLoss = (data >> (7-1)) & 1
        EIDef = (data >> (6-1)) & 1
        UV2 = (data >> (5-1)) & 1
        TSD = (data >> (4-1)) & 1
        TW = (data >> (3-1)) & 1
        Tinfo = (data >> (2-1)) & 11
        
        if(vddReset==1):
            string += "|VdReset=1|"+"\t"
        else:
            string += "|VddReset=0|"+"\t"
        if(stepLoss==1):
            string += "|Steploss detected!|"+"\t"
        else:
            string += "|No steploss|"+"\t"
        if(EIDef==1):
            string += "|Electrical defect detected!|"+"\n"
        else:
            string += "|No electrical defect|"+"\n"
        if(UV2==1):
            string += "|Under voltage detected!|"+"\t"
        else:
            string += "|Voltage level OK|"+"\t"
        if(TSD==1):
            string += "|Temperature warning! (Above 155)|"+"\t"
        else:
            if(TW==1):
                string += "|Temprature warning (above 145)|"+"\n"
            else:
                string+= "|Temperature OK|"+"\n"
        if(Tinfo==0):
            string += "|Chip temperature is Normal|"+"\t"
        elif(Tinfo==1):
            string += "|Chip temperature is low (warning)|"+"\t"
        elif(Tinfo==2):
            string += "|Chip temperature is high (warning)|"+"\t"
        elif(Tinfo==3):
            string += "|Chip temperature TOO HIGH (shutdown)|"+"\n"
        
        self.logger.info(string)   
            
        
                       
        
    '''Manipulate data from the stat3 byte'''    
    def getStat3(self, byte):
        string = ""
        data = byte
        motion = (data >> (6-1)) & 1
        ESW = (data >> (5-1)) & 1
        OVC1 = (data >> (4-1)) & 1
        OVC2 = (data >> (3-1)) & 1
        CPFail = (data >> (1-1)) & 1
        
        if(motion==0):
            string+= "|Robot has reached its destination!|"+"\t"
        elif(motion==1):
            string+= "|Positive Acceleration; Velocity > 0"+"\t"
        elif(motion==2):
            string+= "|Negative Acceleration; Velocity > 0|"
        elif(motion==3):
            string+= "|Acceleration = 0 Velocity = Max Velocity|"
        elif(motion==4):
            string+= "|Actual Position /= Target Position; Velocity = 0|"
        elif(motion==5):
            string+= "|Positive Acceleration; Velocity < 0|"
        elif(motion==6):
            string+= "|Positive Acceleration; Velocity < 0|"
        elif(motion==7):
            string+= "|Acceleration = 0 Velocity = maximum neg. Velocity|"
        if(ESW==1):
            string+= "|External switch open|"+"\n"
        else:
            string+= "|External switch closed|"+"\n"
        if(OVC1==1):
            string+= "|Over current in coil#1|"+"\t"
        else:
            string+= "|Coil#1 OK|"+"\t"
        if(OVC2==1):
            string+= "|Over current in coil#2|"+"\t"
        else:
            string+= "|Coil#2 OK|"+"\t"
        if(CPFail==1):
            string+= "|Charge pump failure|"+"\n"
        else:
            string+= "|Charge pump OK|"+"\n"
            
        self.logger.info(string)
        
        
'''Example of use'''        
@TMC222Status
def getFullStatus1(self):
    r = [[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0F, 0xFF, 0xFF, 0xFF],[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0F, 0xFF, 0xFF, 0xFF]]
    return r
        
def main():      
    getFullStatus1()
        
if __name__== '__main__':
    main()        
