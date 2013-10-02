'''
Created on Oct 1, 2013

@author: machon
'''

class MyClass(object):
    '''
    classdocs
    '''


    def hi(self, func):
        self.func = func
        print "Fetching TMC status"
        print self.func
    
    @hi    
    def lol(self):
        r = [0xFF, 0xAA, 0xCC]
        
        
def main(self):
    test = MyClass
    
    test.lol()
        
if __name__== '__main__':
    main()        