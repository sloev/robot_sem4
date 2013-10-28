'''
Created on Oct 15, 2013

@author: johannes
'''
import logging
import cPickle as pickle
import os.path


Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A


sensorChannels=[Vin1,Vin2,Vin3]

class Pid():
    '''
    pid control
    inspired by:
    http://letsmakerobots.com/node/865
    
    uses three sharp ir sensors connected through i2c with ad7998 ad-converter
    and for output it uses two stepper motors
    
    if self.left =0 and self.right=1 it will drive towards the direction of its sensor head

    '''

    def __init__(self,left,right,ir_sensors, dual_motors):
        self.left=left
        self.right=right
        
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing Pid")
        self.ir_sensors=ir_sensors
        self.dual_motors=dual_motors
        self.setPoint=15
        self.cmMax=25
        self.cmMin=5
        
        self.lastError=[0,0] #last error 
        self.iError=[0,0]
        
        '''gain factors'''
        self.pGain=[0,0]  #proportional gain factor
        self.dGain=[0,0]  #differential gain factor
        self.iGain=[0,0]  #integral gain factor
        gainFactors=self.unpickleGainFactors()

        if(gainFactors==0):           
            self.logger.debug("gainFactors not unpickled")
        else:
            self.pGain=gainFactors[0]
            self.dGain=gainFactors[1]
            self.iGain=gainFactors[2]
            self.logger.debug("gainFactors loaded from pickle")
        self.logger.debug("Initializing Pid DONE")
        
    '''
        doPid:
        calculates errors according to setpoint
        sends calculated new velocities to motors
    '''
    def doPid(self):
        self.logger.debug("Doing pid")
        sample=self.sampleDistances()
        
        walls=self.detectMissingWalls(sample)
        if(walls==[1,1]):
            currentError=[self.setPoint-sample[self.left],self.setPoint-sample[self.right]] 
            self.logger.info("currentError:"+str(currentError))
            #print("currentError:"+str(currentError))            
            
            dError=[currentError[self.left]-self.lastError[self.left],currentError[self.right]-self.lastError[self.right]]
            self.logger.info("dError:"+str(dError))        
            
            controlValues=[self.computeControlValues(self.left,currentError,dError),self.computeControlValues(self.right,currentError,dError)]
            self.logger.info("controlValues:"+str(controlValues))
            
            self.lastError=currentError
            self.iError=[currentError[self.left]+self.iError[self.left],currentError[self.right]+self.iError[self.right]]
            self.logger.info("iError:"+str(self.iError))
            
            self.setMotors(controlValues)
        else:
            msg="walls missing at:"
            if(walls[self.left]==0):
                msg+=" self.left "
            if(walls[self.right]==0):
                msg+=" self.right "
            self.logger.warning(msg)
        self.logger.debug("Doing pid DONE")
        return walls
    
    def sampleDistances(self):
        sample=self.ir_sensors.multiChannelReadCm(sensorChannels,5)
        self.logger.info("sample:"+str(sample))
        return sample
    
    def setMotors(self,controlValues):
        #print("control values="+str(controlValues))
        self.dual_motors.setMotorParams(self.left, self.right, controlValues[self.left], controlValues[self.right])
    
    def detectMissingWalls(self,sample):
        walls=[1,1]
        if(sample[self.left]>self.cmMax):
            walls[self.left]=0
        if(sample[self.right]>self.cmMax):
            walls[self.right]=0
        return [1,1]
    
    def pTune(self,pGain):
        if(pGain[self.left]==0):
            self.pGain=[self.pGain[self.left],pGain[self.right]]
        elif(pGain[self.right]==0):
            self.pGain=[pGain[self.left],self.pGain[self.right]]
        else:
            self.pGain=pGain
        self.logger.debug("pTune new pGain:"+str(self.pGain))

            
    def dTune(self,dGain):
        if(dGain[self.left]==0):
            self.dGain=[self.dGain[self.left],dGain[self.right]]
        elif(dGain[self.right]==0):
            self.dGain=[dGain[self.left],self.dGain[self.right]]
        else:
            self.dGain=dGain
        self.logger.debug("pTune new dGain:"+str(self.dGain))

        
    def iTune(self,iGain):
        if(iGain[self.left]==0):
            self.iGain=[self.iGain[self.left],iGain[self.right]]
        elif(iGain[self.right]==0):
            self.iGain=[iGain[self.left],self.iGain[self.right]]
        else:
            self.iGain=iGain
        self.logger.debug("pTune new iGain:"+str(self.iGain))
    
    def getGainFactors(self):
        return [self.pGain,self.dGain,self.iGain]

            
    def computeControlValues(self,wheel,currentError,dError):
        value=self.pGain[wheel]*currentError[wheel]
        value+=self.dGain[wheel]*dError[wheel]
        value+=self.iGain[wheel]*self.iError[wheel]
        value=self.convertCmToVelocity(value)
        return value
        
    def constrain(self,cm):
        if(cm > self.cmMax-self.setPoint):
            return self.cmMax-self.setPoint
        elif(cm < self.cmMin-self.setPoint):
            return self.cmMin-self.setPoint
        return cm
    
    ''' input cm is ranged from -10 to 10'''
    def convertCmToVelocity(self,cm):
        #print("raw cm ="+str(cm))
        cm=self.constrain(cm)
        #print("soft cm="+str(cm))
        value=2
        if(cm > 0.5):
            if(cm >0.5 and cm < 2):
                value=3
            elif(cm > 2 and cm < 4):
                value=4  
            elif(cm > 4 and cm < 8):
                value=5 
            elif(cm >8 and cm < 10):
                value=6            
        return value
    
    def pickleGainFactors(self):
        gainFactors=[self.pGain,self.dGain,self.iGain]
        try:
            pickle.dump(gainFactors, open("PidGainFactors.p", "wb"), protocol=-1)
            return 1
        except IOError:
            pass
        return 0        
    
    def unpickleGainFactors(self):
        returnValue=0
        if(os.path.exists("PidGainFactors.p")):
            try:
                returnValue = pickle.load(open("PidGainFactors.p", "rb"))
            except EOFError:
                print("Error unpickling pid")
        return returnValue
        
def main():
    pass

if __name__ == '__main__':
    pass