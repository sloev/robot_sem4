'''
Created on Oct 30, 2013

@author: johannes
'''
import re
import sys
from datetime import datetime
class Pid():
    def __init__(self,filename):
        self.filename=filename
        self.foo=open(filename,"r")
        self.strings = self.foo
        self.startTime= datetime.fromtimestamp(0)

        self.patterns=[
                       '/robot',
                       'left/pErrorWithGain/',
                       'right/pErrorWithGain/',
                       'left/iErrorWithGain/',
                       'right/iErrorWithGain/',
                       'left/dErrorWithGain/',
                       'right/dErrorWithGain/',
                       'left/controlValueCm/',
                       'right/controlValueCm/',
                       'left/controlValueVel/',
                       'right/controlValueVel/',
                       'left/pError/', 
                       'right/pError/', 
                       'left/iError/',
                       'right/iError/',
                       'left/dError/',
                       'right/dError/'
                       ]

        self.allOut="leftPGE\trightPGE\tleftIGE\trightIGE\tleftDGE\trightDGE\tleftValCm\trightValCm\tleftValVel\trightValVel\tleftPE\trightPE\tleftIE\trightIE\tleftDE\trightDE\n"

        self.functions=[
                        self.timecode,
                        self.leftPGE,
                        self.rightPGE,
                        self.leftIGE,
                        self.rightIGE,
                        self.leftDGE,
                        self.rightDGE,
                        self.leftValCm,
                        self.rightValCm,
                        self.leftValVel,
                        self.rightValVel,
                        self.leftPError,
                        self.rightPError,
                        self.leftIError,
                        self.rightIError,
                        self.leftDError,
                        self.rightDError
                        ]
        
    def __call__(self):
        for s in self.strings:
            self.currentString=s
            for pattern,case in zip(self.patterns,self.functions):
                case(re.search(pattern,s))
        foo = open(str(self.filename)+"allout.txt", "w")

        try:
            foo.write(self.allOut)
        finally:
            foo.close    
    def timecode(self,found):
        if found: 
            index=found.span()[0]
            thisDate=self.currentString[:index]
            parts = thisDate.split(',')
            dt = datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
            dt.replace(microsecond=int(parts[1]))
                        
            if(round(int(self.startTime.strftime('%s')),3)<1):
                self.startTime=dt
                currentTime=str(0)
            else:
                currentTime=str((dt-self.startTime).strftime('%s.%f'))
            print(currentTime)
            self.allOut=''.join([self.allOut,currentTime]) 
        else: 
            pass          

    def leftPGE(self,found):
        self.same(found)
        
    def rightPGE(self,found):
        self.same(found)

    def leftIGE(self,found):
        self.same(found)

    def rightIGE(self,found):
        self.same(found)

    def leftDGE(self,found):
        self.same(found)

    def rightDGE(self,found):
        self.same(found)

    def leftValCm(self,found):
        self.same(found)

    def rightValCm(self,found):
        self.same(found)

    def leftValVel(self,found):
        self.same(found)

    def rightValVel(self,found):
        self.same(found)
        
    def leftPError(self,found):
        self.same(found)

        
    def rightPError(self,found):
        self.same(found)

    def leftIError(self,found):
        self.same(found)

        
    def rightIError(self,found):
        self.same(found)

    def leftDError(self,found):
        self.same(found)
        
    def rightDError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror])+"\n"
        else: 
            pass
        
    def same(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]                
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass

def main():
    pidParser=Pid(sys.argv[1])
    pidParser()

if __name__ == '__main__':
    main()
#     
#      def rightPGE(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#     def leftIGE(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#     def rightIGE(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#     def leftDGE(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#     def rightDGE(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#     def leftValCm(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#     def rightValCm(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#     def leftValVel(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#     def rightValVel(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#         
#     def leftPError(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#         
#     def rightPError(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#         
#     def leftIError(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#         
#     def rightIError(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass    
#         
#     def leftDError(self,found):
#         if found: 
#             index=found.span()[1]
#             perror=self.currentString[index:len(self.currentString)-2]                
#             self.allOut='\t'.join([self.allOut,perror]) 
#         else: 
#             pass
#     