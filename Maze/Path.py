'''
Created on Nov 14, 2013

@author: johannes
'''

class Path(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.path=[]
        self.cost=0
        
    def append(self,node):
        
        self.cost+=node.g
        self.path.append(node)

    def reverse(self):
        self.path=self.path[::-1]
        
    def __str__(self):
        string="[\tpath\t]\n"
        string+="cost=%d" % self.cost+"\n"
        cost=0
        for a in self.path:
            string+=str(a)+"\tcost until now =\t"+str(a.g)+"\n"
        string+="overallcost =\t"+str(self.path[len(self.path)-1].g)
        string+="\n[\tpath\t]\n"
        return string
    
    def getPath(self):
        return self.path        
        