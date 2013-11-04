'''
Created on Oct 15, 2013

@author: Johannes Jorgensen
'''

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'PID control                                                                                '
'Inspired by:                                                                               ' 
'http://letsmakerobots.com/node/865                                                         '
'                                                                                           ' 
'Uses three sharp ir sensors connected through i2c with ad7998 ad-converter                 '
'and for output it uses two stepper motors                                                  '
'                                                                                           '
'If self.left =0 and self.right=1 it will drive towards the direction of its sensor head    '
'                                                                                           ' 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import logging
import cPickle as pickle
import os.path


Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A

sensorChannels=[Vin1,Vin2,Vin3]

class Pid():

    '''
        Constructor
    '''
    def __init__(self,left,right,ir_sensors, dual_motors):
        self.left=left
        self.right=right
        self.front=2
        
        self.logger = logging.getLogger('robot.pid')
        self.logger.info("Initializing Pid")
        self.ir_sensors=ir_sensors
        self.dual_motors=dual_motors
        self.setPoint=14.9
        self.cmMax=28
        self.cmMin=5
        
        self.lastError=[0,0] #last error 
        self.iError=[0,0]
        
        '''gain factors'''
        self.pGain=[0,0]  #proportional gain factor
        self.dGain=[0,0]  #differential gain factor
        self.iGain=[0,0]  #integral gain factor
        gainFactors=self.unpickleGainFactors()

        if(gainFactors==0):           
            self.logger.info("gainFactors not unpickled")
        else:
            self.pGain=gainFactors[0]
            self.dGain=gainFactors[1]
            self.iGain=gainFactors[2]
            self.logger.info("gainFactors loaded from pickle")
        self.logger.info("Initializing Pid DONE")
        
    def getMinMaxSetpoint(self):
        return [self.cmMin,self.cmMax,self.setPoint]
        
    '''
        Resets the integral error
    '''
    def reset(self):
        self.logger.info("/resetting ierrors")
        self.iError=[0,0]
        self.lastError=[0,0]
        
    '''
        PID controller:
        calculates errors according to setpoint
        sends calculated new velocities to motors
    '''    
    def doPid(self,sample):
        self.sample=sample
        self.logger.info("Doing pid")

        pError=[self.setPoint-self.sample[self.right],self.setPoint-self.sample[self.left]] 
        #print("currentError:"+str(currentError))            
        
        dError=[pError[self.left]-self.lastError[self.left],pError[self.right]-self.lastError[self.right]]
        
        controlValues=[self.computeControlValues(self.left,pError,dError),self.computeControlValues(self.right,pError,dError)]
        
        self.lastError=pError
        self.iError=[pError[self.left]+self.iError[self.left] , pError[self.right]+self.iError[self.right]]
        
        self.setMotors(controlValues)
        
        self.logger.info("left/pError/%f",pError[self.left])
        self.logger.info("right/pError/%f",pError[self.right])
        
        self.logger.info("left/iError/%f",self.iError[self.left])
        self.logger.info("right/iError/%f",self.iError[self.right])
        
        self.logger.info("left/dError/%f",dError[self.left])
        self.logger.info("right/dError/%f",dError[self.right])
 
        self.logger.info("Doing pid DONE")    
        
    '''
        Set the motor parameters
    '''
    def setMotors(self,controlValues):

