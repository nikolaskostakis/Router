"""
"""
from time import sleep
class GenericTreeNode:
    pass

class GenericTreeNode:
    """
    Class representing a node of a generic N-ary tree
    """

    _name:str = None
    _parent:GenericTreeNode = None
    _children:list[GenericTreeNode]

    def __init__(self, name:str, parent:GenericTreeNode = None) -> None:
        self._name = name
        self._parent = parent
        self._children = []
    # End of method

    @property
    def name(self) -> str:
        return self._name
    # End of method

    @property
    def parent(self) -> GenericTreeNode:
        return self._parent
    # End of method

    @parent.setter
    def parent(self, newParent:GenericTreeNode) -> None:
        self._parent = newParent
    # End of method

    @property
    def children(self) -> list[GenericTreeNode]:
        return self._children
    # End of method

    def add_child(self, child:GenericTreeNode) -> None:
        child.parent = self
        self._children.append(child)
    # End of method

    def remove_child(self, child:GenericTreeNode) -> bool:
        try:
            self._children.remove(child)
        except ValueError:
            return False

        return True
    # End of method
# End of class

def print_generic_tree(root:GenericTreeNode):
    def recursive_print(node:GenericTreeNode, prefix:str = ""):
        print(f"{prefix}{node.name}")
        prefix += "  "
        for child in node.children:
            recursive_print(child, prefix)
    # End of inner function

    recursive_print(root)
# End of function