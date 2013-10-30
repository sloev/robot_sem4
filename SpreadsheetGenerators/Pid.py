'''
Created on Oct 30, 2013

@author: johannes
'''
import re
import sys

class Pid():
    def __init__(self,filename):
        self.filename=filename
        self.foo=open(file,"r")
        self.strings = self.foo
        self.patterns=[
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
            
    def leftPGE(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut=''.join([self.allOut,perror]) 
        else: 
            pass
    def rightPGE(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
    def leftIGE(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
    def rightIGE(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
    def leftDGE(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
    def rightDGE(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
    def leftValCm(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
    def rightValCm(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
    def leftValVel(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
    def rightValVel(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
        
    def leftPError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
        
    def rightPError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
        
    def leftIError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
        
    def rightIError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass    
        
    def leftDError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]                
            self.allOut='\t'.join([self.allOut,perror]) 
        else: 
            pass
        
    def rightDError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:len(self.currentString)-2]
            self.allOut='\t'.join([self.allOut,perror])+"\n"
        else: 
            pass

def main():
    pidParser=Pid(sys.argv[1])
    pidParser()

if __name__ == '__main__':
    main()