#         if(controlValues[self.left]>=5 and self.sample[self.front] > self.setPoint*0.8):
#             self.dual_motors.setMotorParams(self.left, self.right, 3, controlValues[self.right])
#             self.logger.info("/setMotors/frontSensorLarge/"+str(controlValues))
#             
#         elif(controlValues[self.right]>=5 and self.sample[self.front] > self.setPoint*0.8):
#             self.dual_motors.setMotorParams(self.left, self.right, controlValues[self.left], 3)
#             self.logger.info("/setMotors/frontSensorLarge/"+str(controlValues))
#             
#         else:
#             self.dual_motors.setMotorParams(self.left, self.right, controlValues[self.left], controlValues[self.right])
#             self.logger.info("/setMotors/frontSensorIgnored/"+str(controlValues))
        self.dual_motors.setMotorParams(self.left, self.right, controlValues[self.left], controlValues[self.right])
        self.logger.info("setMotors/frontSensorIgnored/"+str(controlValues))

        #print("control values="+str(controlValues))
        
    '''
        Tunes the proportional gain
    '''
    def pTune(self,pGain):
        if(pGain[self.left]==0):
            self.pGain=[self.pGain[self.left],pGain[self.right]]
        elif(pGain[self.right]==0):
            self.pGain=[pGain[self.left],self.pGain[self.right]]
        else:
            self.pGain=pGain
        self.logger.info("pTune new pGain:"+str(self.pGain))

            
    '''
        Tunes the derivative gain
    '''
    def dTune(self,dGain):
        if(dGain[self.left]==0):
            self.dGain=[self.dGain[self.left],dGain[self.right]]
        elif(dGain[self.right]==0):
            self.dGain=[dGain[self.left],self.dGain[self.right]]
        else:
            self.dGain=dGain
        self.logger.info("pTune new dGain:"+str(self.dGain))

      
    '''
        Tunes the integral gain
    '''
    def iTune(self,iGain):
        if(iGain[self.left]==0):
            self.iGain=[self.iGain[self.left],iGain[self.right]]
        elif(iGain[self.right]==0):
            self.iGain=[iGain[self.left],self.iGain[self.right]]
        else:
            self.iGain=iGain
        self.logger.info("pTune new iGain:"+str(self.iGain))
        
        
    '''
        Fetch current gain factors
    '''
    def getGainFactors(self):
        return [self.pGain,self.iGain,self.dGain]

            
    '''
        Computes the overall error using the PID controller algorithm
    '''
    def computeControlValues(self,wheel,pError,dError):
        pe=self.pGain[wheel]*pError[wheel]
        ie=self.iGain[wheel]*self.iError[wheel]
        de=self.dGain[wheel]*dError[wheel]
        
        if(wheel==self.left):
            strwheel="left"
        else:
            strwheel="right"
        self.logger.info(strwheel+"/pErrorWithGain/"+str(pe))
        
        self.logger.info(strwheel+"/iErrorWithGain/"+str(ie))
        
        self.logger.info(strwheel+"/dErrorWithGain/"+str(de))
        
        value=pe+de+ie
        self.logger.info(strwheel+"/controlValueCm/"+str(value))
        value=self.convertCmToVelocity(value)
        
        self.logger.info(strwheel+"/controlValueVelocity/"+str(value))
        
        return value
        
    '''
        Checks if the overall error is within a certain threshhold
    '''
    def constrain(self,cm):
        if(cm > self.setPoint-self.cmMin):
            return self.cmMin
        elif(cm < self.setPoint-self.cmMax):
            return self.cmMax
        return cm
    
    
    ''' 
        input cm is ranged from -10 to 10
    '''
    
    def convertCmToVelocity(self,cm):
        #print("raw cm ="+str(cm))
        #cm=self.constrain(cm)
        #print("soft cm="+str(cm))
        value=2
        if(cm < -0.6):
            if(cm < -0.6 and cm > -3):
                value=3
            if(cm < -3 and cm > -7):
                value=4  
            if(cm < -7 and cm > -10):
                value=5 
            if(cm < -10 and cm > - self.cmMax):
                value=6     
        return int(value)
    
    '''
        Serializes gain-factors
    '''
    def pickleGainFactors(self):
        gainFactors=[self.pGain,self.dGain,self.iGain]
        try:
            pickle.dump(gainFactors, open("PidGainFactors.p", "wb"), protocol=-1)
            self.logger.info("pickleGainFactorsSucces/true")
            return 1
        except IOError:
            self.logger.info("pickleGainFactorsSucces/false")
            pass
        return 0     
      
    '''
        Deseriallizes gain-factors
    '''
    def unpickleGainFactors(self):
        returnValue=0
        if(os.path.exists("PidGainFactors.p")):
            try:
                returnValue = pickle.load(open("PidGainFactors.p", "rb"))
            except EOFError:
                print("Error unpickling pid")
        self.logger.info("unpickleGainFactorsSucces/"+str(returnValue))
        return returnValue
        
def main():
    pass

if __name__ == '__main__':
    pass