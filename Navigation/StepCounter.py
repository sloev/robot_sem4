'''
Created on 15/11/2013

@author: Daniel Machon, Ivo Drlje
'''

'''''''''''''''''''''
'  Class variables  '
'''''''''''''''''''''
left = 0
right = 1

class StepCounter():
    

    '''
        Constructor
    '''
    def __init__(self):
        self.stepsLeft = 0
        self.stepsRight = 0
        self.old=0
    
    '''
        Callable
    '''
    def __call__(self, steps):
        self.stepsLeft = steps[left]
        self.stepsRight = steps[right]
    
   
    '''
        Reset step instance variables
    '''
    def resetSteps(self):
        self.old=[self.stepsLeft,self.stepsRight]
        self.stepsLeft = 0
        self.stepsRight = 0
    
    '''
        Calculate average steps using both wheels.
        *Private function*
    '''
    def _average(self, stepsLeft, stepsRight):
        value= (stepsLeft + stepsRight) / 2
        return value
        
    
    '''
        Get average steps
    '''
    def getSteps(self):
        toCompute=[self.stepsLeft-self.old[0],self.stepsRight-self.old[1]]
        return self._average(self.toCompute[0], self.toCompute[1])
    
    
def main():
    test = StepCounter()
    test([5000, 7500])
    print test.getSteps()
    test.resetSteps()
    print test.getSteps()
    
if __name__ == '__main__':
    main()
        