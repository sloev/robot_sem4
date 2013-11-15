'''
Created on 15/11/2013

@author: danielmachon
'''

class Navigator():
    '''
    classdocs
    '''


    def __init__(self):
        self.steps = 0
        
    
    def __call__(self, steps):
        self.steps = self.steps + steps
    
   
    def resetSteps(self):
        self.steps = 0
        
        
    def getSteps(self):
        return self.steps
    
def main():
    pass
    
if __name__ == '__main__':
    main()
        