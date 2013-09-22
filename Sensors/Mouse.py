'''
Created on Sep 17, 2013

@author: machon
'''

class Mouse():
    '''
    classdocs
    '''
    
    angle = 0.0
    length = 0.0

    def __init__(self, x, y, angle, length):
        self.x = x
        self.y = y
        self.angle = angle
        self.length = length
        
    def toString(self):
        a=str(str(self.x)+" "+str(self.y)+" "+str(self.angle)+" "+str(self.length))
        return a
    
    def getAngle(self):
        return self.angle
    
    def getLength(self):
        return self.length
        