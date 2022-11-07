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
        for field,value in iter_fields(node):
            if isinstance(value,list):
                for item in value:
                    if isinstance(item,ast.For):
                        val = self.visit_For(item)
                        if val > self._max_count:
                            self._max_count = val
                    elif isinstance(item,AST):
                        self.visit(item)
            elif isinstance(value,AST):
                self.visit(value)
        return self._max_count
                
    def visit_For(self, node) -> int:
        return 1 + self.generic_visit(node)
    

