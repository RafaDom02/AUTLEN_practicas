"""Automaton implementation."""
from tokenize import String
from typing import (
    Optional,
    Set,
    List,
    Dict,
    Tuple,
)


class State():
    """
    Definition of an automaton state. 

    Args:
        name: Name of the state.
        is_final: Whether the state is a final state or not.
        transitions: The list of transitions starting at this state.

    """

    name: str
    is_final: bool
    transitions: List['Transition']

    def __init__(self, name: str, is_final: bool = False) -> None:
        self.name = name
        self.is_final = is_final
        self.transitions = []

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return (
            self.name == other.name
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.name!r}, is_final={self.is_final!r}, transitions={self.transitions!r})"
        )

    def __hash__(self) -> int:
        return hash(self.name)

    def add_transitions(self, transitions: List['Transition']) -> None:
        """
        Convert to set and back to list to avoid repeated transitions.
        """
        self.transitions.extend(transitions)
        self.transitions = list(set(self.transitions))


class Transition():
    """
    Definition of an automaton transition. Since all transitions 
    'belong' to a given state, the initial state is not specified. 

    Args:
        symbol: Symbol consumed in the transition.
            ``None`` for a lambda transition.
        state: Name of the final state of the transition.

    """

    symbol: Optional[str]
    state: str

    def __init__(
        self,
        symbol: Optional[str],
        state: str,
    ) -> None:
        self.symbol = symbol
        self.state = state

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return (
            self.symbol == other.symbol
            and self.state == other.state
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"{self.symbol!r}, {self.state!r})"
        )

    def __hash__(self) -> int:
        return hash((self.symbol, self.state))


class FiniteAutomaton():
    """
    Definition of an automaton.

    Args:
        states: List of states of the automaton. The first state in the 
                list is the initial state.

    """

    states: List[State]
    name2state: Dict[str, State]
    _deterministic_count: int

    def __init__(
        self,
        states: List[State],
    ) -> None:
        """
        Check that there are no states with the same name.
        """
        if len(set(states)) != len(states):
            raise ValueError(
                "There are states with the same name",
            )
        """
        Check that the states in all transitions exist.
        """
        if not {t.state for s in states for t in s.transitions}.issubset({s.name for s in states}):
            raise ValueError(
                "There are transitions to an undefined state",
            )

        self.states = states
        self.name2state = {s.name: s for s in self.states}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"states={self.states!r}, "
        )

    def _get_deterministic_state(self, det_states: List[Tuple], evaluator) -> String:
        # Buscamos si ya existe primero el estado
        found = False
        i = 0
        
        while i < len(det_states) and found == False:
            if det_states[i][0] == evaluator.current_states:
                found = True
            else:
                i += 1

        if found == False:

            if len(evaluator.current_states) == 0:
                state = State("empty", False)
                det_states.append((set(), state))
                return "empty"

            # En este caso nos toca crear al nuevo estado
            self._deterministic_count += 1
            state = State("q" + str(self._deterministic_count),
                          evaluator.is_accepting())

            # Añade el conjunto y al estado correspondiente al conjunto
            det_states.append((evaluator.current_states.copy(),state ))

            # Devolvemos el nombre para las transiciones
            return state.name

        # Devolvemos el nombre para las transiciones
        return det_states[i][1].name

    def _get_dictionary(self) -> 'set[str]':
        dict = set()

        for state in self.states:
            for t in state.transitions:
                if t.symbol != None:
                    dict.add(t.symbol)

        return dict

    def to_deterministic(self) -> 'FiniteAutomaton':
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        """
        Return a equivalent deterministic automaton.

        Returns:
            Equivalent deterministic automaton.

        """
        # ---------------------------------------------------------------------
        """
        El evaluador nos ayudará a ver las transiciones que se generan.
        Además en el constructor constuye al conjunto inicial de estados
        """

        self._deterministic_count = 0
        evaluator = FiniteAutomatonEvaluator(self)
        det_states: List[Tuple] = list()

        self._get_deterministic_state(det_states, evaluator)
        dictionary = self._get_dictionary()

        # Ahora debemos ver a donde vamos con cada conjunto y símbolo posible

        i = 0
        while i < len(det_states):

            for symbol in dictionary:
                current_set = det_states[i][0].copy()

                evaluator.current_states = current_set
                evaluator.process_symbol(symbol)

                # Añadimos la transición al estado en cuestión
                det_states[i][1].add_transitions(
                    [Transition(symbol, self._get_deterministic_state(det_states, evaluator))])
            i=i+1

        final_states = []

        for d in det_states:
            final_states.append(d[1])

        return FiniteAutomaton(final_states)
        # ---------------------------------------------------------------------

    def to_minimized(self) -> 'FiniteAutomaton':
        """
        Return a equivalent minimal automaton.

        Returns:
            Equivalent minimal automaton.

        """
        # ---------------------------------------------------------------------
        # TO DO: Implement this method...

        raise NotImplementedError("This method must be implemented.")
        # ---------------------------------------------------------------------
