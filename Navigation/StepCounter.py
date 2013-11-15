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
        
    
    '''
        Callable
    '''
    def __call__(self, steps):
        self.stepsLeft = self.stepsLeft + steps[left]
        self.stepsRight = self.stepsRight + steps[right]
    
   
    '''
        Reset step instance variables
    '''
    def resetSteps(self):
        self.stepsLeft = 0
        self.stepsRight = 0
    
    '''
        Calculate average steps using both wheels.
        *Private function*
    '''
    def _average(self, stepsLeft, stepsRight):
        return (stepsLeft + stepsRight) / 2
        
    
    '''
        Get average steps
    '''
    def getSteps(self):
        return self._average(self.stepsLeft, self.stepsRight)
    
    
def main():
    test = StepCounter()
    test([5000, 7500])
    print test.getSteps()
    test.resetSteps()
    print test.getSteps()
    
if __name__ == '__main__':
    main()
        