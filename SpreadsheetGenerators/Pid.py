'''
Created on Oct 30, 2013

@author: johannes
'''
import re
import sys

class Pid():
    def __init__(self,file):
        self.filename=file
        self.foo=open(file,"r")
        self.strings = self.foo
        #left file, right file
        self.patterns=[
                       'left/pError/', 
                       'right/pError/', 
                       'left/iError/',
                       'right/iError/',
                       'left/dError/',
                       'right/dError/'
                       ]
        self.leftPErrors=""
        self.rightPErrors=""
        
        self.leftIErrors=""
        self.rightIErrors=""
        
        self.leftDErrors=""
        self.rightDErrors=""

        self.functions=[
           self.leftPError,
           self.rightPError,
           self.leftIError,
           self.rightIError,
           self.leftDError,
           self.rightDError]
        
    def __call__(self):
        for s in self.strings:
            self.currentString=s
            for pattern,case in zip(self.patterns,self.functions):
                case(re.search(pattern,s))
        f1 = open(str(self.filename)+"leftperror.txt", "w")
        f2 = open(str(self.filename)+"rightperror.txt", "w")

        f3 = open(str(self.filename)+"leftierror.txt", "w")
        f4 = open(str(self.filename)+"rightierror.txt", "w")

        f5 = open(str(self.filename)+"leftderror.txt", "w")
        f6 = open(str(self.filename)+"rightderror.txt", "w")
        
        try:
#             d1="\n".join(self.leftPErrors)
#             d2="\n".join(self.rightPErrors)
# 
#             d3="\n".join(self.leftIErrors)
#             d4="\n".join(self.rightIErrors)
# 
#             d5="\n".join(self.leftDErrors)
#             d6="\n".join(self.rightDErrors)
#             
#             f1.write(d1)
#             f2.write(d2)
#             f3.write(d3)
#             f4.write(d4)
#             f5.write(d5)
#             f6.write(d6)
            f1.write(self.leftPErrors)
            f2.write(self.rightPErrors)
            f3.write(self.leftIErrors)
            f4.write(self.rightIErrors)
            f5.write(self.leftDErrors)
            f6.write(self.rightDErrors)
            
        finally:
            f1.close#write(d1)
            f2.close#write(d2)
            f3.close#write(d3)
            f4.close#write(d4)
            f5.close#write(d5)
            f6.close    
            
    def leftPError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:]
            self.leftPErrors=''.join([self.leftPErrors,perror]) 
        else: 
            pass
        
    def rightPError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:]
            self.rightPErrors=''.join([self.rightPErrors,perror])
        else: 
            pass
        
    def leftIError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:]
            self.leftIErrors=''.join([self.leftIErrors,perror])
        else: 
            pass
        
    def rightIError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:]
            self.rightIErrors=''.join([self.rightIErrors,perror])
        else: 
            pass    
        
    def leftDError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:]
            self.leftDErrors=''.join([self.leftDErrors,perror])      
        else: 
            pass
        
    def rightDError(self,found):
        if found: 
            index=found.span()[1]
            perror=self.currentString[index:]
            self.rightDErrors=''.join([self.rightDErrors,perror])
        else: 
            pass

def main():
    pidParser=Pid(sys.argv[1])
    pidParser()
    pass
if __name__ == '__main__':
    main()