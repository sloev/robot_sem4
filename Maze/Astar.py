'''
Created on Nov 14, 2013

@author: johannes
'''

class MyClass():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def heuristic(self, currentNode, endNode):
        
    
    def search(self, start, end):
        openset = set()
        closedset = set()
        current = start
        openset.add(current)
        while openset:
            current = min(openset, key=lambda o:o.g + o.h)
            if current == end:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path[::-1]#bagl�ns
            openset.remove(current)
            closedset.add(current)
            for node in self.graph[current]:
                if node in closedset:
                    continue
                if node in openset:
                    new_g = current.g + current.move_cost(node)
                    if node.g > new_g:
                        node.g = new_g
                        node.parent = current
                else:
                    node.g = current.g + current.move_cost(node)
                    node.h = self.heuristic(node, end)
                    node.parent = current
                    openset.add(node)
        return None
 
class AStarNode(object):
def __init__(self):
self.g = 0
self.h = 0
self.parent = None
def move_cost(self, other):
raise NotImplementedError