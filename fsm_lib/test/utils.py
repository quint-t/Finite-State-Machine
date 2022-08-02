import collections
import re
from typing import Union


def to_flatten_tuple(any_arg: Union[int, str, tuple, list, set]) -> tuple:
    return tuple(re.findall(pattern=r'\w+', string=str(any_arg)))


def is_dfa_equals(min_fsm: dict,
                  min_initial_states: Union[set, tuple, str],
                  min_final_states: Union[set, tuple, str],
                  orig_fsm: dict,
                  orig_initial_states: Union[set, tuple, str],
                  orig_final_states: Union[set, tuple, str]):
    """
    Compares two DFA's for equality by transitions and final states
    (return value can be True for DFA with different numbers of states, transitions, etc.).
    """
    min_initial_states = set(min_initial_states) if isinstance(min_initial_states, (set, list)) else {
        min_initial_states}
    min_final_states = set(min_final_states) if isinstance(min_final_states, (set, list)) else {min_final_states}
    orig_initial_states = set(orig_initial_states) if isinstance(orig_initial_states, (set, list)) else {
        orig_initial_states}
    orig_final_states = set(orig_final_states) if isinstance(orig_final_states, (set, list)) else {orig_final_states}

    for state, alphas in min_fsm.items():
        for alpha, alpha_state in alphas.items():
            if not isinstance(alpha_state, (int, str)):
                print('Expected FSM is not DFA')
                print(f'Expected FSM: {min_fsm} (initial={min_initial_states}, final={min_final_states})')
                print(f'Founded: {state} -- {alpha} --> {alpha_state}')
                return False

    for state, alphas in orig_fsm.items():
        for alpha, alpha_state in alphas.items():
            if not isinstance(alpha_state, (int, str)):
                print('Actual FSM is not DFA')
                print(f'Actual FSM: {orig_fsm} (initial={orig_initial_states}, final={orig_final_states})')
                print(f'Founded: {state} -- {alpha} --> {alpha_state}')
                return False

    def construct_paths(fsm, initial_states, final_states):
        q = collections.deque([(state, fsm[state], []) for state in initial_states])
        paths = set()
        seen = set()
        used_states = set()
        while q:
            state, next_transitions, stack = q.popleft()
            used_states.add(state)
            if state in seen:
                paths.add(tuple(stack))
                continue
            seen.add(state)
            if next_transitions:
                for alpha, alpha_state in next_transitions.items():
                    q.appendleft((alpha_state,
                                  fsm[alpha_state],
                                  stack + [(alpha, tuple(sorted(fsm[alpha_state])),
                                            'F' * (alpha_state in final_states))]))
            else:
                paths.add(tuple(stack))
        b = True
        for state in initial_states.union(final_states).union(fsm):
            if state not in used_states:
                print(f'State {state} is unused in FSM [{fsm} (initial={initial_states}, final={final_states})]')
                b = False
        return paths if b else None

    def check(paths, fsm, initial_states, final_states):
        for path in paths:
            b = True
            attempts = []
            initial_states_last_index = len(initial_states) - 1
            for i, initial_state in enumerate(initial_states):
                current_state = initial_state
                new_path = [current_state]
                b = True
                for t in path:
                    alpha, transitions, state_type = t
                    must_be_final = (state_type == 'F')
                    if current_state not in fsm or alpha not in fsm[current_state]:
                        b = False
                        if i == initial_states_last_index:
                            if current_state not in fsm:
                                print(f'State {current_state} is not in FSM')
                            else:
                                print(f'Transition {alpha} is not in {fsm[current_state]} (state = {current_state})')
                        break
                    current_state = fsm[current_state][alpha]
                    new_path.append((alpha, current_state))
                    if transitions != tuple(sorted(fsm[current_state])):
                        b = False
                        if i == initial_states_last_index:
                            print(
                                f'Expected transitions {transitions} != Actual transitions {tuple(sorted(fsm[current_state]))}')
                        break
                    if must_be_final and current_state not in final_states:
                        b = False
                        if i == initial_states_last_index:
                            print(f'State {current_state} is not in final states: {final_states}')
                        break
                attempts.append(new_path)
                if b:
                    break
            if not b:
                print(f'=== Error ===')
                print(f'Path: {path}')
                print(f'Attempts: {attempts}')
                return False
        return True

    orig_paths = construct_paths(orig_fsm, orig_initial_states, orig_final_states)
    if orig_paths is None:
        return False
    if not check(orig_paths, min_fsm, min_initial_states, min_final_states):
        return False
    min_paths = construct_paths(min_fsm, min_initial_states, min_final_states)
    if min_paths is None:
        return False
    if not check(min_paths, orig_fsm, orig_initial_states, orig_final_states):
        return False
    return True


