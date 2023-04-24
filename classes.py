##The idea will be that we use /abc/efg/hij/kl/mno/filename.py to tell you a traversal of the directory graph from the root. Once you reach the node mno (which is a directory) we require that all children leaves will have unique names. This allows us to search (using binsearch or something) to find the Node with the name filename.py, which will return to us a Node object, which we can then use to create our position object, and which will allow for insertion, deletion, etc.
import re
import os
import hashlib

print(os.getcwd())

class Path():
    def __init__(self,path):
        self.path = path
    
    def directoryPath(self):
        newpath = path[:]
        newpath = newpath.split("/")
        return newpath[-1]


class Dir():
    def __init__(self,element,parent=None,children=None):
        self.parent = parent
        self.children = children
        self.element = element
        if children == None and ("." not in element):
            self.children = []
        if parent == None:
            self.parent = ""
    def __str__(self):
        showForParent = self.parent.element if self.element != "~" else "None"
        return f"\n------ \n{self.parent}\n\t{self.element}\n{self.children} \n------\n"

class File():
    def __init__(self,element,parent=None,children=None):
        self.parent = parent
        self.element = element
        if parent == None:
            self.parent = ""
    def __str__(self):
        showForParent = self.parent.element if self.element != "~" else "None"
        return f"\n------ \n{self.parent}\n\t{self.element}\n \n------\n"


class Tree(): #TODO: base this on the path object
    def __init__(self,root=os.getcwd()):
        self.rootpath = root
        self.root = Dir(root)
        self.paths = {hashlib.md5(self.rootpath.encode()).hexdigest() : self.root}
        self.generateRepresentation()

    def hashPath(self,path):
        return hashlib.md5(path.encode()).hexdigest()

    def generateRepresentation(self): #using BFS generate an internal representation of the Directory Tree
        level = [os.getcwd()+ "/"  + x for x in os.listdir()]
        while len(level) > 0:
            next_level = []
            for unexploredPath in level:
                thisNodesContribution = []
                print(unexploredPath)
                pathToParent = '/'.join(unexploredPath.split("/")[:-1])
                unexploredNodeName = unexploredPath.split("/")[-1]
                print(pathToParent, unexploredNodeName)
                self.attach(pathToParent, unexploredNodeName)
                if "." not in unexploredNodeName:
                    os.chdir(unexploredPath)
                    unexploredDir = unexploredNodeName
                    thisNodesContribution = [os.getcwd()+ "/"  + x for x in os.listdir()]
                    next_level += thisNodesContribution
            level = next_level


    def attach(self,pathToParent,child):
        parentNode = self.paths[self.hashPath(pathToParent)] 
        if "." in child:
            childNode = File(child,parentNode,children=None)
        else:
            childNode = Dir(child,parentNode,children=None)
        parentNode.children.append(childNode)
        childPath = pathToParent + "/" + child
        self.paths[hashlib.md5((childPath).encode()).hexdigest()] = childNode
    

    def delete(self,pathToNode):
        hashedPath = self.hashPath(pathToNode)
        node = self.paths[hashedPath]
        node.parent.children.remove(node)
        del self.paths[hashedPath]
        return node

    def move(self,startPath,endPath): ##work in progress
        node = self.delete(startPath)
        self.attatch(endPath,node)

    #def rename


    def showTree(self,startNode,depth=1):
        print("-" * depth + startNode.element,end=" ")
        if isinstance(startNode,File):
            print("F")
        if isinstance(startNode,Dir):
            print("D")
            children = startNode.children
            depth = depth + 1
            for child in children:
                self.showTree(child, depth = depth)

DirTree = Tree()
DirTree.showTree(DirTree.root)
DirTree.delete(DirTree.rootpath + "/" + "smalltest.txt")
DirTree.showTree(DirTree.root)
