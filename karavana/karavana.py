from __future__ import annotations

import collections.abc as abcs
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional


class Display(Enum):
    COLLECTION = auto()


@dataclass
class Node:
    value: Display
    children: Optional[Node] = field(default_factory=list)

    def add_child(self, child):
        self.children.append(child)


@dataclass
class ConnectedNode:
    lhs: Any
    rhs: Any


class Viz:
    typeregs = {}

    def visit(self, obj):
        for abc, viz in self.typeregs.items():
            if isinstance(obj, abc):
                return viz(self, obj)
        else:
            return obj

    @classmethod
    def register(cls, protocol, attr):
        def wrapper(func):
            cls.typeregs[getattr(protocol, attr)] = func
            return func

        return wrapper


@Viz.register(abcs, "Mapping")
def mapping(self, obj):
    node = Node(Display.COLLECTION)
    for key, value in obj.items():
        child = ConnectedNode(self.visit(key), self.visit(value))
        node.add_child(child)
    return node


viz = Viz()
node = viz.visit({1: 1, 2: 2, 3: {1: 2}})
print(node)
