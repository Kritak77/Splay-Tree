from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# DO NOT MODIFY!
class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)

    # Search
    def search(self, key: int):
        self.root = self._splay(self.root, key)

    # Insert Method 1
    def insert(self, key: int):
        if self.root is None:
            self.root = Node(key)
            return
        
        self.root = self._splay(self.root, key)
        if key == self.root.key:
            return  # Key already exists

        new_node = Node(key)
        if key < self.root.key:
            new_node.rightchild = self.root
            new_node.rightchild.parent = new_node
            new_node.leftchild = self.root.leftchild
            if new_node.leftchild is not None:
                new_node.leftchild.parent = new_node
            self.root.leftchild = None
            
        else:  # key > self.root.key
            new_node.leftchild = self.root
            new_node.leftchild.parent = new_node
            new_node.rightchild = self.root.rightchild
            if new_node.rightchild is not None:
                new_node.rightchild.parent = new_node
            self.root.rightchild = None

        self.root = new_node

    def _splay(self, node: Node, key: int) -> Node:
        y = node
        x = None

        while y is not None:
            x = y
            if key == y.key:
                break
            elif key < y.key:
                y = y.leftchild
            else:
                y = y.rightchild
        while x.parent is not None:
            if x.parent.parent is None:
                if x == x.parent.leftchild:
                    # zig rotation
                    self._rotate_right(x)
                else:
                    # zag rotation
                    self._rotate_left(x)
            elif x == x.parent.leftchild and x.parent == x.parent.parent.leftchild:
                # zig-zig rotation
                self._rotate_right(x.parent)
                self._rotate_right(x)
            elif x == x.parent.rightchild and x.parent == x.parent.parent.rightchild:
                # zag-zag rotation
                self._rotate_left(x.parent)
                self._rotate_left(x)
            elif x == x.parent.rightchild and x.parent == x.parent.parent.leftchild:
                # zig-zag rotation
                self._rotate_left(x)
                self._rotate_right(x)
            else:
                # zag-zig rotation
                self._rotate_right(x)
                self._rotate_left(x)

        return x

    def _rotate_right(self, node: Node) -> Node:
        root = node.parent
        if root.parent:
            if node.key > root.parent.key:
                root.parent.rightchild = node
            else:
                root.parent.leftchild = node
        node.parent = root.parent
        root.parent = node
        root.leftchild = node.rightchild
        if root.leftchild:
            root.leftchild.parent = root
        node.rightchild = root

    def _rotate_left(self, node: Node) -> Node:
        root = node.parent
        if root.parent:
            if node.key > root.parent.key:
                root.parent.rightchild = node
            else:
                root.parent.leftchild = node
        node.parent = root.parent
        root.parent = node
        root.rightchild = node.leftchild
        if root.rightchild:
            root.rightchild.parent = root
        node.leftchild = root
        
        # Delete Method 1
    def delete(self,key:int):
        if self.root is None:
            return

        self.root = self._splay(self.root, key)

        if key != self.root.key:
            return

        if self.root.leftchild is None:
            self.root = self.root.rightchild
            if self.root:
                self.root.parent = None
        elif self.root.rightchild is None:
            self.root = self.root.leftchild
            if self.root:
                self.root.parent = None
        else:
            right_min = self.root.rightchild
            while right_min.leftchild:
                right_min = right_min.leftchild
            right_min = self._splay(self.root.rightchild, right_min.key)
            right_min.leftchild = self.root.leftchild
            self.root.leftchild.parent = right_min
            self.root = right_min
            

        
