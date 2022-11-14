import ast
from ast import *
from typing import Any
import inspect

class ASTNestedForCounter(NodeVisitor):

    def __init__(self) -> None:
        super().__init__()
        self._max_count = 0

    def visit(self, node: AST) -> Any:
        self._max_count = 0
        return super().visit(node)

    def generic_visit(self, node: AST) -> Any:
        for _,value in iter_fields(node):
            if isinstance(value,list):
                for item in value:
                    val = self.visit(item)
                    if val > self._max_count:
                        self._max_count = val
            elif isinstance(value,AST):
                self.visit(value)
        return self._max_count
                
    def visit_For(self, node) -> int:
        return 1 + self.generic_visit(node)
    

class ASTDotVisitor(NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.state_count = 0

    def generic_visit(self, node: AST) -> Any:
        string,node_id= self.dot_state(node)
        interior = ""
        for field,value in iter_fields(node):
            if isinstance(value,list):
                for item in value:
                    s_id = self.visit(item)
                    print(node_id+ " -> " + s_id + "[label=\"%s\"]" % (field))
            elif isinstance(value,AST):
                s_id = self.visit(value)
                print(node_id+ " -> " + s_id + "[label=\"%s\"]" % (field))
            else:
                interior += "\"%s\"=%s " % (field,value)
        string = string % interior
        print(string)
        return node_id

    
    def dot_state(self,node:AST):
        x = str(type(node).__name__) + "(%s)"
        node_id = "s%d" % (self.state_count)
        string = 's%d[label="%s", shape=box]' % (self.state_count, x)
        self.state_count += 1
        return string,node_id
