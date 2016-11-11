import unittest
from backend.abstract import visitor


class TestVisitor(visitor.Visitor):
    def __init__(self, stop=None):
        self.stop = stop
        self.visited = []

    def visit(self, element):
        if not self.stop or element.value < self.stop:
            self.visited.append(element.value)


class TestVisitable(visitor.VisitableComposite):
    def __init__(self, val, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = val


class VisitorTestCase(unittest.TestCase):
    def test_visit(self):
        root = TestVisitable(1)
        root.add_child(TestVisitable(2))
        root.add_child(TestVisitable(3))
        root.add_child(TestVisitable(4))
        visit_all = TestVisitor()
        root.accept(visit_all)
        assert visit_all.visited == [1, 2, 3, 4]
        visit_some = TestVisitor(3)
        root.accept(visit_some)
        assert visit_some.visited == [1, 2]
