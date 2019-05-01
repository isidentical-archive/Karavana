from __future__ import annotations

import collections.abc as abcs
from dataclasses import dataclass, field
from enum import Enum, auto
from io import StringIO
from typing import Any, Optional

class Display(Enum):
    COLLECTION = auto()


@dataclass
class Node:
    display: Display
    children: Optional[Node] = field(default_factory=list)

    def add_child(self, child):
        self.children.append(child)

@dataclass
class KVNode:
    lhs: Any
    rhs: Any

@dataclass
class LinkedNode:
    prev: Optional[LinkedNode]
    value: Any
    
    def __str__(self):
        return f"{value} ->"
    
class Viz:
    typeregs = {}

    def visit(self, obj):
        for abc, viz in self.typeregs.items():
            if isinstance(obj, abc):
                return viz(self, obj)
        else:
            return obj

    @classmethod
    def register(cls, protocol, attr = None):
        def wrapper(func):
            cls.typeregs[getattr(protocol, attr) if attr else protocol] = func
            return func

        return wrapper


@Viz.register(abcs, "Mapping")
def mapping(self, obj):
    node = Node(Display.COLLECTION)
    for key, value in obj.items():
        child = KVNode(self.visit(key), self.visit(value))
        node.add_child(child)
    return node

@Viz.register((str, bytes))
def string(self, obj):
    return obj

@Viz.register(abcs, "Iterable")
def sequence(self, obj):
    node = Node(Display.COLLECTION)
    prev = None
    for item in obj:
        child = LinkedNode(prev, item)
        node.add_child(child)
        prev = child
    return node


viz = Viz()
node = viz.visit({
    'meta': {
        'imports': [1, 2, 3],
        'forbids': (1, 2),
        'test': 3, 
        'instrs': {'a', 'b'}
    },
    'teta': {
        'x': 'y'
    },
    (1, 2): 'a'
})

