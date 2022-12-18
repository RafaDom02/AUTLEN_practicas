import ast
from ast import NodeVisitor, NodeTransformer, AST, iter_fields, Name, For
import copy
from typing import Any


class ASTNestedForCounter(NodeVisitor):
    def generic_visit(self, node: AST) -> Any:
        max_count = 0
        for _, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    val = self.visit(item)
                    if val > max_count:
                        max_count = val
            elif isinstance(value, AST):
                val = self.visit(value)
                if val > max_count:
                    max_count = val

        return max_count

    def visit_For(self, node) -> int:
        return 1 + self.generic_visit(node)


class ASTDotVisitor(NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.state_count = 0
        self.depth = 0

    def generic_visit(self, node: AST) -> Any:
        self.depth += 1

        string, node_id = self.dot_state(node)
        interior = ""
        comma_counter = 0
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    s_id, s_string = self.visit(item)

                    # Añadimos la transición a la lista + descripción del subárbol
                    string += "\n" + node_id + " -> " + s_id + \
                        "[label=\"%s\"]\n" % (field) + s_string
            elif isinstance(value, AST):
                s_id, s_string = self.visit(value)

                # Añadimos la transición a la lista + descripción del subárbol
                string += "\n" + node_id + " -> " + s_id + \
                    "[label=\"%s\"]\n" % (field) + s_string
            else:
                if comma_counter == 0:
                    interior += "%s=%s" % (field, value)
                else:
                    interior += ", %s=%s" % (field, value)
                comma_counter += 1

        # Rellenamos el interior del nodo y decrementamos la profundidad
        string = string % interior
        self.depth -= 1

        # Caso final: Todos los subárboles han devuelto su descripción
        if self.depth == 0:
            string = "digraph {\n" + string + "\n}"
            print(string)
        else:
            return node_id, string

    def dot_state(self, node: AST):
        """
        Método auxiliar para poner en formato .dot un nodo AST
        """
        x = str(type(node).__name__) + "(%s)"
        node_id = "s%d" % (self.state_count)
        string = 's%d[label="%s", shape=box]' % (self.state_count, x)
        self.state_count += 1
        return string, node_id


class ASTReplaceVar(NodeTransformer):
    def __init__(self, name_var: str, replacement: AST) -> None:
        super().__init__()
        self.name_var = name_var
        self.replacement = replacement

    def visit_Name(self, node: Name) -> Any:
        # Sustituimos si tiene el nombre y es en contexto de carga
        if self.name_var == node.id and isinstance(node.ctx, ast.Load):
            return self.replacement
        return node


class ASTUnroll(NodeTransformer):

    def visit_For(self, node: For) -> Any:
        if isinstance(node.target, ast.Name) and isinstance(node.iter, ast.List):
            new_body = list()

            # Elts contiene los elementos de la lista del for
            for elem in node.iter.elts:
                # Copiamos profundamente el sub-árbol AST
                ncopy = copy.deepcopy(node)

                # Target es la variable del for
                repl = ASTReplaceVar(node.target.id, elem)
                repl.visit(ncopy)

                # Cogemos solo el cuerpo, no nos interesa el for
                new_body.extend(ncopy.body)

            # Iteramos de nuevo para los posibles bucles anidados
            extended_body = list()
            for elem in new_body:
                extended_body.append(self.visit(elem))

            # Devolvemos el cuerpo extendido -> AST reconfigura el árbol
            return extended_body

        # Caso por defecto, devolvemos el nodo sin más
        return node
