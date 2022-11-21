import ast
from ast import *
import copy
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
        self.depth = 0

    def generic_visit(self, node: AST) -> Any:
        self.depth += 1

        string,node_id= self.dot_state(node)
        interior = ""
        comma_counter = 0
        for field,value in iter_fields(node):
            if isinstance(value,list):
                for item in value:
                    s_id,s_string = self.visit(item)
                    # print(node_id+ " -> " + s_id + "[label=\"%s\"]" % (field))
                    string += "\n" + node_id + " -> " + s_id + "[label=\"%s\"]\n" % (field) + s_string
            elif isinstance(value,AST):
                s_id,s_string = self.visit(value)
                # print(node_id+ " -> " + s_id + "[label=\"%s\"]" % (field))
                string += "\n" + node_id + " -> " + s_id + "[label=\"%s\"]\n" % (field) + s_string
            else:
                if comma_counter == 0:
                    interior += "%s=%s" % (field,value)
                else:
                    interior += ", %s=%s" % (field,value)
                comma_counter += 1
        string = string % interior

        #print(string)
        self.depth -= 1

        if self.depth == 0:
            string = "digraph {\n" + string + "\n}"
            f = open("graphic.dot","w")
            f.write(string)
            f.close()
        else:
            return node_id, string

    
    def dot_state(self,node:AST):
        x = str(type(node).__name__) + "(%s)"
        node_id = "s%d" % (self.state_count)
        string = 's%d[label="%s", shape=box]' % (self.state_count, x)
        self.state_count += 1
        return string,node_id

class ASTReplaceVar(NodeTransformer):
    def __init__(self, name_var:str, replacement: AST) -> None:
        super().__init__()
        self.name_var = name_var
        self.replacement = replacement
    
    def visit_Name(self, node: Name) -> Any:
        # Sustituimos si tiene el nombre y es en contexto de carga
        if self.name_var == node.id and isinstance(node.ctx,ast.Load):
            return self.replacement
        return node

class ASTUnroll(NodeTransformer):

    def visit_For(self, node: For) -> Any:
        if isinstance(node.target,ast.Name):
            if isinstance(node.iter, ast.List):
                # De momento solo se carga al for
                new_body = list()

                for elem in node.iter.elts:
                    ncopy = copy.deepcopy(node)
                    repl = ASTReplaceVar(node.target.id,elem)
                    repl.visit(ncopy)
                    new_body.extend(ncopy.body)
                
                extended_body = list()
                for elem in new_body:
                    extended_body.append(self.visit(elem))
                
                return extended_body
        return node