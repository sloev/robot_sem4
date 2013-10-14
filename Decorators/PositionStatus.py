'''
Created on Oct 2, 2013

@author: Daniel Machon
'''

import smbus

class PositionStatus(object):
    


    def __init__(self, f):
        print "\n"
        print "Daniel Machon's awesome decorator initialized!"
        self.bus = smbus.SMBus(1)
        self.f = f
        self.setData(f)
        print "Decorating function " + self.f.__name__ + "\n"
    
    def __call__(self):
        pass
    
    def setData(self, f):
        pass
    
def main():
    pass

if __name__ == '__main__':
    main()
        