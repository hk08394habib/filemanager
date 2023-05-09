from tree import DirTree
import os
import shutil

class Application(): 
    def __init__(self):
        self.FS = DirTree()
        self.pwd = self.FS.root
        self.pwdPath = self.FS.root.path
        self.addObject("deleted")
        self.deleted = self.pwdPath + "/deleted"

    #def searchFS: Will search both with tag and name

    def enterDir(self, dirName):
        directory = self.FS.generateNode(self.pwdPath + "/" + dirName)
        self.pwd = directory
        self.pwdPath = directory.path


    def exitDir(self):
        self.pwd = self.pwd.parent
        self.pwdPath = self.pwd.path

    def openFile(self,nodeName):
        node = self.FS.generateNode(nodeName)
        if node.isFile == True:
            os.startfile(nodeName)


    def retrieveInfo(self, nodeName):
        node = self.FS.generateNode(nodeName)
        return [node.tags,node.size,node.lastAccessed,node.creationTime]

    def addTag(self,tag,nodeName):
        path = self.pwdPath + "/" + nodeName
        node = self.FS.generateNode(path)
        node.tags.append(tag)

    def removeTag(self,tag ,nodeName):
        path = self.pwdPath + "/" + nodeName
        node = self.FS.generateNode(path)
        node.tags.remove(tag)

    #def Compress

    #def Decompress


    def addObject(self, nodeName): 
        print(nodeName)
        print(self.pwdPath)
        self.FS.addPath(self.pwdPath,nodeName)
        childPath = self.pwdPath + "/" + nodeName
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
        childPath = self.pwdPath + "/" + nodeName
        try:
            shutil.move(childPath,self.deleted)
            self.FS.move(self.pwdPath,self.deleted,nodeName)
            self.FS.popPath(self.pwdPath,nodeName)
        except:
            pass

    def moveObject(self,nodeName, resultPath): #result path is relative to current root
        path = self.pwdPath + "/" + nodeName
        finalPath = self.FS.root.path + "/" + resultPath  
        try:
            shutil.move(path,finalPath)
            self.FS.move(self.pwdPath,finalPath,nodeName)
            self.FS.popPath(self.pwdPath,nodeName)
        except:
            pass




dut = Application()
dut.addObject("sus")
while 0 < 1:
    command = input("delete, add, moveDir, listDir, addTag, removeTag,exit and the obj name ").split(" ")
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
    if action == "exit":
        break

dut.FS.showTree(dut.FS.root)
