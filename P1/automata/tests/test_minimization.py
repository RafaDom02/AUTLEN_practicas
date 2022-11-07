"""Test evaluation of minimized automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot


class TestMinimized(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton: FiniteAutomaton,
        expected: FiniteAutomaton,
    ) -> None:
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_minimized()

        equiv_map = deterministic_automata_isomorphism(
            expected,
            transformed,
        )

        self.assertTrue(equiv_map is not None)

    def test_case1(self) -> None:
        """Test Case 1. Reduce al maximo el automata para que se quede solamente en dos estado uno inicial y otro final"""
        automaton_str = """
        Automaton:
        
        q0 final
        q1
        q2 final
        q3
        q4 final
        q5

        q0 -0-> q1
        q0 -1-> q1
        q1 -0-> q2
        q1 -1-> q2
        q2 -0-> q3
        q2 -1-> q3
        q3 -0-> q4
        q3 -1-> q4
        q4 -0-> q5
        q4 -1-> q5
        q5 -0-> q0
        q5 -1-> q0
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        q0 final
        qf
        
        q0 -0-> qf
        q0 -1-> qf
        qf -0-> q0
        qf -1-> q0
        """

        expected = AutomataFormat.read(expected_str)
        
        self._check_transform(automaton, expected)

    def test_case2(self) -> None:
        """Test Case 2. Creamos dos caminos distintos pero con la misma cantidad de estados y transiciones para que se junten ambos caminos en uno"""
        automaton_str = """
        Automaton:
        
        q0
        q1 final
        q2
        q3 final
        q4

        q0 -a-> q1
        q0 -b-> q3
        q1 -a-> q2
        q1 -b-> q1
        q2 -a-> q1
        q2 -b-> q2
        q3 -a-> q4
        q3 -b-> q3
        q4 -a-> q3
        q4 -b-> q4
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        q0
        q1 final
        qf
        
        q0 -a-> q1
        q0 -b-> q1
        q1 -a-> qf
        q1 -b-> q1
        qf -a-> q1
        qf -b-> qf
        """

        expected = AutomataFormat.read(expected_str)
        
        self._check_transform(automaton, expected)

    def test_case3(self) -> None:
        """Test Case 3. Prueba la fusion de dos estados que estan unidos linealmente"""
        automaton_str = """
        Automaton:
        
        A final
        B final
        C final
        D final
        E
        
        A -a-> B
        A -b-> C
        A -c-> B
        B -a-> B
        B -b-> C
        B -c-> B
        C -a-> B
        C -b-> D
        C -c-> B
        D -a-> E
        D -b-> E
        D -c-> E
        E -a-> E
        E -b-> E
        E -c-> E
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        AB final
        C final
        D final
        E
        
        AB -a-> AB
        AB -b-> C
        AB -c-> AB
        C -a-> AB
        C -b-> D
        C -c-> AB
        D -a-> E
        D -b-> E
        D -c-> E
        E -a-> E
        E -b-> E
        E -c-> E
        """

        expected = AutomataFormat.read(expected_str)
        
        self._check_transform(automaton, expected)

    def test_case4(self) -> None:
        """Test Case 4. Test parecido al test3 pero que creando un bucle, uniendo el ultimo estado con el inicial"""
        automaton_str = """
        Automaton:
        
        q0
        q1 final
        q2
        q3 final
        q4
        q5 final

        q0 -a-> q1
        q0 -b-> q3
        q1 -a-> q2
        q1 -b-> q1
        q2 -a-> q1
        q2 -b-> q5
        q3 -a-> q4
        q3 -b-> q3
        q4 -a-> q3
        q4 -b-> q5
        q5 -a-> q0
        q5 -b-> q0
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        q0
        q1 final
        q2
        qf final
        
        q0 -a-> q1
        q0 -b-> q1
        q1 -a-> q2
        q1 -b-> q1
        q2 -a-> q1
        q2 -b-> qf
        qf -a-> q0
        qf -b-> q0
        """

        expected = AutomataFormat.read(expected_str)
        
        self._check_transform(automaton, expected)

    def test_case5(self) -> None:
        """Test Case 5. Creamos un automata no determinista, lo pasamos a determinista y a continuación le hacemos la minimizacion"""
        automaton_str = """
        Automaton:
        
        q0
        q1
        q2
        q3
        q4
        q5 final

        q0 ---> q1
        q0 -+-> q1
        q0 --> q1
        q1 -d-> q1
        q1 -d-> q4
        q1 -.-> q2
        q2 -d-> q3
        q3 -d-> q3
        q3 --> q5
        q4 -.-> q3  
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        q0
        q1
        q2
        q3
        q4 final
        empty
        
        q0 -.-> q3
        q0 ---> q2
        q0 -+-> q2
        q0 -d-> q1
        q1 -.-> q4
        q1 ---> empty
        q1 -+-> empty
        q1 -d-> q1
        q2 -.-> q3
        q2 ---> empty
        q2 -+-> empty
        q2 -d-> q1
        q3 -.-> empty
        q3 ---> empty
        q3 -+-> empty
        q3 -d-> q4
        q4 -.-> empty
        q4 ---> empty
        q4 -+-> empty
        q4 -d-> q4
        empty -.-> empty
        empty ---> empty
        empty -+-> empty
        empty -d-> empty
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()