
### This file contains the required class implementations for data structures

class tree(): 
    def __init__(self,nodes = [],edges=[]):
        self.graph = {}
        for node in nodes:
            self.graph[nodes] = edges
    def _addNode(self,node):
        self.graph[node] = []
    def _addEdge(self,edge):
        self.graph[edge[0]] += (edge,) #give both edges
        self.graph[edge[1]] += (edge[::-1][1:] + (-1 * edge[2],),) #reverse first two elements, keep weight the same but negative
    def addChild(self,parent,child,weight):
        self._addNode(child)
        self._addEdge((parent,child,weight))
    def getParent(self,node):
        for x in self.graph[node]:
            if x[2] < 0:
                return x[1]
        raise Exception("Node is parent")
    def removeNode(self,node):
        parent = self.getParent(node)
        parentlist = self.graph[parent] 
        for index in range(len(parentlist)-1): #remove child reference from parent
            if parentlist[index][1] == node:
                parentlist.pop(index)
        self.graph.pop(node)

    def iter(self):
        return list(self.graph.items())

    def BFS(): #To be implemented
        pass
    def DFS(): #To be implemented
        pass
    def INORDER(): #To be implemented
        pass


class ht():
    def __init__(self,size):
        self.size = size
        self.keys = [None] * self.size 
        self.values = [None] * self.size
        self.contained = 0 
    
    def put(self,key,value):
        if self.contained >= 2 * self.size // 3:
           self.resize()
        i = 0 
        hashval = self.hashfunction(key)
        rehashval = self.rehashfunction(hashval,i) 
        while i < self.size:
            rehashval = self.rehashfunction(key,i)
            if self.keys[rehashval] == None:
                self.keys[rehashval] = key
                self.values[rehashval] = value
                break
            i += 1
    def resize(self):
        new_ht = ht(3 * self.size)
        for x in range(self.size):
          key = self.keys[x]
          value = self.values[x]
          if key != None:
            new_ht.put(key,value)

        self.size = new_ht.size
        self.keys = new_ht.keys
        self.values = new_ht.values
        self.contained = new_ht.contained

    def get(self,key):
       i = 0 
       hashval = self.hashfunction(key)
       rehashval = self.rehashfunction(hashval,i) 
       while i < self.size:
          rehashval = self.rehashfunction(key,i)
          if self.keys[rehashval] == key:
            return self.values[rehashval] 
          i += 1
    def show(self):
       print(self.keys)
       print(self.values)       
    def hashfunction(self,key):
      return key % self.size
    def rehashfunction(self,key, i):
      return self.hashfunction(key+i)






        



