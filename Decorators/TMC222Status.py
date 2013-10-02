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
'getFullStatus2()                                                  '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class TMC222Status(object):

    def __init__(self, f):
        print "Daniel Machon's awesome decorator initialized!"
        self.f = f
        self.setData(f)
        print "Decorating function " + self.f.__name__


    def __call__(self):
        print str(len(self.data)) + " bytes received"
        print "Slave located at " + self.slaveAdd
        print "Bytes read from register " + self.add
        print "IRun is " + str((self.iRun_iHold & 0xF0) >> 4) + " " + "and IHold is " + str(self.iRun_iHold & 0x0F)
        print "VMax is " + str((self.vMax_vMin & 0xF0) >> 4) + " " + "and VMin is " + str(self.vMax_vMin & 0x0F)
        self.getStat1(self.stat1)
        
        
        
        
    def setData(self, f):
        self.data = f(self)
        self.slaveAdd = str(hex(self.data[0]))
        self.add = str(hex(self.data[1]))
        self.iRun_iHold = self.data[2]
        self.vMax_vMin = self.data[3]
        self.stat1 = self.data[4]
        self.stat2 = str(self.data[5])
        self.stat3 = str(self.data[6])
        self.NA1 = str(self.data[7])
        self.NA2 = str(self.data[8])
        
    def getStat1(self, byte):
        data = byte
        self.accShape = (data >> (1-1)) & 1
        self.stepMode = (data >> 3) & 11
        self.shaft = (data >> 4) & 1
        self.ACC = (data >> 7) & 1111
        
        if(self.accShape==0):
            print "Robot is accelerating"
        else: 
            print "Robot is decelerating"
            
        if(self.stepMode==00):
            print "Stepmode is 1/2 steps"
        elif(self.stepMode==01):
            print "Stepmode is 1/4 steps"
        elif(self.stepMode==10):
            print "Stepmode is 1/8 steps"
        elif(self.stepMode==11):
            print "Stepmode is 1/16 steps"    
        if(self.shaft==0):
            print "Robot is moving forward"
        else:
            print "Robot is moving backwards"
        
            
            
    def getStat2(self, byte):
        self.data = byte
        self.vddReset = (self.data >> 1) & 1
        self.stepLoss = (self.data >> 2) & 1
        self.EIDef = (self.data >> 3) & 1
        self.UV2 = (self.data >> 3) & 1
        self.TSD = (self.data >> 5) & 1
        self.TW = (self.data >> 6) & 1
        self.Tinfo = (self.data >> 7) & 1
        
        
    def getStat3(self, byte):
        self.data = byte
        self.motion = (self.data >> 3) & 111
        self.ESW = (self.data >> 4) & 1
        self.OVC1 = (self.data >> 5) & 1
        self.OVC2 = (self.data >> 6) & 1
        self.CPFail = (self.data >> 7) & 1
        
        
@TMC222Status
def getFullStatus2(self):
    r = [0x55, 0xAA, 0xBB, 0xCC, 0x00, 0x43, 0x62, 0x11, 0x99]
    return r
   
        
def main():      
    getFullStatus2()
        
if __name__== '__main__':
    main()        