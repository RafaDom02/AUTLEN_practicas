from __future__ import annotations

import copy
from typing import AbstractSet, Collection, Optional, Dict, List, Optional

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

def find_all_strings(substring, string):
    """ 
    Está pensado para iterar en un bucle 
    mediante yield en vez de return
    """

    i = string.find(substring)
    while i != -1:
        yield i
        i = string.find(substring, i+1)

class Grammar:
    """
    Class that represents a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Dictionary with the production rules for each non terminal
          symbol of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Dict[str, List[str]],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        if non_terminals != set(productions.keys()):
            raise ValueError(
                f"Set of non-terminals and productions keys should be equal."
            )
        
        for nt, rhs in productions.items():
            if not rhs:
                raise ValueError(
                    f"No production rules for non terminal symbol {nt} "
                )
            for r in rhs:
                for s in r:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom
        self.nt_firsts = self._compute_firsts()
        self.nt_follow = self._compute_follows()

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )
    
    def _compute_firsts(self) -> Dict[str, set[str]]:
        old_table: Dict[str,set[str]]= dict()
        equals = False
        # Creamos las entradas de la tabla
        for nt in self.non_terminals:
            old_table[nt] = set()
        
        # Iteramos sobre la tabla
        while not equals:
            new_table = copy.deepcopy(old_table)
            for nt in old_table.keys():
                for p in self.productions[nt]:
                    stop = False
                    i = 0

                    if p == '':
                        new_table[nt].add('')
                    
                    while i < len(p) and not stop:
                        if p[i] in self.terminals:
                            stop = True
                            new_table[nt].add(p[i])
                        elif p[i] in self.non_terminals:
                            next_first = copy.deepcopy(old_table[p[i]])
                            
                            if "" not in next_first or i+1 == len(p):
                                stop = True
                            else:
                                next_first -= {''}
                            
                            new_table[nt].update(next_first)

                        i += 1
            
            # Vemos si son iguales las tablas
            equals = True
            #print(new_table)
            #print(old_table)
            
            for nt in old_table.keys():
                if old_table[nt] != new_table[nt]:
                    equals = False
                    break
            
            old_table = new_table

        return new_table            


    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """
        
        if sentence == "":
            return {''}

        # "Y+i"
        symbols = list(sentence)
        # ['Y','+','i']
                
        i = 0
        stop = False
        firsts = set()

        while i < len(symbols) and not stop:
            sym = symbols[i]
            if sym in self.terminals:
                stop = True
                firsts.add(sym)
            elif sym in self.non_terminals:
                next_first = copy.deepcopy(self.nt_firsts[sym])

                if '' not in next_first or i+1 == len(symbols):
                    stop = True
                else:
                    next_first -= {''}
                
                
                firsts.update(next_first)
                #print(firsts, sym, next_first)
            else:
                raise ValueError("Symbol not in grammar")
            
            i += 1

        return firsts

        
    def _compute_follows(self):
        old_table: Dict[str,set[str]]= dict()
        equals = False

        # Creamos las entradas de la tabla
        for nt in self.non_terminals:
            if nt == self.axiom:
                old_table[nt] = {'$'}
            else:
                old_table[nt] = set()
        
        while not equals:
            new_table = copy.deepcopy(old_table)

            for nt in old_table.keys():
                for p in self.productions[nt]:
                    for cn in old_table.keys():
                        for i in find_all_strings(cn,p):
                            i += 1          # Para mirar al siguiente símbolo
                            stop = False

                            while i <= len(p) and not stop:
                                if i == len(p):
                                    stop = True
                                    new_table[cn].update(copy.deepcopy(old_table[nt]))
                                else:
                                    if p[i] in self.terminals:
                                        stop = True
                                        new_table[cn].add(p[i])
                                    else:
                                        n_firsts = copy.deepcopy(self.nt_firsts[p[i]])
                                        if "" not in n_firsts and cn != p[i]:
                                            stop = True
                                        else:
                                            n_firsts -= {''}
                                        
                                        new_table[cn].update(n_firsts)
                                i += 1
            # Vemos si son iguales las tablas
            equals = True
            
            for nt in old_table.keys():
                if old_table[nt] != new_table[nt]:
                    equals = False
                    break
            
            old_table = new_table


        return old_table

    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """
        """
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Dict[str, List[str]],
        axiom: str,
        """
	# TO-DO: Complete this method for exercise 4...
        if symbol in self.non_terminals:
            return self.nt_follow[symbol]
        else:
            raise ValueError("Symbol is not non-terminal in grammar")


    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """

	# TO-DO: Complete this method for exercise 5...
        ll1_table = LL1Table(self.non_terminals, set(self.terminals).union('$'))
        try:
            for nt in self.non_terminals:
                for p in self.productions[nt]:
                    first_p = self.compute_first(p)

                    for t in self.terminals:
                        if t in first_p:
                            ll1_table.add_cell(nt,t,p)

                    if "" in first_p:
                        for s in self.nt_follow[nt]:
                            ll1_table.add_cell(nt,s,p)
        except Exception as e:
            print(repr(e))
            return None

        return ll1_table


    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None


