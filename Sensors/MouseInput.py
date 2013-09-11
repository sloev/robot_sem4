'''
Created on Sep 11, 2013

@author: johannes, daniel
'''
from evdev import InputDevice
from select import select
from numpy import array

devices = map(InputDevice,('/dev/input/event4','/dev/input/event5'))
devices = {dev.fd : dev for dev in devices}

delta = array([[0,0],[0,0]])


class MouseInput:
    '''
    Takes input from two mice connected to input 4 and 5. 
    Delta movements are stored in a matrix
    
    Depends on:
    evdev.py
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def update(self):

        for dev in devices.values(): print(dev)

        while True:
            r,w,x = select(devices, [], [])
            for fd in r:
                for event in devices[fd].read():
                    string = str(event)
                    strings = string.split()
                    if strings[6]=="02,":
                        if strings[4]=="00,":
                            delta[fd-4,:1]=int(strings[8]) 
                        else:
                            delta[fd-4,1:2]=int(strings[8]) 

            print("mouse3:\t\tmouse4:\n"+str(delta[:1,:])+"\t"+str(delta[1:2,:]))
    def getInput(self):
        return delta
                
def main():
    mouse=MouseInput()
    mouse.getInput()
    
if __name__== '__main__':
    main()