'''
Created on Oct 30, 2013

@author: johannes
'''

class TurnThread():
    def __init__(self):
        self.funcDict={
                       1 : self.goStraight(),
                       2 : self.turnRight(),
                       3 : self.turn180(),
                       4 : self.turnLeft()
                       }
        pass
    
    def checkForTurn(self,choice):
        self.funcDict[choice]()
        
    def turnLeft(self):
        pass
    
    def turnRight(self):
        pass
    
    def turn180(self):
        pass
    
    def goStraight(self):
        pass

def main():
    pass

if __name__== '__main__':
    main()

        
'''
 def turn(self,direction):
        #print("turning wheel="+str(direction))
        time.sleep(1)
        self.dual_motors.softStop()
        time.sleep(0.3)
        self.dual_motors.turn90(direction, 2)
        time.sleep(0.8)
        
        self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
        self.dual_motors.setPosition(32767, 32767)

        time.sleep(0.5)
        self.pid.reset()
# 
#         walls=oldWalls=self.pid.detectMissingWalls(self.pid.sampleDistances())
#         while(walls==oldWalls):
#             try:
#                 walls=self.pid.detectMissingWalls(self.pid.sampleDistances())
#             except IOError:
#                 print("got ioerror in sampling ir sensors")
#             time.sleep(0.1)
        print("turning finnished")
'''