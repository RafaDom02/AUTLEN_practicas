"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton: FiniteAutomaton,
        expected: FiniteAutomaton,
    ) -> None:
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_deterministic()
        equiv_map = deterministic_automata_isomorphism(
            expected,
            transformed,
        )

        self.assertTrue(equiv_map is not None)


    def test_case1(self) -> None:
        """Test Case 1. Test basico de comprobacion. Solo dos estado y cada uno solo utiliza 1 de los dos simbolos existentes"""
        automaton_str = """
        Automaton:
        
        q0
        qf final
        
        q0 -0-> qf
        qf -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        q0
        qf final
        empty
        
        q0 -0-> qf
        q0 -1-> empty
        qf -0-> empty
        qf -1-> qf
        empty -0-> empty
        empty -1-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    
    def test_case2(self) -> None:
        """Test Case 2. Test parecido al 1 pero un poco más complejo para comprobar su buen funcionamiento"""
        automaton_str = """
        Automaton:
        
        q0
        q1
        qf final
        
        q0 -0-> q1
        q1 -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        q0
        q1
        qf final
        empty
        
        q0 -0-> q1
        q0 -1-> empty
        q1 -0-> empty
        q1 -1-> qf
        qf -0-> empty
        qf -1-> empty
        empty -0-> empty
        empty -1-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    
    def test_case3(self) -> None:
        """Test Case 3. Test complejo, aseguramos deshacernos del q0 (ya que todos sus simbolos son lambda) y de estados ineficientes (q7)"""
        automaton_str = """
        Automaton:
        
        q0
        q1
        q2
        q3
        q4
        q5
        q6 final
        q7
        
        q0 --> q1
        q0 --> q2
        q1 -1-> q5
        q1 -1-> q3
        q2 -0-> q4
        q4 -1-> q6
        q5 --> q7
        q5 -0-> q3
        q5 -0-> q4
        q7 --> q6
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        q0q1q2
        q3q5q6q7 final
        q4
        q3q4
        q6 final
        empty

        q0q1q2 -1-> q3q5q6q7
        q0q1q2 -0-> q4
        q4 -1-> q6
        q4 -0-> empty
        q3q5q6q7 -1-> empty
        q3q5q6q7 -0-> q3q4
        q3q4 -1-> q6
        q3q4 -0-> empty
        q6 -1-> empty
        q6 -0-> empty
        empty -1-> empty
        empty -0-> empty
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    
    def test_case4(self) -> None:
        """Test Case 4. Buscamos deshacernos del bucle q0-q4 y minimizarlo visualmente para que sea q5-q6"""
        automaton_str = """
        Automaton:
        
        q0
        q1
        q2
        q3
        q4 final

        q0 -a-> q0
        q0 -b-> q0
        q0 -b-> q1
        q1 -a-> q1
        q1 -b-> q2
        q2 -a-> q3
        q2 -b-> q2
        q3 -a-> q3
        q3 -a-> q4
        q3 -b-> q3
        q4 -a-> q0
        q4 -b-> q0
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        q0
        q0q1
        q0q1q2
        q0q1q3
        q0q1q2q3
        q0q1q3q4 final

        q0 -a-> q0
        q0 -b-> q0q1
        q0q1 -a-> q0q1
        q0q1 -b-> q0q1q2
        q0q1q2 -a-> q0q1q3
        q0q1q2 -b-> q0q1q2
        q0q1q3 -a-> q0q1q3q4
        q0q1q3 -b-> q0q1q2q3
        q0q1q2q3 -a-> q0q1q3q4
        q0q1q2q3 -b-> q0q1q2q3
        q0q1q3q4 -a-> q0q1q3q4
        q0q1q3q4 -b-> q0q1q2q3

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case5(self) -> None:
        """Test Case 5. Caso parecido a test2 pero con q0 teniendo transiciones con simbolos repetidos"""
        automaton_str = """
        Automaton:
        
        q0
        q1
        qf final
        
        q0 -0-> q0
        q0 -1-> q0
        q0 -1-> q1
        q1 -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        
        q0
        q0q1
        q0q1qf final
        
        q0 -0-> q0
        q0 -1-> q0q1
        q0q1 -0-> q0
        q0q1 -1-> q0q1qf
        q0q1qf -1-> q0q1qf
        q0q1qf -0-> q0
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case6(self) -> None:
        """Test Case 6. Ejemplo complejo para visualizar/comprobar la correcta creacion de un estado sumidero"""
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
        
        q0q1
        q1
        q2
        q1q4
        q2q3q5 final
        q3q5 final
        empty
        
        q0q1 -d-> q1q4
        q0q1 ---> q1
        q0q1 -+-> q1
        q0q1 -.-> q2
        q1 -d-> q1q4
        q1 ---> empty
        q1 -+-> empty
        q1 -.-> q2
        q2 -d-> q3q5
        q2 ---> empty
        q2 -+-> empty
        q2 -.-> empty
        q1q4 -d-> q1q4
        q1q4 ---> empty
        q1q4 -+-> empty
        q1q4 -.-> q2q3q5
        q2q3q5 -d-> q3q5
        q2q3q5 ---> empty
        q2q3q5 -+-> empty
        q2q3q5 -.-> empty
        q3q5 -d-> q3q5
        q3q5 ---> empty
        q3q5 -+-> empty
        q3q5 -.-> empty
        empty -d-> empty
        empty ---> empty
        empty -+-> empty
        empty -.-> empty
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)



if __name__ == '__main__':
    unittest.main()