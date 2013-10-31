'''
Created on Oct 30, 2013

@author: johannes
'''
import re
import sys
from datetime import datetime
class Pid():
    def __init__(self,filename,saveName):
        self.saveName=saveName
        self.filename=filename
        self.foo=open(filename,"r")
        self.strings = self.foo
        self.startTime= datetime.fromtimestamp(0)
2013-10-31 10:03:51,477/robot.pid/left/pErrorWithGain/0.0
2013-10-31 10:03:51,479/robot.pid/left/iErrorWithGain/0.0
2013-10-31 10:03:51,481/robot.pid/left/dErrorWithGain/0.0
2013-10-31 10:03:51,482/robot.pid/left/controlValueCm/0.0
2013-10-31 10:03:51,484/robot.pid/left/controlValueVelocity/2
2013-10-31 10:03:51,485/robot.pid/right/pErrorWithGain/0.0
2013-10-31 10:03:51,487/robot.pid/right/iErrorWithGain/0.0
2013-10-31 10:03:51,489/robot.pid/right/dErrorWithGain/0.0
2013-10-31 10:03:51,490/robot.pid/right/controlValueCm/0.0
2013-10-31 10:03:51,492/robot.pid/right/controlValueVelocity/2
        self.patterns=[
                       'left/pErrorWithGain/',
                       'right/pErrorWithGain/',
                       'left/iErrorWithGain/',
                       'right/iErrorWithGain/',
                       'left/dErrorWithGain/',
                       'right/dErrorWithGain/',
                       'left/controlValueCm/',
                       'right/controlValueCm/',
                       'left/controlValueVelocity/',
                       'right/controlValueVelocity/',
                       'left/pError/', 
                       'right/pError/', 
                       'left/iError/',
                       'right/iError/',
                       'left/dError/',
                       'right/dError/'
                       ]

        self.allOut="seconds\tleftPGE\trightPGE\tleftIGE\trightIGE\tleftDGE\trightDGE\tleftValCm\trightValCm\tleftValVel\trightValVel\tleftPE\trightPE\tleftIE\trightIE\tleftDE\trightDE\n"

        self.functions=[
                        self.start,
                        self.same,
                        self.same,
                        self.same,
                        self.same,
                        self.same,
                        self.same,
                        self.same,
                        self.same,
                        self.same,
                        self.same,#shall be same in final
                        self.same,
                        self.same,
                        self.same,
                        self.same,
                        self.finnish
                        ]
        
    def __call__(self):
        for s in self.strings:
            self.currentString=s
            for pattern,case in zip(self.patterns,self.functions):
                case(re.search(pattern,s))
        foo = open(self.saveName, "w")

        try:
            foo.write(self.allOut)
        finally:
            foo.close    
            
    def start(self,found):
        if found: 
            index=found.span()[0]
            thisDate=self.currentString[:22]
            dt = datetime.strptime(thisDate, "%Y-%m-%d %H:%M:%S,%f")
                        
            if(round(int(self.startTime.strftime('%s')),3)<1):
                self.startTime=dt
                currentTime=str(0)
            else:
                delta=(dt-self.startTime).total_seconds()
                seconds=round(delta,5)
                currentTime=str(seconds)            
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]    
                        
            self.allOut=''.join([self.allOut,currentTime+"\t"+perror]) 
        else: 
            pass  
                
    def same(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:]#len(self.currentString)]                
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
        
    def finnish(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror])+"\n"
        else: 
            pass
        
def main():
    pidParser=Pid(sys.argv[1],sys.argv[2])
    pidParser()

if __name__ == '__main__':
    main()