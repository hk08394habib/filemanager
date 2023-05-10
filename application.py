import os
import re
import shutil
import hashlib


#Tree

##The idea will be that we use /abc/efg/hij/kl/mno/filename.py to tell you a traversal of the directory graph from the root. Once you reach the node mno (which is a directory) we require that all children leaves will have unique names. This allows us to search (using binsearch or something) to find the Node with the name filename.py, which will return to us a Node object, which we can then use to create our position object, and which will allow for insertion, deletion, etc.

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

        self.size = None #os.path.getsize(self.path)
        self.lastAccessed = None #os.path.getmtime(self.path)
        self.creationTime = None #os.path.getctime(self.path)

        self.isDir = False
        self.isFile = True

        self.tags = []

        if parent == None:
            self.parent = ""

    def __str__(self):
        showForParent = self.parent.element if self.element != "~" else "None"
        return f"\n------ \n{self.parent}\n\t{self.element}\n \n------\n"


class DirTree(): 
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
                    node = self.generateNode(unexploredPath)
                    thisNodesContribution = [os.path.join(unexploredPath, x) for x in node.children if self.not_in_tree(os.path.join(unexploredPath,x))]
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


    def addPath(self,pathToParent,childName):
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





#App


class Application():
    def __init__(self):
        self.FS = DirTree()
        self.pwd = self.FS.root
        self.pwdPath = self.FS.root.path
        self.addObject("deleted")
        self.deleted = os.path.join(self.FS.root.path, "deleted")

    #def searchFS: Will search both with tag and name

    def enterDir(self, dirName):
        directory = self.FS.generateNode(os.path.join(self.pwdPath, dirName))
        self.pwd = directory
        self.pwdPath = directory.path

    def exitDir(self):
        self.pwd = self.pwd.parent
        self.pwdPath = self.pwd.path

    def searchTree(self,nodeName):
            self.FS.searchTree(nodeName)

    def openFile(self,nodeName):
        node = self.FS.generateNode(nodeName)
        if node.isFile == True:
            os.startfile(nodeName)

    def retrieveInfo(self, nodeName):
        node = self.FS.generateNode(nodeName)
        return [node.tags,node.size,node.lastAccessed,node.creationTime]

    def addTag(self,tag,nodeName):
        path = os.path.join(self.pwdPath, nodeName)
        node = self.FS.generateNode(path)
        node.tags.append(tag)

    def removeTag(self,tag ,nodeName):
        path = os.path.join(self.pwdPath, nodeName)
        node = self.FS.generateNode(path)
        node.tags.remove(tag)

    #def Compress

    #def Decompress

    def addObject(self, nodeName):
        print(nodeName)
        print(self.pwdPath)
        self.FS.addPath(self.pwdPath,nodeName)
        childPath = os.path.join(self.pwdPath, nodeName)
        if "." not in nodeName:
            try:
               os.mkdir(childPath)
            except:
                pass
        else:
            try:
                fp = open(childPath,"x")
                fp.close()
            except:
                pass

    def remObject(self,nodeName):
        childPath = os.path.join(self.pwdPath, nodeName)
        try:
            shutil.move(childPath,self.deleted)
            self.FS.move(self.pwdPath,self.deleted,nodeName)
            self.FS.popPath(self.pwdPath,nodeName)
        except:
            pass

    def moveObject(self,nodeName, resultPath): #result path is relative to current root
        path = os.path.join(self.pwdPath, nodeName)
        finalPath = os.path.join(self.FS.root.path, resultPath)
        try:
            shutil.move(path,finalPath)
            self.FS.move(self.pwdPath,finalPath,nodeName)
            self.FS.popPath(self.pwdPath,nodeName)
        except:
            pass





#GUI

import tkinter as tk
from tkinter import filedialog

class ApplicationGUI():
    def __init__(self, master):
        self.master = master
        master.title("File System")

        self.app = Application()

        # Create buttons
        self.add_button = tk.Button(master, text="Add", command=self.add_object)
        self.delete_button = tk.Button(master, text="Delete", command=self.rem_object)
        self.move_button = tk.Button(master, text="Move", command=self.move_object)
        self.enter_button = tk.Button(master, text="Enter", command=self.enter_dir)
        self.search_button = tk.Button(master, text="Search", command=self.search_tree)
        self.show_button = tk.Button(master, text="Show", command=self.show_tree)

        # Create labels and text boxes
        self.object_label = tk.Label(master, text="Object name:")
        self.object_text = tk.Entry(master)
        self.tag_label = tk.Label(master, text="Tag:")
        self.tag_text = tk.Entry(master)

        # Layout widgets using grid
        self.add_button.grid(row=0, column=0)
        self.delete_button.grid(row=0, column=1)
        self.move_button.grid(row=0, column=2)
        self.enter_button.grid(row=1, column=0)
        self.search_button.grid(row=1, column=1)
        self.show_button.grid(row=1, column=2)

        self.object_label.grid(row=2, column=0)
        self.object_text.grid(row=2, column=1)
        self.tag_label.grid(row=3, column=0)
        self.tag_text.grid(row=3, column=1)

    def add_object(self):
        name = self.object_text.get()
        self.app.addObject(name)

    def rem_object(self):
        name = self.object_text.get()
        self.app.remObject(name)

    def move_object(self):
        name = self.object_text.get()
        path = filedialog.askdirectory()
        self.app.moveObject(name, path)

    def enter_dir(self):
        name = self.object_text.get()
        if name == "..":
            self.app.exitDir()
        else:
            self.app.enterDir(name)

    def search_tree(self):
        name = self.object_text.get()
        self.app.searchTree(name)

    def show_tree(self):
        self.app.FS.showTree(self.app.pwd) 

cliorgui = input("cli/gui: ")
if cliorgui == "gui":
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()
else:
    dut = Application()
    dut.FS.showTree(dut.FS.root)
    while 0 < 1:
         command = input("Give me a command: (h for help) ").split(" ")

         action = command[0]
         try:
             obj = command[1]
         except:
             obj = None
         try:
             tag = command[2]
         except:
             tag = []
         if action == "delete":
             dut.remObject(obj)
         if action == "add":
             dut.addObject(obj)
         if action == "h":
             print("\n\nAvailable list of commands:\n")
             print("\tdelete, deletes a node from filesystem\n")
             print("\tadd, adds a node to filesystem\n")
             print("\tmove, deletes a node to a path in filesystem\n")
             print("\taddTag, adds a tag to a node\n")
             print("\tremoveTag, removes a tag from a node\n")
             print("Command usage: command node endpath/tag\n")
         if action == "move":
             dut.moveObject(obj,tag)

         if action == "addTag":
             dut.addTag(tag,obj)
         if action == "removeTag":
             dut.removeTag(tag,obj)
         if action == "enter":
             if obj != "..":
                dut.enterDir(obj)
             else:
                 dut.exitDir()
         if action == "show":
             dut.FS.showTree(dut.pwd)
         if action == "open":
             dut.openFile(obj)
         if action == "search":
             dut.searchTree(obj)
         if action == "exit":
             break
               


