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
            string+=str(a)+"\tGcost =\t"+str(a.g)+"\t"
            string+=str(a)+"\tHcost =\t"+str(a.h)+"\t"
            string+=str(a)+"\tFcost =\t"+str(a.f)+"\t"
            string+=str(a)+"\tdirection to me =\t"+str(a.directionToMe)+"\n"
        string+="overallcost =\t"+str(self.path[len(self.path)-1].g)
        string+="\n[\tpath\t]\n"
        return string
    
    def getPath(self):
        return self.path        
        