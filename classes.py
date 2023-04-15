##The idea will be that we use /abc/efg/hij/kl/mno/filename.py to tell you a traversal of the directory graph from the root. Once you reach the node mno (which is a directory) we require that all children leaves will have unique names. This allows us to search (using binsearch or something) to find the Node with the name filename.py, which will return to us a Node object, which we can then use to create our position object, and which will allow for insertion, deletion, etc.



class Tree(): 
    class Position:
        def element(self): #element stored at position
            raise NotImplementedError
        def __eq__(self,other):
            raise NotImplementedError
        def __ne__(self,other):
            return not (self == other)
    

    #In what follows, p is a position, and e is an element, and t is a tree

    #These will be the public access methods we will use for the class, we leave the updating ones to be defined in the concrete class

    def root(self):
        raise NotImplementedError

    def parent(self,p):
        raise NotImplementedError

    def children(self,p):
        raise NotImplementedError

    def num_children(self,p):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def is_root(self,p):
        return (p == self.root())

    def is_leaf(self,p):
        return (self.num_children(p) == 0)

    def is_empty(self):
        return (len(self) == 0)

class DirTree(Tree):
    class _Node:
        __slots__ = '_element','_parent','_children'
        def __init__(self, element, parent=None, children=None):
            self._element = element
            self._parent = parent
            self._children = children
    class Position(Tree.Position): #We need this in order to make sure everything is valid
        def __init__(self,container,node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self,other):
            return type(other) is type(self) and other._node is self._node
    
    def _validate(self,p): #Check if position is valid, and return node
        if not isinstance(p,Position):
            raise TypeError("Not position type")
        if p._container is not self:
            raise ValueError("Wrong container")
        if p._node._parent is p._node: #We delete nodes this way, we're setting a convention
            raise ValueError("Deprecated")

        return p._node

    def _make_position(self,node): #Check if node is valid and return position
        return self.Position(self,node) if node is not None else None

    def __init__(self):
        self._root = None
        self._size = 0
    
    def __len__(self):
        return self._size

    def root(self): #return the position of root
        return self._make_position(self._root)

    def parent(self,p): #return position of parent
        node = self._validate(p) 
        return self._make_position(node._parent)

    def children(self,p): #allow to iterate over children
        node = self._validate(p)
        yield self._make_position(node._children)

    def num_children(self,p):
        count = 0
        for c in self.children(p):
            count += 1

    def _add_root(self,e):
        if self.root() is not None: raise ValueError("Already existing root")
        self._size = 1
        self._root = self._Node(e) 
        return self._make_position(self._root)

    def _add_child(self,p,e): ##TODO: implement path as a way to traverse the tree from the root node
        node = self._validate(p)
        self._size += 1
        if node._children == None:
            node._children = []
        node._children += [self._Node(e,node)]
        return self._make_position(node._left)

    def _replace(self,p,e):
        node = self._validate(p)
        old = node._element
        node._element = e
        return old
    
    def _delete(self,p): ##TODO
        node = self._validate(p)
        self._size -= 1 ##num elements

    def _attach(self,p,t):
        node = self._validate(p)
        if not self.is_leaf(p): raise ValueError('Position must be a leaf')
        if not type(self) is type(t):
            raise TypeError('Tree types must match')
        self._size += len(t)
        if not t.is_empty():
            t._root._parent = node
            t._root = None
            t._size = 0 











