'''
Created on Nov 14, 2013

@author: johannes
'''

class Path(object):
    '''
    classdocs
    '''


    def __init__(self,path=[]):
        '''
        Constructor
        '''
        self.path=path
        self.path.reverse()
        self.cost=self.calculateCost()
        
    def calculateCost(self):       
        lastNode=self.path[len(self.path)-1]
        cost=lastNode.g
        return cost

    def __str__(self):
        string="[\tpath\t]\n"
        string+="cost=%d" % self.cost+"\n"
        for a in self.path:
            string+=str(a)+"\tGcost =\t"+str(a.cost)+"\t"
        string+="\n[\tpath\t]\n"
        return string
    
    def getPath(self):
        return self.path        
        