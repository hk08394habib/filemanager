##The idea will be that we use /abc/efg/hij/kl/mno/filename.py to tell you a traversal of the directory graph from the root. Once you reach the node mno (which is a directory) we require that all children leaves will have unique names. This allows us to search (using binsearch or something) to find the Node with the name filename.py, which will return to us a Node object, which we can then use to create our position object, and which will allow for insertion, deletion, etc.
import re
import os
import hashlib



class Dir():
    def __init__(self,element,path,parent=None,children=None):
        self.parent = parent
        self.children = children
        self.element = element
        self.path = path

        self.size = None #os.path.getsize(self.path)
        self.lastAccessed = None #os.path.getmtime(self.path)
        self.creationTime = None # os.path.getctime(self.path)
    
        self.isDir = True
        self.isFile = False

        self.tags = []

        if children == None: 
            self.children = []
        if parent == None:
            self.parent = ""

    def __str__(self):
        return f"\n------ \n{self.parent}\n\t{self.element}\n{self.children} \n------\n"

class File():
    def __init__(self,element,path,parent=None,children=None):
        self.parent = parent
        self.element = element
        self.path = path

        #self.size = os.path.getsize(self.path)
        #self.lastAccessed = os.path.getmtime(self.path)
        #self.creationTime = os.path.getctime(self.path)

        self.isDir = False
        self.isFile = True

        self.tags = []

        if parent == None:
            self.parent = ""

    def __str__(self):
        showForParent = self.parent.element if self.element != "~" else "None"
        return f"\n------ \n{self.parent}\n\t{self.element}\n \n------\n"


class DirTree(): #TODO: base this on the path object
    def __init__(self,root=os.getcwd()):
        self.root = Dir("",root)
        self.paths = {root : self.root}
        self.generateTree()
        self.showTree(self.root)

    def hashPath(self,path): 
        return hashlib.md5(path.encode()).hexdigest()

    def generateNode(self,path):
        return self.paths[path]

    def generatePath(self,node):
        return self.node.path

    def not_in_tree(self,path):
        try:
            self.paths[path]
            return False
        except:
            return True




    def generateTree(self): #using BFS generate an internal representation of the Directory Tree
        level = [os.path.join(os.getcwd(), x) for x in os.listdir()]
        while len(level) > 0:
            next_level = []
            for unexploredPath in level:
                thisNodesContribution = []
                pathToParent = os.path.dirname(unexploredPath)
                unexploredNodeName = os.path.basename(unexploredPath)
                print(unexploredPath)
                self.addPath(pathToParent, unexploredNodeName)
                if "." not in unexploredNodeName and unexploredNodeName != "kivy_venv" and unexploredNodeName[0] != ".":
                    unexploredDir = unexploredNodeName
                    thisNodesContribution = [os.path.join(unexploredPath, x) for x in os.listdir(unexploredPath) if self.not_in_tree(os.path.join(unexploredPath,x))]
                    next_level += thisNodesContribution
            level = next_level

    def searchTree(self,nodeName):
        level = [child.path for child in self.root.children]
        while len(level) > 0:
            next_level = []
            for path in level:
                childname = os.path.basename(path)
                newpath = os.path.dirname(path)
                if nodeName == childname:
                    print(path)
                #print(pathToParent, unexploredNodeName)
                if "." not in childname:
                    thisChild = self.generateNode(path)
                    addition = [child.path for child in thisChild.children]
                    next_level += (addition)
            level = next_level


    def addPath(self,pathToParent,childName): #TODO:only add path if it is in Dir
        #parentNode = self.paths[self.hashPath(pathToParent)] 
        parentNode = self.generateNode(pathToParent)
        childPath = pathToParent + "/" + childName
        try: 
            self.paths[childPath]
        except:
            if "." in childName:
                childNode = File(childName,childPath,parent=parentNode,children=None)
            else:
                childNode = Dir(childName,childPath,parent=parentNode,children=None)
            parentNode.children.append(childNode)
            self.paths[childPath] = childNode
    

    def popPath(self,pathToDir,nodeName):
        #hashedPath = self.hashPath(pathToNode)
        #print("here")
        #print(pathToNode)
        pathToNode = os.path.join(pathToDir, nodeName)
        node = self.generateNode(pathToNode)
        #print(node.element)
        #print(node)
        if node.parent == "":
            print("Error, can not delete root")
            return 
        try:
            node.parent.children.remove(node)
        except:
            pass
        del self.paths[pathToNode]
        return node

    def move(self,startPath,endPath,file): ##work in progress
        node = self.popPath(startPath,file)
        pathToNode = os.path.join(startPath, file)
        newParent = self.generateNode(endPath)
        try: 
            self.paths[pathToNode]
        except:
            if "." in file:
                newNode = File(node.element,node.path,parent=newParent)
            else:
                newNode = Dir(node.element,node.path,parent=newParent,children=node.children)
            newParent.children.append(node)
            self.paths[pathToNode] = node

    def showTree(self,startNode,depth=1):
        print("-" * depth + startNode.element,end=" ")
        if isinstance(startNode,File):
            print("F", startNode.tags)
        if isinstance(startNode,Dir):
            print("D", startNode.tags)
            children = startNode.children
            depth = depth + 1
            for child in children:
                self.showTree(child, depth = depth)



