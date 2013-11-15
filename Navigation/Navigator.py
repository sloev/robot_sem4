'''
Created on 15/11/2013

@author: danielmachon
'''

left = 0
right = 1

class Navigator():
    '''
    classdocs
    '''


    def __init__(self):
        self.steps = 0
        
    
    def __call__(self, steps):
        self.stepsLeft = self.stepsLeft + steps[left]
        self.stepsRight = self.stepsRight + steps[right]
    
   
    def resetSteps(self):
        self.stepsLeft = 0
        self.stepsRight = 0
        
    def _average(self, stepsLeft, stepsRight):
        return (stepsLeft + stepsRight) / 2
        
        
    def getSteps(self):
        return self._average(self.stepsLeft, self.stepsRight)
    
    
def main():
    pass
    
if __name__ == '__main__':
    main()
        