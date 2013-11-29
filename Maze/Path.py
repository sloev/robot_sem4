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
        cost=lastNode.cost
        return cost
    
    def pathToStack(self):
        stack=[]
        lastN=None
        #string=""
        
        for n in self.path:
            if lastN != None:
                if lastN.x==n.x and lastN.y==n.y:
                    #string+="%d"%n.d
                    stack.append([n.d,n.dillemma])
            else:                      
                stack.append([n.d,n.dillemma])
            #string+="\n"
            lastN=n
        stack.reverse()
        #print string
        return stack
            
    def __str__(self):
        string="[\tpath\t]\n"
        string+="cost=%d" % self.cost+"\n"
        for a in self.path:
            string+="["+str(a.x)+","+str(a.y)+"]\t"
            string+=str(a)+"\tGcost =\t"+str(a.cost)+"\t"
            if a.dillemma:
                string+="dillemma"
            string+="\n"
        string+="\n[\tpath\t]\n"
        return string
    
    def getPath(self):
        return self.path        
        