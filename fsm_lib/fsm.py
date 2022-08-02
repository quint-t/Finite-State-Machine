import random
from copy import deepcopy
from typing import Dict, Set, Union, Hashable, Iterable, Literal

from .state import State
from .transition import Transition
from .utils import fsm_plot


class FSM:
    __slots__ = ('_fsm', '_initial_states', '_final_states')

    def __init__(self, *,
                 fsm: Dict[State, Dict[Transition, Union[State, Set[State]]]] = None,
                 initial_states: Set[State] = None,
                 final_states: Set[State] = None):
        self._check_fsm(fsm, allow_none=True)
        self._check_set_of_states(initial_states, allow_none=True)
        self._check_set_of_states(final_states, allow_none=True)
        self._fsm = deepcopy(fsm) if fsm is not None else dict()
        self._initial_states = deepcopy(initial_states) if initial_states is not None else set()
        self._final_states = deepcopy(final_states) if final_states is not None else set()

    def add_transition(self, state_from: State, transition: Transition, state_to: State) -> bool:
        self._check_state(state_from, allow_none=False)
        self._check_transition(transition, allow_none=False)
        self._check_state(state_to, allow_none=False)
        self._fsm.setdefault(state_from, dict())
        self._fsm.setdefault(state_to, dict())
        transitions = self._fsm.get(state_from)
        state_or_set_of_states = transitions.get(transition)
        if state_or_set_of_states is not None:
            if isinstance(state_or_set_of_states, set):
                if state_to not in state_or_set_of_states:
                    state_or_set_of_states.add(state_to)
                    return True
                return False
            if isinstance(state_or_set_of_states, State):
                if state_to != state_or_set_of_states:
                    transitions[transition] = {state_or_set_of_states, state_to}
                    return True
                return False
        transitions[transition] = state_to
        return True

    def add_transitions(self, state_from: State, transition: Transition, states_to: Set[State]) -> bool:
        self._check_state(state_from, allow_none=False)
        self._check_transition(transition, allow_none=False)
        self._check_set_of_states(states_to, allow_none=False)
        self._fsm.setdefault(state_from, dict())
        transitions = self._fsm.get(state_from)
        state_or_set_of_states = transitions.get(transition)
        changed = False
        for state_to in states_to:
            self._fsm.setdefault(state_to, dict())
            if state_or_set_of_states is not None:
                if isinstance(state_or_set_of_states, set):
                    if state_to not in state_or_set_of_states:
                        state_or_set_of_states.add(state_to)
                        changed = True
                    continue
                if isinstance(state_or_set_of_states, State):
                    if state_to != state_or_set_of_states:
                        x = transitions[transition] = {state_or_set_of_states, state_to}
                        state_or_set_of_states = x
                        changed = True
                    continue
            transitions[transition] = state_to
            changed = True
        return changed

    def set_transition(self, state_from: State, transition: Transition, state_to: State, replace=True) -> bool:
        self._check_state(state_from, allow_none=False)
        self._check_transition(transition, allow_none=False)
        self._check_state(state_to, allow_none=False)
        self._fsm.setdefault(state_from, dict())
        self._fsm.setdefault(state_to, dict())
        transitions = self._fsm.get(state_from)
        old_state_to = transitions.get(transition)
        if old_state_to is not None and (not isinstance(old_state_to, set) or bool(old_state_to)) and not replace:
            return False
        changed = old_state_to != state_to
        transitions[transition] = state_to
        return changed

    def set_transitions(self, state_from: State, transition: Transition, states_to: Set[State], replace=True) -> bool:
        self._check_state(state_from, allow_none=False)
        self._check_transition(transition, allow_none=False)
        self._check_set_of_states(states_to, allow_none=False)
        self._fsm.setdefault(state_from, dict())
        for state in states_to:
            self._fsm.setdefault(state, dict())
        transitions = self._fsm.get(state_from)
        old_state_to = transitions.get(transition)
        if old_state_to is not None and (not isinstance(old_state_to, set) or bool(old_state_to)) and not replace:
            return False
        changed = old_state_to != states_to
        transitions[transition] = states_to
        return changed

    def remove_transition(self, state_from: State, transition: Transition, state_to: State) -> bool:
        self._check_state(state_from, allow_none=False)
        self._check_transition(transition, allow_none=False)
        self._check_state(state_to, allow_none=False)
        transitions = self._fsm.get(state_from)
        if transitions is None:
            return False
        state_or_set_of_states = transitions.get(transition)
        if state_or_set_of_states is None:
            return False
        if isinstance(state_or_set_of_states, State):
            if state_to == state_or_set_of_states:
                transitions.pop(transition)
                return True
        elif isinstance(state_or_set_of_states, set):
            if state_to in state_or_set_of_states:
                state_or_set_of_states.remove(state_to)
                if len(state_or_set_of_states) == 0:
                    transitions.pop(transition)
                return True
        return False

    def remove_transitions(self, state_from: State, transition: Transition, states_to: Set[State]) -> bool:
        self._check_state(state_from, allow_none=False)
        self._check_transition(transition, allow_none=False)
        self._check_set_of_states(states_to, allow_none=False)
        transitions = self._fsm.get(state_from)
        if transitions is None:
            return False
        state_or_set_of_states = transitions.get(transition)
        if state_or_set_of_states is None:
            return False
        changed = False
        for state_to in states_to:
            if isinstance(state_or_set_of_states, set):
                if state_to in state_or_set_of_states:
                    state_or_set_of_states.remove(state_to)
                    if len(state_or_set_of_states) == 0:
                        transitions.pop(transition)
                        return True
                    changed = True
                continue
            if isinstance(state_or_set_of_states, State):
                if state_to == state_or_set_of_states:
                    transitions.pop(transition)
                    return True
                continue
        return changed

    def set_initial_state(self, initial_state: State) -> bool:
        self._check_state(initial_state, allow_none=False)
        if initial_state not in self._fsm:
            raise ValueError()
        if initial_state in self._initial_states:
            return False
        self._initial_states.add(initial_state)
        return True

    def set_initial_states(self, initial_states: Set[State]) -> bool:
        self._check_set_of_states(initial_states, allow_none=False)
        if not initial_states.issubset(self._fsm):
            raise ValueError()
        if initial_states == self._initial_states:
            return False
        self._initial_states.update(initial_states)
        return True

    def set_final_state(self, final_state: State) -> bool:
        self._check_state(final_state, allow_none=False)
        if final_state not in self._fsm:
            raise ValueError()
        if final_state in self._final_states:
            return False
        self._final_states.add(final_state)
        return True

    def set_final_states(self, final_states: Set[State]) -> bool:
        self._check_set_of_states(final_states, allow_none=False)
        if not final_states.issubset(self._fsm):
            raise ValueError()
        if final_states == self._final_states:
            return False
        self._final_states.update(final_states)
        return True

    def unset_initial_state(self, initial_state: State) -> bool:
        self._check_state(initial_state, allow_none=False)
        if initial_state not in self._initial_states:
            return False
        self._initial_states.remove(initial_state)
        return True

    def unset_initial_states(self, initial_states: Set[State]) -> bool:
        self._check_set_of_states(initial_states, allow_none=False)
        if self._initial_states.issuperset(initial_states):
            return False
        self._initial_states.difference_update(initial_states)
        return True

    def unset_final_state(self, final_state: State) -> bool:
        self._check_state(final_state, allow_none=False)
        if final_state not in self._final_states:
            return False
        self._final_states.remove(final_state)
        return True

    def unset_final_states(self, final_states: Set[State]) -> bool:
        self._check_set_of_states(final_states, allow_none=False)
        if self._final_states.issuperset(final_states):
            return False
        self._final_states.difference_update(final_states)
        return True

    def remove_state(self, state: State) -> Union[Dict[Transition, Union[State, Set[State]]], None]:
        self._check_state(state, allow_none=False)
        if state not in self._fsm:
            return None
        transitions = self._fsm.pop(state)
        if state in self._initial_states:
            self._initial_states.remove(state)
        if state in self._final_states:
            self._final_states.remove(state)
        return transitions

    def remove_states(self, states: Set[State]) -> None:
        self._check_set_of_states(states, allow_none=False)
        for state in states:
            self._fsm.pop(state)
            if state in self._initial_states:
                self._initial_states.remove(state)
            if state in self._final_states:
                self._final_states.remove(state)

    def clear_initial_states(self) -> bool:
        if not self._initial_states:
            return False
        self._initial_states.clear()
        return True

    def clear_final_states(self) -> bool:
        if not self._final_states:
            return False
        self._final_states.clear()
        return True

    def has_state(self, state: State):
        self._check_state(state, allow_none=False)
        return state in self._fsm

    def has_all_states(self, states: Set[State]):
        self._check_set_of_states(states, allow_none=False)
        return states.issubset(self._fsm)

    def has_any_states(self, states: Set[State]):
        self._check_set_of_states(states, allow_none=False)
        return not states.isdisjoint(self._fsm)

    def get_states(self) -> Set[State]:
        return set(self._fsm.keys())

    def copy(self):
        return self.__class__(fsm=self._fsm, initial_states=self._initial_states, final_states=self._final_states)

    def fsm_deepcopy(self) -> Dict[State, Dict[Transition, Union[State, Set[State]]]]:
        return deepcopy(self._fsm)

    def initial_states_deepcopy(self) -> Set[State]:
        return deepcopy(self._initial_states)

    def final_states_deepcopy(self) -> Set[State]:
        return deepcopy(self._final_states)

    def to_original(self) -> (Dict[Hashable, Dict[Hashable, Union[Hashable, Set[Hashable]]]],
                              Set[Hashable], Set[Hashable]):
        fsm = dict()
        for state_from, transitions in self._fsm.items():
            fsm.setdefault(state_from.uid, dict())
            for transition, state_to in transitions.items():
                fsm[state_from.uid][transition.label] = state_to.uid if isinstance(state_to, State) \
                    else set(state.uid for state in state_to) \
                    if isinstance(state_to, (set, frozenset)) else state_to
        initial_states = {state.uid for state in self._initial_states}
        final_states = {state.uid for state in self._final_states}
        return fsm, initial_states, final_states

    def alphabet(self):
        alphabet = set()
        for transitions in self._fsm.values():
            alphabet.update(transitions.keys())
        return alphabet

    def __str__(self) -> str:
        indent = ' ' * 4
        r = ['{']
        for state_from, transitions in sorted(self._fsm.items()):
            state_type = ''
            state_type += ' [initial state]' if state_from in self._initial_states else ''
            state_type += ' [final state]' if state_from in self._final_states else ''
            state_from = '(' + ', '.join(map(str, state_from.uid)) + ')' \
                if isinstance(state_from.uid, tuple) else state_from
            if not transitions:
                r.append(f"{indent}{state_from}{state_type}: " + '{},')
                continue
            r.append(f"{indent}{state_from}{state_type}: " + '{')
            for transition, state_to in transitions.items():
                if isinstance(state_to, (set, frozenset)):
                    state_to = '{' + ', '.join(map(str, state_to)) + '}'
                elif isinstance(state_to, State) and isinstance(state_to.uid, tuple):
                    state_to = '(' + ', '.join(map(str, state_to.uid)) + ')'
                r.append(f"{indent}{indent}{transition}: {state_to},")
            if r[-1][-1] == ',':
                r[-1] = r[-1][:-1]
            r.append(indent + '},')
        if r[-1][-1] == ',':
            r[-1] = r[-1][:-1]
        r.append('}')
        return '\n'.join(r)

    def __repr__(self) -> str:
        indent = ' ' * 4
        d_indent = indent * 2
        t_indent = indent * 3
        r = [f'{self.__class__.__name__}(\n{indent}' + 'fsm={']
        for state_from, transitions in sorted(self._fsm.items()):
            if not transitions:
                r.append(f"{d_indent}{repr(state_from)}: " + '{},')
                continue
            r.append(f"{d_indent}{repr(state_from)}: " + '{')
            for transition, state_to in transitions.items():
                r.append(f"{t_indent}{repr(transition)}: {repr(state_to)},")
            if r[-1][-1] == ',':
                r[-1] = r[-1][:-1]
            r.append(d_indent + '},')
        if r[-1][-1] == ',':
            r[-1] = r[-1][:-1]
        r.append(indent + '},\n' +
                 f'{indent}initial_states={repr(self._initial_states)},\n{indent}'
                 f'final_states={repr(self._final_states)}')
        r.append(')')
        return '\n'.join(r)

    def __eq__(self, other) -> bool:
        return self._fsm == other._fsm and self._initial_states == other._initial_states and \
               self._final_states == other._final_states if isinstance(other, self.__class__) else False

    def __hash__(self) -> int:
        fsm = []
        for state_from, transitions in self._fsm.items():
            for transition, state_to in transitions.items():
                if isinstance(state_to, set):
                    state_to = tuple(sorted(state_to))
                fsm.append((state_from, transition, state_to))
        fsm.sort()
        fsm = tuple(fsm)
        initial_states = tuple(self._initial_states)
        final_states = tuple(self._final_states)
        return hash((fsm, initial_states, final_states))

    def __iter__(self):
        for state_from, transitions in self._fsm.items():
            for transition, state_to in transitions.items():
                yield state_from, transition, state_to

    @classmethod
    def _check_fsm(cls, fsm: Dict[State, Dict[Transition, Union[State, Set[State]]]], *, allow_none):
        cls_name = cls.__name__
        if allow_none and fsm is None:
            return
        if not (isinstance(fsm, dict) and all(isinstance(k, State) and isinstance(v, dict) and all(
                isinstance(t, Transition) and (isinstance(s, State) or isinstance(s, set) and
                                               all(isinstance(x, State) for x in s))
                for t, s in v.items()) for k, v in fsm.items())):
            raise TypeError(f'{cls_name}. Argument must be None or '
                            f'Dict[State, Dict[Transition, Union[State, Set[State]]]]; got: {type(fsm)}')

    @classmethod
    def _check_set_of_states(cls, states: Set[State], *, allow_none):
        cls_name = cls.__name__
        if allow_none and states is None:
            return
        if not (isinstance(states, (set, frozenset)) and all(isinstance(s, State) for s in states)):
            raise TypeError(f'{cls_name}. Argument `initial_states` must be None or Set[State]')

    @classmethod
    def _check_state(cls, state: State, *, allow_none):
        cls_name = cls.__name__
        if allow_none and state is None:
            return
        if not isinstance(state, State):
            raise TypeError(f'`{cls_name}._check_state`: Expected object of class State, got: {type(state)}')

    @classmethod
    def _check_transition(cls, transition: Transition, *, allow_none):
        cls_name = cls.__name__
        if allow_none and transition is None:
            return
        if not isinstance(transition, Transition):
            raise TypeError(
                f'`{cls_name}._check_transition`: Expected object of class Transition, got: {type(transition)}')

    @classmethod
    def _check_fsm_class(cls, other):
        cls_name = cls.__name__
        if not isinstance(other, cls):
            raise TypeError(f'{cls_name}. Argument must be an object of class {cls_name}, got: {type(other)}')

    @classmethod
    def from_original(cls, fsm: Dict[Hashable, Dict[Hashable, Union[Hashable, Set[Hashable]]]],
                      initial_states: Set[Hashable], final_states: Set[Hashable]):
        cls_name = cls.__name__
        if not (isinstance(fsm, dict) and all(isinstance(k, Hashable) and isinstance(v, dict) and all(
                isinstance(t, Hashable) and (isinstance(s, Hashable) or isinstance(s, set) and
                                             all(isinstance(x, Hashable) for x in s))
                for t, s in v.items()) for k, v in fsm.items())):
            raise TypeError(f'{cls_name}. Argument must be None or '
                            f'Dict[Hashable, Dict[Hashable, Union[Hashable, Set[Hashable]]]]; got: {type(fsm)}')
        if not (isinstance(initial_states, set) and all(isinstance(s, Hashable) for s in initial_states)):
            raise TypeError(f'{cls_name}. Argument `initial_states` must be None or Set[Hashable]')
        if not (isinstance(final_states, set) and all(isinstance(s, Hashable) for s in final_states)):
            raise TypeError(f'{cls_name}. Argument `final_states` must be None or Set[Hashable]')
        new_fsm = dict()
        for state_from, transitions in fsm.items():
            if not isinstance(state_from, State):
                state_from = State(state_from)
            new_fsm.setdefault(state_from, dict())
            for transition, state_to in transitions.items():
                if not isinstance(transition, Transition):
                    transition = Transition(transition)
                if not isinstance(state_to, set) and not isinstance(state_to, State):
                    state_to = State(state_to)
                elif isinstance(state_to, set):
                    state_to = {s if isinstance(s, State) else State(s) for s in state_to}
                new_fsm[state_from].setdefault(transition, state_to)
        fsm = new_fsm
        initial_states = {s if isinstance(s, State) else State(s) for s in initial_states}
        final_states = {s if isinstance(s, State) else State(s) for s in final_states}
        return FSM(fsm=fsm, initial_states=initial_states, final_states=final_states)

    @classmethod
    def generate(cls, deterministic: bool,
                 states_alphabet: Iterable, min_states: int, max_states: int,
                 transitions_alphabet: Union[str, list, tuple, set], min_transitions_from_state: int,
                 max_transitions_from_state: int,
                 min_initial_states: int, max_initial_states: int,
                 min_final_states: int, max_final_states: int):
        if not isinstance(deterministic, bool):
            raise TypeError()
        if not hasattr(states_alphabet, '__iter__'):
            raise TypeError()
        if not isinstance(transitions_alphabet, (str, list, tuple, set)):
            raise TypeError()
        if not isinstance(min_states, int) or not isinstance(max_states, int):
            raise TypeError()
        if not isinstance(min_transitions_from_state, int) or not isinstance(max_transitions_from_state, int):
            raise TypeError()
        if not isinstance(min_initial_states, int) or not isinstance(max_initial_states, int):
            raise TypeError()
        if not isinstance(min_final_states, int) or not isinstance(max_final_states, int):
            raise TypeError()
        states_alphabet = iter(states_alphabet)
        transitions_alphabet = iter(transitions_alphabet)
        fsm = dict()
        states = [next(states_alphabet) for _ in range(max_states)]
        states = [s if isinstance(s, State) else State(s) for s in states]
        transitions = random.choices(population=list(transitions_alphabet), k=max_transitions_from_state)
        transitions = [t if isinstance(t, Transition) else Transition(t) for t in transitions]
        states = random.sample(population=states, k=random.randint(min_states, max_states))
        for state in states:
            fsm[state] = dict()
            for transition in random.sample(population=transitions, k=random.randint(min_transitions_from_state,
                                                                                     max_transitions_from_state)):
                if deterministic:
                    fsm[state][transition] = random.choice(states)
                else:
                    fsm[state][transition] = set(random.sample(population=states,
                                                               k=random.randint(min(len(states),
                                                                                    min_transitions_from_state),
                                                                                min(len(states),
                                                                                    max_transitions_from_state))))
        initial_states = set(random.sample(population=states, k=random.randint(min(len(states), min_initial_states),
                                                                               min(len(states), max_initial_states))))
        final_states = set(random.sample(population=states, k=random.randint(min(len(states), min_final_states),
                                                                             min(len(states), max_final_states))))
        return FSM(fsm=fsm, initial_states=set(initial_states), final_states=set(final_states))

    def eliminate_epsilon_transitions(self):
        fsm = self._fsm
        initial_states = self._initial_states
        final_states = self._final_states

        if not fsm or not initial_states:
            return FSM(fsm=dict(), initial_states=set(), final_states=set())

        new_fsm = dict()
        new_initial_states = initial_states.copy()
        new_final_states = final_states.copy()
        from_state_to_state_by_epsilon = dict()

        b = False
        for state_from, transitions in fsm.items():
            new_fsm.setdefault(state_from, dict())
            from_state_to_state_by_epsilon.setdefault(state_from, set())
            for transition, states_to in transitions.items():
                if transition.is_epsilon():
                    b = True
                    all_states = {state_from}
                    if isinstance(states_to, (set, frozenset)):
                        all_states.update(state_to for state_to in states_to if state_to in fsm)
                    elif isinstance(states_to, State) and states_to in fsm:
                        all_states.add(states_to)
                    from_state_to_state_by_epsilon[state_from].update(all_states)
                else:
                    new_fsm[state_from].setdefault(transition, set())
                    if isinstance(states_to, (set, frozenset)):
                        new_fsm[state_from][transition].update(state_to for state_to in states_to if state_to in fsm)
                    elif isinstance(states_to, State) and states_to in fsm:
                        new_fsm[state_from][transition].add(states_to)
        while b:
            b = False
            for state_from, next_states in from_state_to_state_by_epsilon.items():
                states_by_epsilon = from_state_to_state_by_epsilon.get(state_from, set())
                for next_state in next_states.copy():
                    previous_length = len(states_by_epsilon)
                    states_by_epsilon.update(from_state_to_state_by_epsilon.get(next_state, set()))
                    b |= (previous_length != len(states_by_epsilon))
        for state_from, next_states in from_state_to_state_by_epsilon.items():
            for next_state in next_states:
                for transition, states_to in new_fsm[next_state].items():
                    new_fsm[state_from].setdefault(transition, set()).update(states_to)
            if state_from in new_initial_states:
                new_initial_states.update(next_states)
            if not new_final_states.isdisjoint(next_states):
                new_final_states.add(state_from)

        return FSM(fsm=new_fsm, initial_states=new_initial_states, final_states=new_final_states)

    def reverse(self):
        inv_fsm = dict()
        for state, transitions in self._fsm.items():
            inv_fsm.setdefault(state, dict())
            for transition, states_to in transitions.items():
                if isinstance(states_to, State):
                    states_to = {states_to}
                for state_to in states_to:
                    inv_fsm.setdefault(state_to, dict()).setdefault(transition, set()).add(state)
        return FSM(fsm=inv_fsm, initial_states=self._final_states.copy(),
                   final_states=self._initial_states.copy())

    def plot(self, filename: str, rankdir: Union[Literal['TB'], Literal['BT'], Literal['LR'], Literal['RL']] = 'TB'):
        fsm_plot(filename, *self.to_original(), rankdir=rankdir)
