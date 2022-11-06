"""Conversion from regex to automata."""
from typing import List, Tuple

from automata.automaton import FiniteAutomaton, State, Transition


def _re_to_rpn(re_string: str) -> str:
    """
    Convert re to reverse polish notation (RPN).

    Does not check that the input re is syntactically correct.

    Args:
        re_string: Regular expression in infix notation.

    Returns:
        Regular expression in reverse polish notation.

    """
    stack: List[str] = []
    rpn_string = ""
    for x in re_string:
        if x == "+":
            while len(stack) > 0 and stack[-1] != "(":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == ".":
            while len(stack) > 0 and stack[-1] == ".":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == "(":
            stack.append(x)
        elif x == ")":
            while stack[-1] != "(":
                rpn_string += stack.pop()
            stack.pop()
        else:
            rpn_string += x

    while len(stack) > 0:
        rpn_string += stack.pop()

    return rpn_string


class REParser():
    """Class for processing regular expressions in Kleene's syntax."""

    state_counter: int

    def __init__(self) -> None:
        self.state_counter = 0

    def _create_terminal_states(self) -> Tuple[State, State]:
        """
        This is a new method for creating both beginning and ending
        states for the standard procedure of conversion of regular expressions
        (in Kleene's syntax) into an non deterministic automaton.

        Returns:
            Both initial and final states
        """

        state_ini = State('state' + str(self.state_counter), False)
        self.state_counter += 1
        
        state_final = State('state' + str(self.state_counter), True)
        self.state_counter += 1

        return state_ini, state_final

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the empty language.

        Returns:
            Automaton that accepts the empty language.

        """
        # ---------------------------------------------------------------------
        # TO DO: Implement this method...

        initial_state, final_state = self._create_terminal_states()

        return FiniteAutomaton([initial_state, final_state])
        # ---------------------------------------------------------------------

    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the empty string.

        Returns:
            Automaton that accepts the empty string.

        """
        # ---------------------------------------------------------------------
        # TO DO: Implement this method...
        initial_state, final_state = self._create_terminal_states()

        transition_ini_fin = Transition(None, final_state.name)
        initial_state.add_transitions([transition_ini_fin])

        return FiniteAutomaton([initial_state, final_state])
        # ---------------------------------------------------------------------

    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts one symbol.

        Args:
            symbol: Symbol that the automaton should accept.

        Returns:
            Automaton that accepts a symbol.

        """
        # ---------------------------------------------------------------------
        # TO DO: Implement this method...
        initial_state, final_state = self._create_terminal_states()

        transition_ini_fin = Transition(symbol, final_state.name)
        initial_state.add_transitions([transition_ini_fin])

        return FiniteAutomaton([initial_state, final_state])
        # ---------------------------------------------------------------------

    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the Kleene star of another.

        Args:
            automaton: Automaton whose Kleene star must be computed.

        Returns:
            Automaton that accepts the Kleene star.

        """
        # ---------------------------------------------------------------------
        # TO DO: Implement this method...
        initial_state, final_state = self._create_terminal_states()
        states = [initial_state, final_state]

        #--------- INIT - FINAL | INIT - AUTOMATON ---------#
        t1 = Transition(None, final_state.name)
        t2 = Transition(None, automaton.states[0].name)

        initial_state.add_transitions([t1, t2])

        #--------- FINAL - INIT | AUTOMATON - FINAL ---------#
        old_final = automaton.states[1]
        old_final.is_final = False

        t1 = Transition(None, initial_state.name)
        t2 = Transition(None, final_state.name)

        final_state.add_transitions([t1])
        old_final.add_transitions([t2])

        states.extend(automaton.states)

        return FiniteAutomaton(states)
        # ---------------------------------------------------------------------

    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the union of two automata.

        Args:
            automaton1: First automaton of the union.
            automaton2: Second automaton of the union.

        Returns:
            Automaton that accepts the union.

        """
        # ---------------------------------------------------------------------
        # TO DO: Implement this method...
        initial_state, final_state = self._create_terminal_states()
        states = [initial_state, final_state]

        #--------- INIT - AUTO1 | INIT - AUTO2 ---------#
        t1 = Transition(None, automaton1.states[0].name)
        t2 = Transition(None, automaton2.states[0].name)

        initial_state.add_transitions([t1, t2])

        #--------- AUTO1 - FINAL | AUTO2 - FINAL ---------#
        old_final1 = automaton1.states[1]
        old_final1.is_final = False
        old_final2 = automaton2.states[1]
        old_final2.is_final = False

        t1 = Transition(None, final_state.name)

        old_final1.add_transitions([t1])
        old_final2.add_transitions([t1])

        states.extend(automaton1.states)
        states.extend(automaton2.states)

        return FiniteAutomaton(states)
        # ---------------------------------------------------------------------

    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the concatenation of two automata.

        Args:
            automaton1: First automaton of the concatenation.
            automaton2: Second automaton of the concatenation.

        Returns:
            Automaton that accepts the concatenation.

        """
        # ---------------------------------------------------------------------
        # TO DO: Implement this method...
        initial_state, final_state = self._create_terminal_states()
        states = [initial_state, final_state]

        #--------- INIT - AUTO1 ---------#
        t1 = Transition(None, automaton1.states[0].name)

        initial_state.add_transitions([t1])

        #--------- AUTO1 - AUTO2 ---------#
        old_final1 = automaton1.states[1]
        old_final1.is_final = False
        old_init2 = automaton2.states[0]

        t1 = Transition(None, old_init2.name)
        old_final1.add_transitions([t1])

        #--------- AUTO2 - FINAL ---------#
        old_final2 = automaton2.states[1]
        old_final2.is_final = False

        t1 = Transition(None, final_state.name)
        old_final2.add_transitions([t1])

        states.extend(automaton1.states)
        states.extend(automaton2.states)
        
        return FiniteAutomaton(states)
        # ---------------------------------------------------------------------

    def create_automaton(
        self,
        re_string: str,
    ) -> FiniteAutomaton:
        """
        Create an automaton from a regex.

        Args:
            re_string: String with the regular expression in Kleene notation.

        Returns:
            Automaton equivalent to the regex.

        """
        if not re_string:
            return self._create_automaton_empty()

        rpn_string = _re_to_rpn(re_string)

        stack: List[FiniteAutomaton] = []
        self.state_counter = 0
        for x in rpn_string:
            if x == "*":
                aut = stack.pop()
                stack.append(self._create_automaton_star(aut))
            elif x == "+":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_union(aut1, aut2))
            elif x == ".":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_concat(aut1, aut2))
            elif x == "λ":
                stack.append(self._create_automaton_lambda())
            else:
                stack.append(self._create_automaton_symbol(x))
        
        return stack.pop()
