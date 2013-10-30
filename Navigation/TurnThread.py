'''
Created on Oct 30, 2013

@author: johannes
'''
import logging


class TurnThread():
    def __init__(self):
        self.funcDict={
                       1 : self.goStraight(),
                       2 : self.turnRight(),
                       3 : self.turn180(),
                       4 : self.turnLeft()
                       }
        self.logger=logging.getLogger("robot.TurnThread")
        self.logger.info("TurnThread initialised")
        pass
    
    def checkForTurn(self,choice):
        self.funcDict[choice]()
        
    def turnLeft(self):
        self.logger.info("left")
        pass
    
    def turnRight(self):
        self.logger.info("right")
        pass
    
    def turn180(self):
        self.logger.info("180")
        pass
    
    def goStraight(self):
        self.logger.info("straight")
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