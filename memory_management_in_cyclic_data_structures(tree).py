from typing import List, Dict, Optional
import weakref

"""
A simple example of a cyclic data structure is a tree structure where a parent points to
its children and the children point back to their parent. For code like this, you should
consider making one of the links a weak reference using the weakref library. For
example:
"""


class Node:
    def __init__(self, id_: int, title: str, parent_id: Optional[int]):
        self.id = id_
        self.title = title
        self.parent_id = parent_id
        self._parent = None
        self.children = []

    def __repr__(self):
        return 'Node(id={!r:}, title={!r:})'.format(self.id, self.title)

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

    # property that manages the parent as a weak-reference
    @property
    def parent(self):
        return self._parent if self._parent is None else self._parent()

    @parent.setter
    def parent(self, node_: Node):
        self._parent = weakref.ref(node_)

    def add_child(self, node_: Node):
        self.children.append(node_)
        node_.parent = self


class Tree:
    def __init__(self, items: List[Dict]) -> None:
        self.nodes = []

        for item in items:
            self.create_node(item)

        self.populate_children()

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def create_node(self, item: Dict) -> Node:
        """
        Create `Node` instance from `Dict`
        """
        n = Node(
            id_=item.get('id'),
            title=item.get('title'),
            parent_id=item.get('parent_id')
        )
        self.nodes.append(n)
        return n

    def populate_children(self) -> None:
        """
        Populates children for all nodes
        """
        for n in self.nodes:
            children = filter(lambda x: x.parent_id == n.id, self.nodes)
            for child in children:
                n.add_child(child)

    @staticmethod
    def descendants(n: Node) -> List:
        """
        All child nodes and all their child nodes.
        """
        children = n.children.copy()

        # first variant
        stack = [children]
        while stack:
            children = stack[-1]
            if children:
                child = children.pop(0)
                yield child
                if child.children:
                    stack.append(child.children)
            else:
                stack.pop()

        # second variant
        # for child in children:
        #     yield child
        #     children.extend(n.children)

    @staticmethod
    def ancestors(n: Node) -> List:
        """
        All parent nodes and their parent nodes - see :any:`ancestors`.
        """
        parents = []
        node_ = n
        while node_:
            node_ = node_.parent
            parents.insert(0, node)
            # parents.append(node)
        return parents

    @staticmethod
    def children(n: Node) -> List:
        """
        All child nodes.
        """
        return n.children

    def root(self, n: Node) -> Optional[int]:
        """
        Tree Root Node.
        """
        ancestors = self.ancestors(n)
        return ancestors[0] if ancestors else []
        # return ancestors[-1] if ancestors else []


data = [
  {'id': 1, 'title': 'Category #1', 'parent_id': None},
  {'id': 2, 'title': 'Category #2', 'parent_id': None},
  {'id': 3, 'title': 'Category #3', 'parent_id': 1},
  {'id': 4, 'title': 'Category #4', 'parent_id': 2},
  {'id': 5, 'title': 'Category #5', 'parent_id': 3},
  {'id': 6, 'title': 'Category #6', 'parent_id': 4},
  {'id': 7, 'title': 'Category #7', 'parent_id': 6},
  {'id': 8, 'title': 'Category #8', 'parent_id': 5},
  {'id': 9, 'title': 'Category #9', 'parent_id': 5}
]

tree = Tree(items=data)

if __name__ == '__main__':
    print(tree.nodes)
    for node in tree.nodes:
        print(node)
        print(node.children)
    # solver.ancestors(5)  # [3, 1]
    # solver.descendants(2)  # [4, 6, 7]
    # solver.children(6)  # [7]
    # solver.root(8)  # 1
    # print('Children for 6:', solver.children(6))
    # print('Root for 8:', solver.root(8))
    # print('Ancestors for 5:', solver.ancestors(5))
    # print('Descendants for 2:', solver.descendants(2))