class LL1Table:
    """
    LL1 table. Initially all cells are set to None (empty). Table cells
    must be filled by calling the method add_cell.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        self.terminals: AbstractSet[str] = terminals
        self.non_terminals: AbstractSet[str] = non_terminals
        self.cells: Dict[str, Dict[str, Optional[str]]] = {nt: {t: None for t in terminals} for nt in non_terminals}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o,LL1Table):
            return False
        ll1_2: LL1Table = __o
        return (ll1_2.cells == self.cells)

    def add_cell(self, non_terminal: str, terminal: str, cell_body: str) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            non_terminal: Non termial symbol (row)
            terminal: Terminal symbol (column)
            cell_body: content of the cell 

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if non_terminal not in self.non_terminals:
            raise ValueError(
                "Trying to add cell for non terminal symbol not included "
                "in table.",
            )
        if terminal not in self.terminals:
            raise ValueError(
                "Trying to add cell for terminal symbol not included "
                "in table.",
            )
        if not all(x in self.terminals | self.non_terminals for x in cell_body):
            raise ValueError(
                "Trying to add cell whose body contains elements that are "
                "not either terminals nor non terminals.",
            )            
        if self.cells[non_terminal][terminal] is not None:
            raise RepeatedCellError(
                f"Repeated cell ({non_terminal}, {terminal}).")
        else:
            self.cells[non_terminal][terminal] = cell_body

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """

        # TO-DO: Complete this method for exercise 2...
        stack = list()
        root = ParseTree(start)
        node_stack:List[ParseTree] = list()
        stack.append("$")
        stack.append(start)
        node_stack.append(root)
        index = 0

        while len(stack) != 0:            
            if index == len(input_string):
                raise SyntaxError()
            
            #print(root, "--> root")
            elem = stack.pop()
            if elem != '$':
                node = node_stack.pop()
            
            if elem in self.non_terminals:
                row = self.cells[elem]
                n_sym = row.get(input_string[index])
                if n_sym != None:
                    # Si la regla es λ, no hay que añadir nada al stack
                    if n_sym != "":
                        texto = list(n_sym)

                        texto.reverse()
                        stack.extend(texto)

                        nodes = list(map(lambda n:ParseTree(n),texto))
                        node_stack.extend(nodes)
                        
                        nodes.reverse()
                        node.add_children(nodes)
                    else:
                        node.add_children([ParseTree("λ")])
                else:
                    raise SyntaxError()
                
            elif elem in self.terminals:
                if elem == input_string[index]:
                    index += 1
                else:
                    raise SyntaxError()
        
        if index == len(input_string):
            return root

        raise SyntaxError()
    
class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection[ParseTree] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection[ParseTree]) -> None:
        self.children = children

    def pretty_print(self,identation="  "):
        print(identation + self.root)

        for n in self.children:
            n.pretty_print(identation=identation + "  ")