'''
Created on Sep 11, 2013

@author: johannes, Daniel
'''
from evdev import InputDevice
from select import select
from numpy import array
from CalculateAngle import Calculations
import threading

devices = map(InputDevice,('/dev/input/event3','/dev/input/event3'))
devices = {dev.fd : dev for dev in devices}


class MouseInput(threading.Thread):
    '''
    Takes input from two mice connected to input 4 and 5. 
    Delta movements are stored in a matrix
    lolling fra ivo til johannes
    Depends on:
    evdev.py
    '''

    def __init__(self, calc):
        threading.Thread.__init__(self)
        self.delta = array([[0,0],[0,0]])
        self.calculator = calc
        hasEvent=0
        '''
        Constructor
        '''

    def run(self):

        for dev in devices.values(): print(dev)

        while True:
            r,w,x = select(devices, [], [])
            for fd in r:
                for event in devices[fd].read():
                    hasEvent=1
                    string = str(event)
                    strings = string.split()
                    if strings[6]=="02,":
                        if strings[4]=="00,":
                            a=int(strings[8]) 
                            self.delta[fd-4,:1]=a
                        else:
                            a=int(strings[8]) 
                            self.delta[fd-4,1:2]=a 
            if(hasEvent):
                hasEvent=0
                #print(delta)
                self.calculator.calcAngle(self.delta)

            #print("mouse3:\t\tmouse4:\n"+str(delta[:1,:])+"\t"+str(delta[1:2,:]))

                
def main():
    mouse=MouseInput()
    mouse.getInput()
    
if __name__== '__main__':
    main()

