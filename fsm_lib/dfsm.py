import collections
from itertools import count
from typing import Dict, Set, Union, Hashable

from .fsm import FSM
from .state import State
from .transition import Transition


class DeterministicFSM(FSM):
    __slots__ = ()  # declaration is required; no extra slots (only parent slots)

    def __init__(self, *,
                 fsm: Dict[State, Dict[Transition, Union[State, Set[State]]]] = None,
                 initial_states: Set[State] = None,
                 final_states: Set[State] = None):
        """
        :param fsm: deterministic FSM; for nondeterministic use cls.from_fsm(fsm: FSM = fsm)
        :param initial_states:
        :param final_states:
        """
        self._check_dfsm(fsm, allow_none=True)
        super().__init__(fsm=fsm, initial_states=initial_states, final_states=final_states)

    def add_transition(self, state_from: State, transition: Transition, state_to: State) -> bool:
        if transition.is_epsilon():
            raise ValueError('Epsilon transitions are forbidden in a DeterministicFSM')
        self._check_state(state_from, allow_none=False)
        self._check_transition(transition, allow_none=False)
        self._check_state(state_to, allow_none=False)
        self._fsm.setdefault(state_from, dict())
        self._fsm.setdefault(state_to, dict())
        transitions = self._fsm.get(state_from)
        state_or_set_of_states = transitions.get(transition)
        if state_or_set_of_states is not None and state_or_set_of_states != state_to:
            raise RuntimeError()
        transitions[transition] = state_to
        return True

    def add_transitions(self, state_from: State, transition: Transition,
                        states_to: Set[State]) -> NotImplementedError:
        raise NotImplementedError()

    def set_transitions(self, state_from: State, transition: Transition, states_to: Set[State],
                        replace=True) -> NotImplementedError:
        raise NotImplementedError()

    def remove_transitions(self, state_from: State, transition: Transition,
                           states_to: Set[State]) -> NotImplementedError:
        raise NotImplementedError()

    def minimize(self, name_of_state_generator=...):
        """
        Hopcroft's algorithm for minimizing a finite state machine.
        """

        if name_of_state_generator is ...:
            name_of_state_generator = map(str, count(1, 1))
        if name_of_state_generator is not None:
            if not hasattr(name_of_state_generator, '__iter__'):
                raise RuntimeError('Generator must have __iter__ method')
            name_of_state_generator = iter(name_of_state_generator)

        fsm = self.fsm_deepcopy()
        initial_states = self.initial_states_deepcopy()
        final_states = self.final_states_deepcopy()
        alphabet = self.alphabet()

        fictive_state = State('fictive_state')
        while fictive_state in self._fsm:
            fictive_state.uid += "'"
        fictive_alpha = Transition('fictive_alpha')
        while fictive_alpha in alphabet:
            fictive_alpha.label += "'"
        fsm[fictive_state] = {fictive_alpha: initial_states}
        initial_states = {fictive_state}
        alphabet.add(fictive_alpha)
        dfsm_obj = DeterministicFSM.from_original(fsm, initial_states, final_states, name_of_state_generator=None)
        fsm, initial_states, final_states = dfsm_obj._fsm, dfsm_obj._initial_states, dfsm_obj._final_states

        inversed_fsm = dict()
        for state, transitions in fsm.items():
            inversed_fsm.setdefault(state, dict())
            for transition, state_to in transitions.items():
                if isinstance(state_to, State):
                    state_to = {state_to}
                for alpha_state in state_to:
                    inversed_fsm.setdefault(alpha_state, dict()).setdefault(transition, set()).add(state)
        only_final_states = frozenset(final_states)
        without_final_states = frozenset(fsm).difference(final_states.union({fictive_state}))
        classes = {frozenset({fictive_state}), only_final_states, without_final_states}
        q = classes.copy()
        while q:
            some_class = q.pop()
            for alpha in alphabet:
                path_sources = set()
                for state in some_class:
                    if state in inversed_fsm and alpha in inversed_fsm[state]:
                        path_sources.update(inversed_fsm[state][alpha])
                for class_to_split in classes.copy():
                    p_with_class = class_to_split.intersection(path_sources)
                    if p_with_class:
                        p_without_class = class_to_split.difference(path_sources)
                        if p_without_class:
                            classes.remove(class_to_split)
                            classes.add(p_with_class)
                            classes.add(p_without_class)
                            if class_to_split in q:
                                q.remove(class_to_split)
                                q.add(p_with_class)
                                q.add(p_without_class)
                            else:
                                if len(p_with_class) <= len(p_without_class):
                                    q.add(p_with_class)
                                else:
                                    q.add(p_without_class)
        new_states = dict()
        new_initial_states = set()
        new_final_states = set()
        new_non_initial_classes = set()
        initial_states = fsm[fictive_state][fictive_alpha] if fictive_alpha in fsm[fictive_state] else set()
        initial_states = {initial_states} if isinstance(initial_states, State) else initial_states
        classes = {some_class for some_class in classes if bool(some_class) and fictive_state not in some_class}
        for some_class in classes:
            if not initial_states.isdisjoint(some_class):
                if name_of_state_generator is None:
                    n_class_str = some_class
                else:
                    n_class_str = next(name_of_state_generator)
                new_initial_states.add(State(n_class_str))
                for state in some_class:
                    new_states[state] = n_class_str
                if not final_states.isdisjoint(some_class):
                    new_final_states.add(State(n_class_str))
            else:
                new_non_initial_classes.add(some_class)
        new_final_classes = set()
        for some_class in new_non_initial_classes:
            if final_states.isdisjoint(some_class):
                if name_of_state_generator is None:
                    n_class_str = some_class
                else:
                    n_class_str = next(name_of_state_generator)
                for state in some_class:
                    new_states[state] = n_class_str
            else:
                new_final_classes.add(some_class)
        for some_class in new_final_classes:
            if name_of_state_generator is None:
                n_class_str = some_class
            else:
                n_class_str = next(name_of_state_generator)
            new_final_states.add(State(n_class_str))
            for state in some_class:
                new_states[state] = n_class_str
        new_fsm = dict()
        for some_class in classes:
            new_state = dict()
            for state in some_class:
                for alpha, alpha_state in fsm[state].items():
                    new_state[alpha] = State(new_states[alpha_state])
            any_state = next(iter(some_class))
            new_fsm[State(new_states[any_state])] = new_state
        return DeterministicFSM(fsm=new_fsm, initial_states=new_initial_states, final_states=new_final_states)

    def _brzozowski(self, name_of_state_generator=...):
        """
        Brzhozovsky's algorithm for minimizing a finite state machine.
        The disadvantage of the algorithm is that non-final states from which there are no transitions are discarded.
        Therefore, this algorithm in such cases has a different result compared to Hopcroft's algorithm.
        """

        dfsm_obj = DeterministicFSM(fsm=self._fsm, initial_states=self._initial_states, final_states=self._final_states)
        alphabet = dfsm_obj.alphabet()

        def add_initial_fictive_state(fsm_alphabet, fsm_obj):
            initial_fictive_state = State('initial_fictive_state')
            while fsm_obj.has_state(initial_fictive_state):
                initial_fictive_state.uid += "'"
            initial_fictive_alpha = Transition('initial_fictive_alpha')
            while initial_fictive_alpha in fsm_alphabet:
                initial_fictive_alpha.label += "'"
            fsm_alphabet.add(initial_fictive_alpha)
            fsm_obj.set_transitions(initial_fictive_state, initial_fictive_alpha, fsm_obj._initial_states)
            fsm_obj._initial_states = {initial_fictive_state}
            return initial_fictive_state, initial_fictive_alpha

        def remove_initial_fictive_state(fsm_alphabet, fsm_obj, initial_fictive_state, initial_fictive_alpha):
            if fsm_obj.has_state(initial_fictive_state):
                old_transitions = fsm_obj.remove_state(initial_fictive_state)
                if initial_fictive_alpha in old_transitions:
                    fsm_obj._initial_states = {old_transitions.pop(initial_fictive_alpha)}
            if initial_fictive_alpha in fsm_alphabet:
                fsm_alphabet.remove(initial_fictive_alpha)

        final_states_empty = not bool(dfsm_obj._final_states)

        # 1. r(A)
        inv_fsm_obj = dfsm_obj.reverse()
        if final_states_empty:
            inv_fsm_obj.set_initial_states(inv_fsm_obj.get_states())

        # add initial fictive state
        fictive_state, fictive_alpha = add_initial_fictive_state(alphabet, inv_fsm_obj)

        # 2. d(r(A))
        d_inv_fsm_obj = DeterministicFSM.from_fsm(inv_fsm_obj, None)

        # remove initial fictive state
        remove_initial_fictive_state(alphabet, d_inv_fsm_obj, fictive_state, fictive_alpha)
        if final_states_empty:
            d_inv_fsm_obj._initial_states.clear()

        # 3. r(d(r(A)))
        inv_fsm_obj = d_inv_fsm_obj.reverse()

        # --- add initial fictive state
        fictive_state, fictive_alpha = add_initial_fictive_state(alphabet, inv_fsm_obj)

        # 4. d(r(d(r(A))))
        d_inv_fsm_obj = DeterministicFSM.from_fsm(inv_fsm_obj, None)

        # remove initial fictive state
        remove_initial_fictive_state(alphabet, d_inv_fsm_obj, fictive_state, fictive_alpha)

        return DeterministicFSM.from_fsm(d_inv_fsm_obj, name_of_state_generator)

    @classmethod
    def from_original(cls, fsm: Dict[Hashable, Dict[Hashable, Union[Hashable, Set[Hashable]]]],
                      initial_states: Set[Hashable], final_states: Set[Hashable],
                      name_of_state_generator=...):
        fsm_obj = super().from_original(fsm, initial_states, final_states)
        return cls.from_fsm(fsm_obj, name_of_state_generator)

    @classmethod
    def from_fsm(cls, fsm_obj: FSM, name_of_state_generator=...):
        if name_of_state_generator is ...:
            name_of_state_generator = map(str, count(1, 1))
        if name_of_state_generator is not None:
            if not hasattr(name_of_state_generator, '__iter__'):
                raise RuntimeError('Generator must have __iter__ method')
            name_of_state_generator = iter(name_of_state_generator)

        fsm_obj = fsm_obj.eliminate_epsilon_transitions()
        fsm = fsm_obj.fsm_deepcopy()
        initial_states = fsm_obj.initial_states_deepcopy()
        final_states = fsm_obj.final_states_deepcopy()

        if not fsm or not initial_states:
            return DeterministicFSM(fsm=dict(), initial_states=set(), final_states=set())

        new_fsm = {initial_state: dict() for initial_state in initial_states}
        new_initial_states = initial_states.copy()
        new_final_states = set()
        q: collections.deque = collections.deque(initial_states)
        seen = set()
        while q:
            state_from = q.popleft()
            if state_from in seen:
                continue
            seen.add(state_from)
            if isinstance(state_from, State):
                if state_from in final_states:
                    new_final_states.add(state_from)
                for transition, state_or_set_of_states in fsm.get(state_from, dict()).items():
                    if isinstance(state_or_set_of_states, (set, frozenset)) and len(state_or_set_of_states) == 1:
                        state_or_set_of_states = next(iter(state_or_set_of_states))
                    if isinstance(state_or_set_of_states, (set, frozenset)) and len(state_or_set_of_states) > 1:
                        is_final_state = bool(state_or_set_of_states.intersection(final_states))
                        new_state_frozenset = frozenset(state_or_set_of_states)
                        new_state = State(new_state_frozenset)
                        new_fsm.setdefault(state_from, dict())[transition] = new_state
                        new_fsm.setdefault(new_state, dict())
                        if is_final_state:
                            new_final_states.add(new_state)
                        q.append(new_state_frozenset)
                    elif isinstance(state_or_set_of_states, State):
                        new_fsm.setdefault(state_from, dict())[transition] = state_or_set_of_states
                        new_fsm.setdefault(state_or_set_of_states, dict())
                        q.append(state_or_set_of_states)
            elif isinstance(state_from, (set, frozenset)):
                states = frozenset(state_from)
                state_of_old_states = State(states)
                if not states.isdisjoint(final_states) or state_of_old_states in final_states:
                    new_final_states.add(state_of_old_states)
                transitions = dict()
                for old_state_to in states:
                    for transition, state_or_set_of_states in fsm.get(old_state_to, dict()).items():
                        if isinstance(state_or_set_of_states, (set, frozenset)):
                            transitions.setdefault(transition, set()).update(state_or_set_of_states)
                        elif isinstance(state_or_set_of_states, State):
                            transitions.setdefault(transition, set()).add(state_or_set_of_states)
                for transition, set_of_states in transitions.items():
                    if len(set_of_states) > 1:
                        new_state_frozenset = frozenset(set_of_states)
                        new_state = State(new_state_frozenset)
                        new_fsm.setdefault(state_of_old_states, dict())[transition] = new_state
                        new_fsm.setdefault(new_state, dict())
                        q.append(new_state_frozenset)
                    elif len(set_of_states) == 1:
                        new_state = next(iter(set_of_states))
                        new_fsm.setdefault(state_of_old_states, dict())[transition] = new_state
                        new_fsm.setdefault(new_state, dict())
                        q.append(new_state)
        new_initial_states.intersection_update(new_fsm)
        new_final_states.intersection_update(new_fsm)
        if name_of_state_generator is not None:
            all_states = {state: State(next(name_of_state_generator)) for state in new_initial_states}
            all_states.update({state: State(next(name_of_state_generator))
                               for state in set(new_fsm).difference(all_states)})
            new_fsm = {
                all_states[state_from]: {
                    transition: all_states[state_to]
                    for transition, state_to in transitions.items()
                }
                for state_from, transitions in new_fsm.items()
            }
            new_initial_states = set(map(all_states.get, new_initial_states))
            new_final_states = set(map(all_states.get, new_final_states))
        return DeterministicFSM(fsm=new_fsm, initial_states=new_initial_states, final_states=new_final_states)

    @classmethod
    def _check_dfsm(cls, fsm: Dict[State, Dict[Transition, Union[State, Set[State]]]], *, allow_none):
        cls_name = cls.__name__
        if allow_none and fsm is None:
            return
        if not (isinstance(fsm, dict) and all(isinstance(k, State) and isinstance(v, dict) and all(
                isinstance(t, Transition) and isinstance(s, State) for t, s in v.items()) for k, v in fsm.items())):
            raise TypeError(f'{cls_name}. Argument must be None or '
                            f'Dict[State, Dict[Transition, Union[State, Set[State]]]]; got: {type(fsm)}')
