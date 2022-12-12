import unittest
from typing import AbstractSet

from grammar.grammar import Grammar
from grammar.utils import GrammarFormat


class TestFollow(unittest.TestCase):
    def _check_follow(
        self,
        grammar: Grammar,
        symbol: str,
        follow_set: AbstractSet[str],
    ) -> None:
        with self.subTest(string=f"Follow({symbol}), expected {follow_set}"):
            computed_follow = grammar.compute_follow(symbol)
            self.assertEqual(computed_follow, follow_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        E -> X+
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "E", {'$', ')', '+'})
        self._check_follow(grammar, "T", {'$', ')', '+'})
        self._check_follow(grammar, "X", {'$', ')', '+'})
        self._check_follow(grammar, "Y", {'$', ')', '+'})

    def test_case2(self) -> None:
        ''' Test case 2.'''
        grammar_str = """
        E -> TTX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "E", {'$', ')'})
        self._check_follow(grammar, "T", {'$', ')', '+', '(', 'i'})
        self._check_follow(grammar, "X", {'$', ')'})
        self._check_follow(grammar, "Y", {'$', ')', '+', '(', 'i'})

    def test_case3(self) -> None:
        ''' Test case 3.'''
        grammar_str = """
        A -> BCD
        B -> <
        B ->
        C -> 0C;
        C -> 1C;
        D -> 0>
        D -> 1>
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "A", {'$'})
        self._check_follow(grammar, "B", {'1', '0'})
        self._check_follow(grammar, "C", {'1', '0', ';'})
        self._check_follow(grammar, "D", {'$'})
    
    def test_case4(self) -> None:
        ''' Test case 4.'''
        grammar_str = """
        P -> bZe
        Z -> S;Z
        Z ->
        S -> DV
        D -> i
        D -> f
        V -> iU
        U ->,V
        U ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "D", {'i'})
        self._check_follow(grammar, "P", {'$'})
        self._check_follow(grammar, "S", {';'})
        self._check_follow(grammar, "U", {';'})
        self._check_follow(grammar, "V", {';'})
        self._check_follow(grammar, "Z", {'e'})

    def test_case5(self) -> None:
        ''' Test case 5.'''
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
        self._check_follow(grammar, "A", {'$', '*'})
        self._check_follow(grammar, "D", {'$'})
        self._check_follow(grammar, "I", {'*'})
        self._check_follow(grammar, "X", {'$'})

    def test_case6(self) -> None:
        ''' Test case 6.'''
        grammar_str = """
        T -> FGH
        F -> 
        F -> Gb
        G -> Nd
        G ->  
        H -> aA
        H -> 
        N -> 0N
        N -> 1N
        N -> 
        A -> a
        A ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "A", {'$'})
        self._check_follow(grammar, "F", {'0', '1', 'a', '$', 'd'})
        self._check_follow(grammar, "G", {'a', 'b', '$'})
        self._check_follow(grammar, "H", {'$'})
        self._check_follow(grammar, "N", {'d'})
        self._check_follow(grammar, "T", {'$'})

    def test_case7(self) -> None:
        ''' Test case 7.'''
        grammar_str = """
        N -> F
        N -> n
        F -> TR
        T -> t
        T -> 
        R -> nA
        R -> A
        A -> aS
        S -> a
        S -> 
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "A", {'$'})
        self._check_follow(grammar, "F", {'$'})
        self._check_follow(grammar, "N", {'$'})
        self._check_follow(grammar, "R", {'$'})
        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "T", {'a','n'})
    
    def test_case8(self) -> None:
        ''' Test case 8.'''
        grammar_str = """
        A -> I=E 
        I -> iX
        X -> 
        X -> [E]
        E -> k
        E -> i
        E -> f(L)
        L -> ER
        R -> 
        R -> ;L
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "A", {'$'})
        self._check_follow(grammar, "E", {'$', ')', ';', ']'})
        self._check_follow(grammar, "I", {'='})
        self._check_follow(grammar, "L", {')'})
        self._check_follow(grammar, "R", {')'})
        self._check_follow(grammar, "X", {'='})
    
    def test_case9(self) -> None:
        ''' Test case 9.'''
        grammar_str = """
        A -> I=E 
        I -> iX
        X -> 
        X -> [E]
        E -> CE
        E -> i
        E -> k
        C -> i+E
        C -> k+E
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "A", {'$'})
        self._check_follow(grammar, "C", {'i','k'})
        self._check_follow(grammar, "E", {'$', 'i', 'k', ']'})
        self._check_follow(grammar, "I", {'='})
        self._check_follow(grammar, "X", {'='})
    
    def test_case10(self) -> None:
        ''' Test case 10.'''
        grammar_str = """
        E -> (FE)
        F -> s
        F -> c
        F -> l
        F -> e
        E -> *EE
        E -> +EE
        E -> -EE
        E -> _EE
        E -> v
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "E", {'$', 'v', '(', ')', '*', '+', '-', '_'})
        self._check_follow(grammar, "F", {'v', '(', '*', '+', '-', '_'})

    def test_case11(self) -> None:
        ''' Test case 11.'''
        grammar_str = """
        X -> ST
        S -> a
        S ->
        T -> SX
        T ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "S", {'a', '$'})
        self._check_follow(grammar, "X", {'$'})
        self._check_follow(grammar, "T", {'$'})

if __name__ == '__main__':
    unittest.main()