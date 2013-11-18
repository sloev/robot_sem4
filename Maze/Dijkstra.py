'''
Created on Nov 18, 2013

@author: johannes
'''
class Node():
    def __init__(self,x,y,d):
        self.x=x
        self.y=y
        self.d=d
        self.prev=None
        self.visited=False
        
    def __str__(self):
        string="[%d,%d,%d]"%(self.x,self.y,self.d)
        return string

class Graph():
    def __init__(self):
        pass
    
class Dijkstra():
    def __init__(self):
        
        pass
    def search(self):
        pass
    
def main():
    pass

if __name__ == '__main__':
    main()