from abc import *


class Visitor(metaclass=ABCMeta):
    """
    Abstract visitor class for traversing visitable components
    """
    @abstractmethod
    def visit(self, element):
        """
        Visits an element
        :param element: Some Visitable element
        :return: Should return True or None to continue traversal, False to stop early
        """
        pass


class Visitable:
    """
    Abstract visitable class that allows traversal by a visitor
    """
    def accept(self, visitor):
        """
        Accepts a visitor and passes itself to the visitor's visit function
        :param visitor: Visitor object
        :return: Return value from visitor's visit function
        """
        return visitor.visit(self)


class VisitableComposite(Visitable):
    """
    Abstract visitable class which has visitable children
    :param children: list of visitable children of this node
    """
    def __init__(self, children=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = children or []

    def accept(self, visitor):
        """
        Accepts a visitor to this node and then its children (pre-order traversal). Stops traversal prematurely if visit
        function returns False
        :param visitor: Visitor object
        :return: False if the visit function returned false at any point, otherwise True or None
        """
        ret = super().accept(visitor)
        # if return is None or True
        if ret is None or ret:
            for child in self.children:
                ret = child.accept(visitor)
                # if return is False
                if ret is not None and not ret:
                    break
        return ret

    def add_child(self, child):
        """
        Adds a visitable child to this node's list of children
        :param child: Visitable component
        """
        self.children.append(child)

    def remove_child(self, child):
        """
        Removes a child from this component
        :param child: Visitable child to remove
        """
        self.children.remove(child)