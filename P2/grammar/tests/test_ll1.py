import unittest
from typing import AbstractSet

from grammar.grammar import Grammar
from grammar.utils import GrammarFormat
from grammar.grammar import Grammar, LL1Table, ParseTree, SyntaxError


class TestLL1(unittest.TestCase):
    def _check_table(
        self,
        grammar: Grammar,
        t_table: LL1Table,
        exception: bool
    ) -> None:
        if exception:
            t_calc = grammar.get_ll1_table()
            self.assertEqual(t_calc, None)
        else:
            t_calc = grammar.get_ll1_table()
            self.assertEqual(t_calc, t_table)

    def test_case1(self) -> None:
        """Test for syntax analysis from table."""
        terminals = {"(", ")", "i", "+", "*", "$"}
        non_terminals = {"E", "T", "X", "Y"}
        cells = [('E', '(', 'TX'),
                 ('E', 'i', 'TX'),
                 ('T', '(', '(E)'),
                 ('T', 'i', 'iY'),
                 ('X', '+', '+E'),
                 ('X', ')', ''),
                 ('X', '$', ''),
                 ('Y', '*', '*T'),
                 ('Y', '+', ''),
                 ('Y', ')', ''),
                 ('Y', '$', '')]
        table = LL1Table(non_terminals, terminals)
        for (nt, t, body) in cells:
            table.add_cell(nt, t, body)
        
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_table(grammar,table,False)

    def test_case2(self) -> None:
        """Test for syntax analysis from table."""
        
        grammar_str = """
        X -> I*AD
        I -> A*I
        I -> a
        I -> 
        A -> aa*A
        A -> a
        A -> 
        D -> *
        D -> 
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_table(grammar,None,True)

    def test_case3(self) -> None:
        """Test for syntax analysis from table."""
        
        grammar_str = """
        A -> BCD
        B -> <
        B -> 
        C -> 0C;
        C -> 1C;
        C -> 
        D -> 0>
        D -> 1>
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_table(grammar,None,True)

    def test_case4(self) -> None:
        """Test for syntax analysis from table."""
        
        grammar_str = """
        A -> I=E
        I -> iX
        X -> l
        X -> [E]
        E -> CE
        E -> i
        E -> k
        C -> i+E
        C -> k+E
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_table(grammar,None,True)

    
    def test_case5(self) -> None:
        """Test for syntax analysis from table."""

        terminals = {"=", "(", ")", "i", "k", 
                     "f", "[", "]","$"}
        non_terminals = {"S", "V", "R", "E"}
        cells = [('S', 'i', 'V=E'),
                 ('E', 'f', 'f(k)'),
                 ('E', 'i', 'i'),
                 ('E', 'k', 'k'),
                 ('R', '=', ''),
                 ('R', '[', '[E]'),
                 ('V', 'i', 'iR'),
                 ]
        table = LL1Table(non_terminals, terminals)
        for (nt, t, body) in cells:
            table.add_cell(nt, t, body)
        
        grammar_str = """
        S -> V=E
        V -> iR
        R -> 
        R -> [E]
        E -> k
        E -> i
        E -> f(k)
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_table(grammar,table,False)

if __name__ == '__main__':
    unittest.main()