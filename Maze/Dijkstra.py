'''
Created on Nov 18, 2013

@author: johannes
'''
from collections import defaultdict
from Path import Path
class Node():
    def __init__(self,x,y,d):
        self.x=x
        self.y=y
        self.d=d
        self.prev=None
        self.visited=False
        self.cost=100000
        
    def costTo(self,node):
        cost=1
        tmp=node.d-2
        if tmp < 0 :
            tmp=3-abs(tmp)
        if tmp!=self.d:
            cost=cost+1
        return cost
    def __str__(self):
        string="[%d,%d,%d]"%(self.x,self.y,self.d)
        return string

class Graph():
    def __init__(self,mazeModel):
        self.mazeModel=mazeModel
        self.nodes=defaultdict(lambda:defaultdict(defaultdict(int)))
        self.graph=set()
        self.distances=set()
        self.straightCost=1
        self.cornerCost=2
        self.makeWAR()
        
    def makeWAR(self):          
        for y in range(self.mazeModel.getHeight()):
            for x in range(self.mazeModel.getWidth()):  
                walls=self.mazeModel.get(x,y)   
                for d in range(4):
                    tmp=1
                    if(walls &(1<<d)):
                        tmp=0
                    self.nodes[x][y][d]=Node(x,y,tmp)
                    self.graph[self.nodes[x][y][d]]=[]
                for i in range(4):
                    for j in range(4):
                        cost=self.straightCost
                        if(abs(i-j)!=2):
                            cost=self.cornerCost
                        if i!=j:
                            self.graph[self.nodes[x][y][i]].append((self.nodes[x][y][j],cost))
                            self.graph[self.nodes[x][y][j]].append((self.nodes[x][y][i],cost))   
#                 
#                 self.graph[self.nodes[x][y][0]].append((self.nodes[x][y][2],self.straightCost))
#                 self.graph[self.nodes[x][y][2]].append((self.nodes[x][y][0],self.straightCost))
#                 
# #                 self.distances[(self.nodes[x][y][0], self.nodes[x][y][2])]=self.straightCost
# #                 self.distances[(self.nodes[x][y][2], self.nodes[x][y][0])]=self.straightCost
#                 
#                 self.graph[self.nodes[x][y][1]].append((self.nodes[x][y][3],self.straightCost))
#                 self.graph[self.nodes[x][y][3]].append((self.nodes[x][y][1],self.straightCost))
# #                 self.distances[(self.nodes[x][y][1], self.nodes[x][y][3])]=self.straightCost
# #                 self.distances[(self.nodes[x][y][3], self.nodes[x][y][1])]=self.straightCost
#                                 
#                 self.graph[self.nodes[x][y][0]].append((self.nodes[x][y][1],self.cornerCost))
#                 self.graph[self.nodes[x][y][1]].append((self.nodes[x][y][0],self.cornerCost))
# #                 self.distances[(self.nodes[x][y][0], self.nodes[x][y][1])]=self.cornerCost
# #                 self.distances[(self.nodes[x][y][1], self.nodes[x][y][0])]=self.cornerCost
#                 
#                 self.graph[self.nodes[x][y][1]].append((self.nodes[x][y][2],self.cornerCost))
#                 self.graph[self.nodes[x][y][2]].append((self.nodes[x][y][1],self.cornerCost))
# #                 self.distances[(self.nodes[x][y][1], self.nodes[x][y][2])]=self.cornerCost
# #                 self.distances[(self.nodes[x][y][2], self.nodes[x][y][1])]=self.cornerCost
#                                 
#                 self.graph[self.nodes[x][y][2]].append((self.nodes[x][y][3],self.cornerCost))
#                 self.graph[self.nodes[x][y][3]].append((self.nodes[x][y][2],self.cornerCost))
# #                 self.distances[(self.nodes[x][y][2], self.nodes[x][y][3])]=self.cornerCost
# #                 self.distances[(self.nodes[x][y][3], self.nodes[x][y][2])]=self.cornerCost
#                 
#                 self.graph[self.nodes[x][y][3]].append((self.nodes[x][y][0],self.cornerCost))
#                 self.graph[self.nodes[x][y][0]].append((self.nodes[x][y][3],self.cornerCost))
# #                 self.distances[(self.nodes[x][y][3], self.nodes[x][y][0])]=self.cornerCost
# #                 self.distances[(self.nodes[x][y][0], self.nodes[x][y][3])]=self.cornerCost

        for y in range(self.mazeModel.getHeight()):
            for x in range(self.mazeModel.getWidth()):
                #east
                if(self.nodes[x][y][1] and self.nodes[x+1][y][3]):
                    self.graph[self.nodes[x][y][1]].append((self.nodes[x+1][y][3],self.straightCost))
                    self.graph[self.nodes[x+1][y][3]].append((self.nodes[x][y][1],self.straightCost))
                    
#                     self.distances[(self.nodes[x][y][1],self.nodes[x+1][y][3])]=self.straightCost
#                     self.distances[(self.nodes[x+1][y][3],self.nodes[x][y][1])]=self.straightCost
                    
                if(self.nodes[x][y][2] and self.nodes[x][y+1][0]):
                    self.graph[self.nodes[x][y][2]].append((self.nodes[x][y+1][0],self.straightCost))
                    self.graph[self.nodes[x][y+1][0]].append((self.nodes[x][y][2],self.straightCost)) 
                    
#                     self.distances[(self.nodes[x][y][1],self.nodes[x+1][y][3])]=self.straightCost
#                     self.distances[(self.nodes[x+1][y][3],self.nodes[x][y][1])]=self.straightCost              
                    
class Dijkstra():
    def __init__(self,mazeModel,source,target):
        self.source=source
        self.target=target
        self.mazeModel=mazeModel
        self.graph=Graph(self.mazeModel)
        self.start=self.graph.nodes[source[0]][source[1]][0]
        self.end=self.graph.nodes[target[0]][target[1]][0]

    def retracePath(self,c):
        def parentgen(c):
            while c:
                yield c
                c = c.prev
        result = [element for element in parentgen(c)]
        path=Path(result)
        return path
           
    def search(self):
        for v in self.graph:
            v.cost=10000
        for i in range(4):
            self.graph.nodes[self.source[0]][self.Ssource[1]][i].cost=0
        openList=set()
        openList.add(self.start)
        visited=[]
        closedList = set()

        while openList:
            current = sorted(openList, key=lambda inst:inst.cost)[0]
            if [current.x,current.y]==[self.end.x,self.end.y]:
                self.retracePath(current)
            visited.append(current)
            openList.remove(current)
            closedList.add(current)
            
            for p in self.graph(current):
                n=p[0]
                cost=p[1]
                dist=current.cost+cost
                if dist < n.cost and not n.visited:
                    n.cost=dist
                    n.prev=current
                    openList.add(n)
def main():
    
    

if __name__ == '__main__':
    main()