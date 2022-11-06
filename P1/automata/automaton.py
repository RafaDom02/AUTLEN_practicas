"""Automaton implementation."""
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

    def get_lambdas(self) -> List['Transition']:
        """
        Searches for all lambda transitions

        Returns:
            A list of Transitions (empty if there are none)
        """
        selected = list()

        for t in self.transitions:
            if t.symbol == None:
                selected.append(t)

        return selected

    def search_transitions(self, symbol) -> List['Transition']:
        """
        Searches if there's a transition with the specified symbol.

        Returns:
            A list of Transitions (empty if there are none)
        """
        selected = list()

        for t in self.transitions:
            if t.symbol == symbol:
                selected.append(t)

        return selected

    def _could_be_deterministic(self, dictionary: Set[str]) -> bool:
        """
        Determines if the current state is deterministic according to the following criteria

            1. There's no lambdas
            2. There are transitions for all symbols
            3. There is only one transition for each symbol.
        """
        symbol_subset: Set[str] = set()

        for t in self.transitions:
            if t.is_lambda():
                return False

            # Si hay otra transición que utiliza el mismo símbolo entonces ya estará en el subconjunto
            if t.symbol in symbol_subset:
                return False
            else:
                symbol_subset.add(t.symbol)

        """
        Si tienen la misma cantidad de elementos podemos decir que son iguales (bajo la condición que
        esta instancia del estado esté asocido al autómata que le proporciona el diccionario)
        """
        return len(symbol_subset) == len(dictionary)


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

    def is_lambda(self) -> bool:
        return self.symbol == None

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
    # New variable for storing the dictionary of the automaton
    _dictionary = Set[str]
    # New variable for keeping the count of generated deterministic states
    _deterministic_count: int
    # New variable for caching the result of index processed transitions
    _cached_class_indexes: Dict[str, int]
    # New variable for indicating if current automaton is deterministic
    _is_deterministic: bool

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
        self._get_dictionary()
        self._cached_class_indexes = dict()
        self.name2state = {s.name: s for s in self.states}

        # Por defecto
        self._is_deterministic = False

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"states={self.states!r}, "
        )

    def __set_deterministic(self, deterministic: bool):
        """
        This method should not be used outside this class
        or there could be undefined behaviour
        """
        self._is_deterministic = deterministic

    def _get_dictionary(self):
        """
        Generates the dictionary of the automaton
        """
        self._dictionary = set()

        for state in self.states:
            for t in state.transitions:
                if t.symbol != None:
                    self._dictionary.add(t.symbol)

    def _check_deterministic(self) -> bool:
        """
        Checks if the current automaton is deterministic
        """
        for state in self.states:
            if not state._could_be_deterministic(self._dictionary):
                return False

        # Caso en el que desde la creación del autómata era deteminista -> Lo indicamos para el futuro
        self.__set_deterministic(True)
        
        return True

    def _get_deterministic_state(self, det_states: List[Tuple], evaluator) -> str:
        """
        This method searches for deterministic state in the provided table
        that matches the current set of states in the evaluator (it's an instance of FiniteAutomatonEvaluator)

        Note: The evaluator isn't typed because of the circular import problem
        """
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
            det_states.append((evaluator.current_states.copy(), state))

            # Devolvemos el nombre para las transiciones
            return state.name

        # Devolvemos el nombre para las transiciones
        return det_states[i][1].name

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

        # Esta tabla contiene : [conjunto de estados, estado determinista correspondiente]
        det_states: List[Tuple] = list()

        # Lanzamos el procesado del conjunto inicial de estados
        self._get_deterministic_state(det_states, evaluator)

        # Ahora debemos ver a donde vamos con cada conjunto y símbolo posible
        i = 0
        while i < len(det_states):

            for symbol in self._dictionary:
                current_set = det_states[i][0].copy()

                evaluator.current_states = current_set
                evaluator.process_symbol(symbol)

                # Añadimos la transición al estado en cuestión
                det_states[i][1].add_transitions(
                    [Transition(symbol, self._get_deterministic_state(det_states, evaluator))])

            # Vamos a por el siguiente estado
            i = i+1

        final_states = []

        # Agrupamos el resultado del cálculo
        for d in det_states:
            final_states.append(d[1])

        # Creamos el estado y anotamos el hecho que ya es determinista
        result = FiniteAutomaton(final_states)
        result.__set_deterministic(True)

        return result
        # ---------------------------------------------------------------------

    def _eliminate_inaccesible_states(self) -> None:
        """
        Eliminates all the inaccesible states from the automaton
        via BFS with graph search (elimination of repeated states)
        """
        to_visit: List[State] = list()
        to_visit.append(self.states[0])
        visited: List[State] = list()

        while len(to_visit) != 0:
            state = to_visit.pop(0)

            if state not in visited:
                for t in state.transitions:
                    next_state = self.name2state[t.state]
                    to_visit.append(next_state)

                visited.append(state)

        self.states = visited

    def _get_index_of_det_transition(self, symbol: str, pos: int) -> int:
        # Comprobamos si el resultado lo tenemos ya en la caché
        destination = self._cached_class_indexes.get("%d%s" % (pos, symbol))

        if destination is None:
            state: State = self.states[pos]
            selected: Transition = None

            for t in state.transitions:
                if t.symbol == symbol:
                    selected = t

            # Obtenemos el índice
            destination = self.states.index(self.name2state[selected.state])

            # Lo metemos en la caché para futuras consultas
            self._cached_class_indexes["%d%s" % (pos, symbol)] = destination

        return destination

    def _equivalent_classes(self, new_classes: List[int], classes: List[int], pos1: int, pos2: int) -> bool:
        # Comprobamos que no tiene clase de equivalencia asignada
        if new_classes[pos1] != -1:
            return False

        # Comprobamos que tienen la misma clase de equivalencia anterior
        if classes[pos2] != classes[pos1]:
            return False

        for symbol in self._dictionary:
            final1 = classes[self._get_index_of_det_transition(symbol, pos1)]
            final2 = classes[self._get_index_of_det_transition(symbol, pos2)]

            # Si las clases no coinciden al transitar -> No son equivalentes
            if final1 != final2:
                return False

        return True

    def _get_transitions_from_index(self, class_list: List[int], pos: int) -> List[Transition]:
        transitions: List[Transition] = list()

        for symbol in self._dictionary:
            transitions.append(Transition(symbol, "q{}".format(
                class_list[self._get_index_of_det_transition(symbol, pos)])))

        return transitions

    def _get_deterministic_from_classes(self, class_list: List[int]) -> list[State]:

        new_states = list()
        classes = list(set(class_list))

        # A partir de la tabla de clases obtenemos los nuevos estados
        for c in classes:
            # Creamos el estado
            state = State("q{}".format(c),
                          self.states[class_list.index(c)].is_final)
            new_states.append(state)

            # Buscamos las transiciones a las otras clases a partir de una base
            base_state = class_list.index(c)
            state.add_transitions(
                self._get_transitions_from_index(class_list, base_state))

        return new_states

    """
    Detalles de implementación importantes

    Para facilitar el acceso y ahorrar búsquedas están alineados
    por índice los estados con sus clases de equivalencia antiguas y nuevas.

    Ejemplo:

    self.states ->  q1  q2  q3  qf 
    classes     ->  0   0   0   1
    new_classes ->  0   -1  -1  -1

    Por tanto solemos manipular los índices en vez de los estados puesto que estos
    conllevan el triple de información.
    """

    def to_minimized(self) -> 'FiniteAutomaton':
        """
        Return a equivalent minimal automaton.

        Returns:
            Equivalent minimal automaton.

        """
        # Antes de empezar comprobamos si el autómata es determinista
        if not self._is_deterministic:

            # Debemos comprobar el hecho puesto que asumimos por defecto que no lo es
            if not self._check_deterministic():
                self.to_deterministic()

        classes: List[int] = list()
        # Eliminamos los estados inaccesibles
        self._eliminate_inaccesible_states()

        # Primera iteración: Finales = 1 y No Finales = 0
        for state in self.states:
            classes.append(1 if state.is_final else 0)

        # N-ésimas iteraciones: Solo paramos si las clases no han cambiado
        changed = True
        while changed:
            new_classes: List[int] = [-1 for state in self.states]
            class_id = 0
            try:
                while True:
                    # Buscamos al siguiente estado que no tiene una clase asignada
                    j = new_classes.index(-1)
                    new_classes[j] = class_id

                    for i in range(j+1, len(classes)):
                        if self._equivalent_classes(new_classes, classes, i, j):
                            new_classes[i] = new_classes[j]

                    # Creamos la siguiente clase
                    class_id += 1

            except ValueError:
                # En este caso hemos agotado la lista de new_classes
                pass

            # Comprobamos si la lista de clases cambió respecto a la anterior
            changed = False
            i = 0
            while i < len(classes) and changed == False:
                if classes[i] != new_classes[i]:
                    changed = True
                i = i + 1

            # Actualizamos las clases de equivalencia
            classes = new_classes

        # Creamos el automata
        return FiniteAutomaton(self._get_deterministic_from_classes(classes))
        # ---------------------------------------------------------------------