def is_dfa_isomorphic(min_dfa, initial_states, final_states, new_dfa, new_initial_states, new_final_states):
    """
    Compares two DFA's by isomorphism (not for all sufficient conditions, but for the main ones):
    whether the arguments are DFA's, whether the number of vertices (states) is equal,
    whether the number of arcs (transitions) is equal,
    whether the degrees of the vertices (states) are equal,
    as well as everything that the is_dfa_equals function checks.
    """

    if len(min_dfa) != len(new_dfa):
        print('Number of states of expected DFA != Number of states of actual DFA')
        print(f'Expected DFA: {min_dfa} (initial={initial_states}, final={final_states}) (n_states = {len(min_dfa)})')
        print(
            f'Actual DFA: {new_dfa} (initial={new_initial_states}, final={new_final_states}) (n_states = {len(new_dfa)})')
        return False

    initial_states = set(initial_states) if isinstance(initial_states, (set, list)) else {initial_states}
    final_states = set(final_states) if isinstance(final_states, (set, list)) else {final_states}
    new_initial_states = set(new_initial_states) if isinstance(new_initial_states, (set, list)) else {
        new_initial_states}
    new_final_states = set(new_final_states) if isinstance(new_final_states, (set, list)) else {new_final_states}

    if len(initial_states) != len(new_initial_states):
        print('Number of initial states of expected DFA != Number of initial states of actual DFA')
        print(f'Expected DFA: {min_dfa} (initial={initial_states}, final={final_states})')
        print(f'Actual DFA: {new_dfa} (initial={new_initial_states}, final={new_final_states})')
        return False

    min_dfa_vertices = set()
    new_dfa_vertices = set()
    min_dfa_arcs = 0
    new_dfa_arcs = 0
    min_degrees_of_vertices = dict()
    new_degrees_of_vertices = dict()
    for state, alphas in min_dfa.items():
        min_dfa_vertices.add(state)
        for alpha, alpha_state in alphas.items():
            if not isinstance(alpha_state, (int, str)):
                print('Expected FSM is not DFA')
                print(f'Expected FSM: {min_dfa} (initial={initial_states}, final={final_states})')
                print(f'Founded: {state} -- {alpha} --> {alpha_state}')
                return False
            min_dfa_arcs += 1
            min_degrees_of_vertices.setdefault(state, [0, 0])
            min_degrees_of_vertices[state][0] += 1
            min_degrees_of_vertices.setdefault(alpha_state, [0, 0])
            min_degrees_of_vertices[alpha_state][1] += 1
            min_dfa_vertices.add(alpha_state)
    for state, alphas in new_dfa.items():
        new_dfa_vertices.add(state)
        for alpha, alpha_state in alphas.items():
            if not isinstance(alpha_state, (int, str)):
                print('Actual FSM is not DFA')
                print(f'Actual FSM: {new_dfa} (initial={new_initial_states}, final={new_final_states})')
                print(f'Founded: {state} -- {alpha} --> {alpha_state}')
                return False
            new_dfa_arcs += 1
            new_degrees_of_vertices.setdefault(state, [0, 0])
            new_degrees_of_vertices[state][0] += 1
            new_degrees_of_vertices.setdefault(alpha_state, [0, 0])
            new_degrees_of_vertices[alpha_state][1] += 1
            new_dfa_vertices.add(alpha_state)
    if set(map(tuple, min_degrees_of_vertices.values())) != set(map(tuple, new_degrees_of_vertices.values())):
        print('Degrees of vertices (states) in expected DFA != Degrees of vertices (states) in actual DFA')
        print(f'Expected DFA: {min_dfa} (initial={initial_states}, final={final_states})')
        print(f'Degrees of vertices (states): {min_degrees_of_vertices}')
        print(f'Actual DFA: {new_dfa} (initial={new_initial_states}, final={new_final_states})')
        print(f'Degrees of vertices (states): {new_degrees_of_vertices}')
        return False
    if min_dfa_arcs != new_dfa_arcs:
        print('Number of arcs (transitions) in expected DFA != Number of arcs (transitions) in actual DFA')
        print(
            f'Expected DFA: {min_dfa} (initial={initial_states}, final={final_states}) ({min_dfa_arcs} arcs (transitions))')
        print(
            f'Actual DFA: {new_dfa} (initial={new_initial_states}, final={new_final_states}) ({new_dfa_arcs} arcs (transitions))')
        return False
    min_dfa_vertices_count = len(min_dfa_vertices)
    new_dfa_vertices_count = len(new_dfa_vertices)
    if min_dfa_vertices_count != new_dfa_vertices_count:
        print('Number of vertices (states) in expected DFA != Number of vertices (states) in actual DFA')
        print(
            f'Expected DFA: {min_dfa} (initial={initial_states}, final={final_states}) ({min_dfa_vertices_count} vertices (states))')
        print(
            f'Actual DFA: {new_dfa} (initial={new_initial_states}, final={new_final_states}) ({new_dfa_vertices_count} vertices (states))')
        return False
    if not is_dfa_equals(min_dfa, initial_states, final_states, new_dfa, new_initial_states, new_final_states):
        print(f'Expected DFA: {min_dfa} (initial={initial_states}, final={final_states})')
        print(f'Actual DFA: {new_dfa} (initial={new_initial_states}, final={new_final_states})')
        return False
    return True
