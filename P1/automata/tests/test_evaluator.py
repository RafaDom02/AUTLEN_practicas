"""Test evaluation of automatas."""
import unittest
from abc import ABC, abstractmethod
from typing import Optional, Type

from automata.automaton import FiniteAutomaton
from automata.automaton_evaluator import FiniteAutomatonEvaluator
from automata.utils import AutomataFormat


class TestEvaluatorBase(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    automaton: FiniteAutomaton
    evaluator: FiniteAutomatonEvaluator

    @abstractmethod
    def _create_automata(self) -> FiniteAutomaton:
        pass

    def setUp(self) -> None:
        """Set up the tests."""
        self.automaton = self._create_automata()
        self.evaluator = FiniteAutomatonEvaluator(self.automaton)

    def _check_accept_body(
        self,
        string: str,
        should_accept: bool = True,
    ) -> None:
        accepted = self.evaluator.accepts(string)
        self.assertEqual(accepted, should_accept)

    def _check_accept(
        self,
        string: str,
        should_accept: bool = True,
        exception: Optional[Type[Exception]] = None,
    ) -> None:

        with self.subTest(string=string):
            if exception is None:
                self._check_accept_body(string, should_accept)
            else:
                with self.assertRaises(exception):
                    self._check_accept_body(string, should_accept)


class TestEvaluatorFixed(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:

            Empty
            H
            He
            Hel
            Hell
            Hello final

            Empty -H-> H
            H -e-> He
            He -l-> Hel
            Hel -l-> Hell
            Hell -o-> Hello
        """

        return AutomataFormat.read(description)

    def test_fixed(self) -> None:
        """Test for a fixed string."""
        self._check_accept("Hello", should_accept=True)
        self._check_accept("Helloo", should_accept=False)
        self._check_accept("Hell", should_accept=False)
        self._check_accept("llH", should_accept=False)
        self._check_accept("", should_accept=False)
        self._check_accept("Hella", should_accept=False)
        self._check_accept("aHello", should_accept=False)
        self._check_accept("Helloa", should_accept=False)


class TestEvaluatorLambdas(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:

            1
            2
            3
            4 final

            1 --> 2
            2 --> 3
            3 --> 4
        """

        return AutomataFormat.read(description)

    def test_lambda(self) -> None:
        """Test for a fixed string."""
        self._check_accept("", should_accept=True)
        self._check_accept("a", should_accept=False)


class TestEvaluatorNumber(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:

            initial
            sign
            int final
            dot
            decimal final

            initial ---> sign
            initial --> sign
            sign -0-> int
            sign -1-> int
            int -0-> int
            int -1-> int
            int -.-> dot
            dot -0-> decimal
            dot -1-> decimal
            decimal -0-> decimal
            decimal -1-> decimal
        """

        return AutomataFormat.read(description)

    def test_number(self) -> None:
        """ Test for a fixed string. """
        self._check_accept("0", should_accept=True)
        self._check_accept("0.0", should_accept=True)
        self._check_accept("0.1", should_accept=True)
        self._check_accept("1.0", should_accept=True)
        self._check_accept("-0", should_accept=True)
        self._check_accept("-0.0", should_accept=True)
        self._check_accept("-0.1", should_accept=True)
        self._check_accept("-1.0", should_accept=True)
        self._check_accept("-101.010", should_accept=True)
        self._check_accept("0.", should_accept=False)
        self._check_accept(".0", should_accept=False)
        self._check_accept("0.0.0", should_accept=False)
        self._check_accept("0-0.0", should_accept=False)

class TestEvaluatorCicle(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:

            s1
            s2
            s3
            s4 final
            s5 final

            s1 --> s2
            s2 --> s3
            s2 -b-> s5
            s3 --> s1
            s3 -a-> s4
            s3 -b-> s3
            s5 -b-> s5
        """

        return AutomataFormat.read(description)

    def test_cicle(self) -> None:
        """ Test for a fixed string. """
        self._check_accept("b", should_accept=True)
        self._check_accept("bb", should_accept=True)
        self._check_accept("bbbbbbbbb", should_accept=True)
        self._check_accept("a", should_accept=True)
        self._check_accept("b", should_accept=True)
        self._check_accept("aa", should_accept=False)
        self._check_accept("bbbbba", should_accept=True)
        self._check_accept("bbbbbaa", should_accept=False)
        self._check_accept("", should_accept=False)


if __name__ == '__main__':
    unittest.main()
