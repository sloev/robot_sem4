'''
Created on Sep 11, 2013

@author: johannes
@review: johannes, benjamin
'''
from MouseInput import MouseInput
from CalculateAngle import Calculations
import thread


class Pid(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.calculator=Calculations()
        self.mice = MouseInput(self.calculator)

        '''
        Constructor
        '''
        
        #miceSensors.update()        thread.start_new_thread( miceSensor.update(), ("Thread-1", 2, ) )
        
#        self.initMouseThread()
        pass
    
    def computeAngle(self):
        pass

    def initMiceThread(self):
        self.mice.start()


def main():
    pid=Pid()
    pid.initMiceThread()
    
    while(1):
        pass
    
if __name__== '__main__':
    main()
