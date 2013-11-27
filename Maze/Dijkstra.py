'''
Created on Nov 18, 2013

@author: johannes
'''
from collections import defaultdict
from Path import Path
class Node():
    def __init__(self,x,y,walls,d,dillemma):
        self.x=x
        self.y=y
        self.walls=walls
        self.d=d
        self.prev=None
        self.visited=False
        self.cost=100000
        self.dillemma=dillemma
        
    def costTo(self,node):
        cost=1
        tmp=node.d-2
        if tmp < 0 :
            tmp=3-abs(tmp)
        if tmp!=self.d:
            cost=cost+1
        return cost
    
    def __str__(self):
        string="[%d,%d,%d,%d]"%(self.x,self.y,self.walls,self.d)
        return string

class Graph():
    def __init__(self,mazeModel):
        self.mazeModel=mazeModel
        self.nodes=defaultdict(lambda:defaultdict(lambda:defaultdict(int)))
        self.graph={}
        self.distances=set()
        self.straightCost=1
        self.cornerCost=3
        self.makeWAR()
        
    def __str__(self):
        string=""
        for y in range(self.mazeModel.height):
            for x in range(self.mazeModel.width):
                string=string+"["
                for d in range(4):
                    if self.nodes[x][y][d]:
                        node=self.nodes[x][y][d]
                        string=string+str(node.d)+","
                    else:
                        string=string+"x,"
                string=string+"]\t"
            string=string+"\n"
        return string

    def makeWAR(self):          
        for y in range(self.mazeModel.getHeight()):
            for x in range(self.mazeModel.getWidth()):  
                walls=self.mazeModel.get(x,y)  
                dillemma=True
                if walls==10 or walls==5:
                    dillemma=False
                for d in range(4):
                    tmp=1
                    if not (walls &(1<<(3-d))):
                        tmp=0
                    self.nodes[x][y][d]=Node(x,y,tmp,d,dillemma)
                    self.graph[self.nodes[x][y][d]]=[]
                for i in range(4):
                    for j in range(4):
                        cost=self.straightCost
                        if(abs(i-j)!=2):
                            cost=self.cornerCost
                        if i!=j:
                            if self.nodes[x][y][i] and self.nodes[x][y][j]:
                                self.graph[self.nodes[x][y][i]].append((self.nodes[x][y][j],cost))
                                self.graph[self.nodes[x][y][j]].append((self.nodes[x][y][i],cost))   
                            
        for y in range(self.mazeModel.getHeight()):
            for x in range(self.mazeModel.getWidth()):
                #east
                if(self.nodes[x][y][1] and self.nodes[x+1][y][3]):
                    if(self.nodes[x][y][1].walls!=1 and self.nodes[x+1][y][3].walls!=1):
                        self.graph[self.nodes[x][y][1]].append((self.nodes[x+1][y][3],self.straightCost))
                        self.graph[self.nodes[x+1][y][3]].append((self.nodes[x][y][1],self.straightCost))
                    
                if(self.nodes[x][y][2] and self.nodes[x][y+1][0]):
                    if(self.nodes[x][y][2].walls!=1 and self.nodes[x][y+1][0].walls!=1):
                        self.graph[self.nodes[x][y][2]].append((self.nodes[x][y+1][0],self.straightCost))
                        self.graph[self.nodes[x][y+1][0]].append((self.nodes[x][y][2],self.straightCost)) 
                    
class Dijkstra():
    def __init__(self):
        pass
        #print self.graphObj
        
    def retracePath(self,c):

        parents=[]
        parents.append(c)
        parent=c.prev
        while parent!=None:
            parents.append(parent)
            parent=parent.prev
        path=Path(parents)
        return path
           
    def __call__(self,source,target,graphObj):
        graph=graphObj.graph
        nodes=graphObj.nodes
        source=source
        target=target
        #print self.nodes
        openList=set()

        for i in range(4):
            if nodes[self.source[0]][self.source[1]][i]:
                nodes[source[0]][source[1]][i].cost=0
                self.start=nodes[source[0]][source[1]][i]
                openList.add(self.start)

        for i in range(4):
            if nodes[self.target[0]][self.target[1]][i]:
                self.end=nodes[target[0]][target[1]][i]
                break
        visited=[]
        closedList = set()

        while openList:
            current = sorted(openList, key=lambda inst:inst.cost)[0]
            #print current
            if current.x==self.end.x and current.y==self.end.y:
                return [self.retracePath(current),visited]
                
            visited.append(current)
            openList.remove(current)
            closedList.add(current)
            
            for p in graph[current]:
                n=p[0]
                cost=p[1]
                dist=current.cost+cost
                if dist <= n.cost and not n.visited:
                    n.cost=dist
                    n.prev=current
                    openList.add(n)
        print visited
        return [None,visited]
    
def main():
    pass
    

if __name__ == '__main__':
    main()