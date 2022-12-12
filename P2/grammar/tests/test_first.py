import unittest
from typing import AbstractSet

from grammar.grammar import Grammar
from grammar.utils import GrammarFormat
class TestFirst(unittest.TestCase):
    def _check_first(
        self,
        grammar: Grammar,
        input_string: str,
        first_set: AbstractSet[str],
    ) -> None:
        with self.subTest(
            string=f"First({input_string}), expected {first_set}",
        ):
            computed_first = grammar.compute_first(input_string)
            self.assertEqual(computed_first, first_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        X ->
        X -> +E
        T -> iY
        T -> (E)
        Y -> 
        Y -> *T
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "Y", {'', '*'})
        self._check_first(grammar, "", {''})
        self._check_first(grammar, "Y+i", {'+', '*'})
        self._check_first(grammar, "YX", {'+', '*', ''})
        self._check_first(grammar, "YXT", {'+', '*', 'i', '('})

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
        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "Y", {'', '*'})

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
        self._check_first(grammar, "A", {'0', '1', '<'})
        self._check_first(grammar, "B", {'', '<'})
        self._check_first(grammar, "C", {'0', '1'})
        self._check_first(grammar, "D", {'0', '1'})
    

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
        self._check_first(grammar, "D", {'f','i'})
        self._check_first(grammar, "P", {'b'})
        self._check_first(grammar, "S", {'f', 'i'})
        self._check_first(grammar, "U", {'', ','})
        self._check_first(grammar, "V", {'i'})
        self._check_first(grammar, "Z", {'', 'f', 'i'})

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
        self._check_first(grammar, "A", {'', 'a'})
        self._check_first(grammar, "D", {'', '*'})
        self._check_first(grammar, "I", {'', 'a', '*'})
        self._check_first(grammar, "X", {'a', '*'})

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
        self._check_first(grammar, "A", {'', 'a'})
        self._check_first(grammar, "F", {'0', '', '1', 'b', 'd'})
        self._check_first(grammar, "G", {'0', '', '1', 'd'})
        self._check_first(grammar, "H", {'', 'a'})
        self._check_first(grammar, "N", {'0', '', '1'})
        self._check_first(grammar, "T", {'', '0', 'a', '1', 'b', 'd'})

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
        self._check_first(grammar, "A", {'a'})
        self._check_first(grammar, "F", {'a', 't', 'n'})
        self._check_first(grammar, "N", {'a', 't', 'n'})
        self._check_first(grammar, "R", {'a', 'n'})
        self._check_first(grammar, "S", {'', 'a'})
        self._check_first(grammar, "T", {'','t'})
    
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
        self._check_first(grammar, "A", {'i'})
        self._check_first(grammar, "E", {'f', 'i', 'k'})
        self._check_first(grammar, "I", {'i'})
        self._check_first(grammar, "L", {'f', 'i', 'k'})
        self._check_first(grammar, "R", {'', ';'})
        self._check_first(grammar, "X", {'', '['})
    
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
        self._check_first(grammar, "A", {'i'})
        self._check_first(grammar, "C", {'i','k'})
        self._check_first(grammar, "E", {'i', 'k'})
        self._check_first(grammar, "I", {'i'})
        self._check_first(grammar, "X", {'', '['})
    
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
        self._check_first(grammar, "E", {'v', '(', '*', '+', '-', '_'})
        self._check_first(grammar, "F", {'s', 'c', 'l', 'e'})

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
        self._check_first(grammar, "S", {'', 'a'})
        self._check_first(grammar, "X", {'', 'a'})
        self._check_first(grammar, "T", {'', 'a'})

    def test_case12(self) -> None:
        ''' Test case 12.'''
        grammar_str = """
        E -> T
        E -> 
        E -> i
        T -> Ec
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {'', 'c', 'i'})
        self._check_first(grammar, "T", {'c', 'i'})

if __name__ == '__main__':
    unittest.main()