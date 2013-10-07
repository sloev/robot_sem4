'''
Created on Oct 1, 2013

@author: Daniel Machon
'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' This class is a decorator. Its purpose is to return the status   '
' of the stepper motor in printed text. The decorator takes the    '
' getFullStatus2 method, decorates it, and prints the result in a  '
' more understandable way.                                         '
'                                                                  '
' The decorator can be used on the getFullStatus2 method, by using ' 
' the following syntax:                                            '
'                                                                  '
'@TMCStatus222                                                     '
'getFullStatus1()                                                  '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import smbus

class TMC222Status(object):

    '''Constructor'''    
    def __init__(self, f):
        print "\n"
        print "Daniel Machon's awesome decorator initialized!"
        self.f = f
        self.setData(f)
        print "Decorating function " + self.f.__name__ + "\n"


    '''Called after the class is instantiated'''        
    def __call__(self):
        string =""
        string += "|"+str(len(self.data)) + " bytes received from slave located at "+self.slaveAdd+"|"+"\n"
        string += "|Bytes read from register " + self.add+"|"+"\n"
        string += "|IRun is " + str((self.iRun_iHold & 0xF0) >> 4) + " " + "and IHold is " + str(self.iRun_iHold & 0x0F)+"|"+"\t"
        string +=  "|VMax is " + str((self.vMax_vMin & 0xF0) >> 4) + " " + "and VMin is " + str(self.vMax_vMin & 0x0F)+"|"+""
        print string
        self.getStat1(self.stat1)
        self.getStat2(self.stat2)
        self.getStat3(self.stat3)
        
        
        
    '''Retrieve data from the original function'''    
    def setData(self, f):
        self.data = f(self)
        self.slaveAdd = str(hex(self.data[0]))
        self.add = str(hex(self.data[1]))
        self.iRun_iHold = self.data[2]
        self.vMax_vMin = self.data[3]
        self.stat1 = self.data[4]
        self.stat2 = self.data[5]
        self.stat3 = self.data[6]
        self.NA1 = str(self.data[7])
        self.NA2 = str(self.data[8])
        
     
    '''Manipulate data from the stat1 byte'''    
    def getStat1(self, byte):
        string = ""
        data = byte
        self.accShape = (data >> (8-1)) & 1
        self.stepMode = (data >> 7-1) & 11
        self.shaft = (data >> 5-1) & 1
        self.ACC = (data >> 1-1) & 1111
        
        if(self.accShape==0):
            string += "|Robot is accelerating|"+"\t"
        else: 
            string +="|Robot is decelerating|"+"\t"
            
        if(self.stepMode==00):
            string += "|Stepmode is 1/2 steps|"+"\t"
        elif(self.stepMode==01):
            string += "|Stepmode is 1/4 steps|"+"\t"
        elif(self.stepMode==10):
            string += "|Stepmode is 1/8 steps|"+"\t"
        elif(self.stepMode==11):
            string += "|Stepmode is 1/16 steps|"+"\t"    
        if(self.shaft==0):
            string += "|Robot is moving forward|"+"\n"
        else:
            string += "|Robot is moving backwards|"+"\n"
            
        print string
        
            
    '''Manipulate data from the stat2 byte'''        
    def getStat2(self, byte):
        string = ""
        self.data = byte
        self.vddReset = (self.data >> (8-1)) & 1
        self.stepLoss = (self.data >> (7-1)) & 1
        self.EIDef = (self.data >> (6-1)) & 1
        self.UV2 = (self.data >> (5-1)) & 1
        self.TSD = (self.data >> (4-1)) & 1
        self.TW = (self.data >> (3-1)) & 1
        self.Tinfo = (self.data >> (2-1)) & 11
        
        if(self.vddReset==1):
            string += "|VdReset=1|"+"\t"
        else:
            string += "|VddReset=0|"+"\t"
        if(self.stepLoss==1):
            string += "|Steploss detected!|"+"\t"
        else:
            string += "|No steploss|"+"\t"
        if(self.EIDef==1):
            string += "|Electrical defect detected!|"+"\n"
        else:
            string += "|No electrical defect|"+"\n"
        if(self.UV2==1):
            string += "|Under voltage detected!|"+"\t"
        else:
            string += "|Voltage level OK|"+"\t"
        if(self.TSD==1):
            string += "|Temperature warning! (Above 155)|"+"\t"
        else:
            if(self.TW==1):
                string += "|Temprature warning (above 145)|"+"\n"
            else:
                string+= "|Temperature OK|"+"\n"
        if(self.Tinfo==0):
            string += "|Chip temperature is Normal|"+"\t"
        elif(self.Tinfo==1):
            string += "|Chip temperature is low (warning)|"+"\t"
        elif(self.Tinfo==2):
            string += "|Chip temperature is high (warning)|"+"\t"
        elif(self.Tinfo==3):
            string += "|Chip temperature TOO HIGH (shutdown)|"+"\n"
        
        print string    
            
        
                       
        
    '''Manipulate data from the stat3 byte'''    
    def getStat3(self, byte):
        string = ""
        self.data = byte
        self.motion = (self.data >> (6-1)) & 1
        self.ESW = (self.data >> (5-1)) & 1
        self.OVC1 = (self.data >> (4-1)) & 1
        self.OVC2 = (self.data >> (3-1)) & 1
        self.CPFail = (self.data >> (1-1)) & 1
        
        if(self.motion==0):
            string+= "|Robot has reached its destination!|"+"\t"
        elif(self.motion==1):
            string+= "|Positive Acceleration; Velocity > 0"+"\t"
        elif(self.motion==2):
            string+= "|Negative Acceleration; Velocity > 0|"
        elif(self.motion==3):
            string+= "|Acceleration = 0 Velocity = Max Velocity|"
        elif(self.motion==4):
            string+= "|Actual Position /= Target Position; Velocity = 0|"
        elif(self.motion==5):
            string+= "|Positive Acceleration; Velocity < 0|"
        elif(self.motion==6):
            string+= "|Positive Acceleration; Velocity < 0|"
        elif(self.motion==7):
            string+= "|Acceleration = 0 Velocity = maximum neg. Velocity|"
        if(self.ESW==1):
            string+= "|External switch open|"+"\n"
        else:
            string+= "|External switch closed|"+"\n"
        if(self.OVC1==1):
            string+= "|Over current in coil#1|"+"\t"
        else:
            string+= "|Coil#1 OK|"+"\t"
        if(self.OVC2==1):
            string+= "|Over current in coil#2|"+"\t"
        else:
            string+= "|Coil#2 OK|"+"\t"
        if(self.CPFail==1):
            string+= "|Charge pump failure|"+"\n"
        else:
            string+= "|Charge pump OK|"+"\n"
            
        print string
        
        
'''Example of use'''        
@TMC222Status
def getFullStatus1(self):
    r = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0F, 0xFF, 0xFF, 0xFF]
    return r
   
        
def main():      
    getFullStatus1()
        
if __name__== '__main__':
    main()        