"""Evaluation of automata."""
from collections import defaultdict, deque
from pstats import StatsProfile
from typing import Set

from automata.automaton import FiniteAutomaton, State

class FiniteAutomatonEvaluator():
    """
    Definition of an automaton evaluator.

    Args:
        automaton: Automaton to evaluate.

    Attributes:
        current_states: Set of current states of the automaton.

    """

    automaton: FiniteAutomaton
    current_states: Set[State]

    def __init__(self, automaton: FiniteAutomaton) -> None:
        self.automaton = automaton
        current_states: Set[State] = {
            self.automaton.states[0],  
        }
        self._complete_lambdas(current_states)
        self.current_states = current_states


    def process_symbol(self, symbol: str) -> None:
        """
        Process one symbol.

        Args:
            symbol: Symbol to consume.

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        expanded_states: Set[State] = set()

        for state in self.current_states:
            for transition in state.transitions:
                if transition.symbol == symbol:
                    expanded_states.add(self.automaton.name2state[transition.state])
        
        self.current_states = expanded_states
        self._complete_lambdas(self.current_states)
        #---------------------------------------------------------------------

        
    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        """
        Add states reachable with lambda transitions to the set.

        Args:
            set_to_complete: Current set of states to be completed.
        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        visited_states = list()
        to_visit_states = list(set_to_complete)
        
        while True:
            if(len(to_visit_states) == 0):
                return
            
            current_state = to_visit_states.pop()

            if (visited_states.count(current_state) == 0):
                for transition in current_state.transitions:
                    if transition.symbol == None:
                        state = self.automaton.name2state[transition.state]
                        to_visit_states.append(state)
                        set_to_complete.add(state)
            
                visited_states.append(current_state)        
        #---------------------------------------------------------------------

        
    def process_string(self, string: str) -> None:
        """
        Process a full string of symbols.

        Args:
            string: String to process.

        """
        for symbol in string:
            self.process_symbol(symbol)


    def is_accepting(self) -> bool:
        """Check if the current state is an accepting one."""
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        for state in self.current_states:
            if state.is_final == True:
                return True
        
        return False
        #---------------------------------------------------------------------
        

    def accepts(self, string: str) -> bool:
        """
        Return if a string is accepted without changing state.

        Note: This function is NOT thread-safe.

        """
        old_states = self.current_states
        try:
            self.process_string(string)
            accepted = self.is_accepting()
        finally:
            self.current_states = old_states

        return accepted

