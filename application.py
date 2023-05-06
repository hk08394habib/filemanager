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

    #def moveObject:

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

    def addTags(self,*tags,nodeName):
        node = self.FS.generateNode(nodeName)
        for tag in tags:
            node.tags.append(tag)

    def removeTags(self,*tags,nodeName):
        node = self.FS.generateNode(nodeName)
        for tag in tags:
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

dut = Application()
dut.addObject("sus")
while 0 < 1:
    command = input("delete, add, moveDir, listDir: ")
    if command == "delete":
        obj = input("object name: ")
        dut.remObject(obj)
    if command == "add":
        obj = input("object name: ")
        dut.addObject(obj)
    if command == "moveDir":
        dirname = input("new dir name, or enter .. to move back: ")
        if dirname != "..":
            dut.enterDir(dirname)
        else:
            dut.exitDir()
    if command == "listDir":
        dut.FS.showTree(dut.pwd)

dut.FS.showTree(dut.FS.root)
