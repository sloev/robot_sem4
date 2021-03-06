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
        self.steps=[0,0]
        self.old=[0,0]
    
    '''
        Callable
    '''
    def __call__(self, steps):
        self.steps=steps
        
    '''
        Reset step instance variables
    '''
    def resetSteps(self,steps=0):
        self.steps=[steps,steps]

    '''
        Calculate average steps using both wheels.
        *Private function*
    '''

    
    '''
        Get average steps
    '''
    def getSteps(self):

        return (self.steps[0]+self.steps[1])/2

def main():
    test = StepCounter()
    test([5000, 7500])
    print test.getSteps()
    test.resetSteps()
    print test.getSteps()
    
if __name__ == '__main__':
    main()
        