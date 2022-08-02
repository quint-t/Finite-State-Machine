import sys
from typing import Dict, Any, Set, Union, Tuple, List

from fsm_lib import fsm_plot, DeterministicFSM


def fsm_int_states_to_str(fsm: Dict[Any, Dict[Any, Any]]) -> Dict[str, Dict[str, Union[str, Set[str]]]]:
    return {str(state): {str(alpha): set((str(x) for x in sorted(alpha_states)))
    if isinstance(alpha_states, (set, tuple, list)) and len(alpha_states) != 1 else
    str(next(iter(alpha_states)))
    if isinstance(alpha_states, (set, tuple, list)) and len(alpha_states) == 1 else
    str(alpha_states)
                         for alpha, alpha_states in alphas.items()}
            for state, alphas in fsm.items()}


def fsm_startswith(alphabet: str, prefix: str) -> (Dict[str, Dict[str, str]], Set[str], Set[str]):
    if not set(prefix).issubset(alphabet):
        raise Exception('input prefix contains invalid symbol')
    initial_state = 1
    final_state = initial_state + len(prefix)
    fsm = dict()
    fsm[final_state] = {x: {final_state, } for x in alphabet}
    for i, x in enumerate(prefix, initial_state):
        fsm[i] = {x: {i + 1, }}
    fsm = fsm_int_states_to_str(fsm)
    return fsm, {str(initial_state)}, {str(final_state)}


def fsm_endswith(alphabet: str, suffix: str) -> (Dict[str, Dict[str, str]], Set[str], Set[str]):
    if not set(suffix).issubset(alphabet):
        raise Exception('input suffix contains invalid symbol')
    initial_state = 1
    final_state = initial_state + len(suffix)
    fsm = dict()
    fsm[initial_state] = {x: {initial_state, } for x in
                          alphabet}
    if suffix:
        fsm[initial_state][suffix[0]].add(initial_state + 1)
        for i, x in enumerate(suffix[1:], initial_state + 1):
            fsm[i] = {x: {i + 1, }}
        fsm[final_state] = {}
    fsm = fsm_int_states_to_str(fsm)
    dfsm = DeterministicFSM.from_original(fsm, {str(initial_state)}, {str(final_state)})
    return dfsm.minimize().to_original()


def fsm_check(string: str,
              fsm: Dict[str, Dict[str, str]],
              initial_state: Union[str, Tuple[str]],
              final_states: Union[str, Tuple[str],
                                  List[Union[str, Tuple[str]]], Set[Union[str, Tuple[str]]]]) -> bool:
    final_states = set(final_states) if isinstance(final_states, (set, list)) else {final_states}
    state = initial_state
    for x in string:
        transition = fsm.get(state)
        if transition is None:
            return False
        state = transition.get(x)
        if state is None:
            return False
    return state in final_states


def main():
    def print_fsm(fsm: Any, final_states: Any) -> None:
        import pprint
        print('Deterministic FSM:')
        pprint.pprint(fsm)
        print(f'Final states: {final_states}')

    def print_examples(fsm: Dict[str, Dict[str, str]],
                       initial_state: Union[str, Tuple[str]],
                       final_states: Union[str, Tuple[str],
                                           List[Union[str, Tuple[str]]],
                                           Set[Union[str, Tuple[str]]]]) -> None:
        examples = ['', '0', '1', '00', '01', '10', '11', '0001', '1000', '0110', '1100', '0011', '001100', '110011']
        for example in examples:
            result = fsm_check(string=example, fsm=fsm, initial_state=initial_state, final_states=final_states)
            print(f"'{example}': {result}" + (', ' if example != examples[-1] else ''), end='')
        print(end='\n\n')

    def print_fsm_and_examples(alphabet: str, ix: str, task_type: str) -> None:
        if task_type == 'startswith':
            print(f'The words of the language begin with {ix}')
            fsm, initial_states, final_states = fsm_startswith(alphabet=alphabet, prefix=ix)
        elif task_type == 'endswith':
            print(f'The words of the language end with {ix}')
            fsm, initial_states, final_states = fsm_endswith(alphabet=alphabet, suffix=ix)
        else:
            print('Task is missing')
            return None
        print_fsm(fsm, final_states)
        print_examples(fsm, next(iter(initial_states)), final_states)
        try:
            fsm_plot(f'images/{task_type}_{ix}', fsm, initial_states, final_states)
        except Exception as e:
            print(e, file=sys.stderr)
            return None

    alphabet = '01'
    print(f'Alphabet: {alphabet}')

    print_fsm_and_examples(alphabet, '00', 'endswith')

    print_fsm_and_examples(alphabet, '00', 'startswith')

    print_fsm_and_examples(alphabet, '11', 'endswith')

    print_fsm_and_examples(alphabet, '11', 'startswith')

    print_fsm_and_examples(alphabet, '10', 'endswith')

    print_fsm_and_examples(alphabet, '10', 'startswith')

    print_fsm_and_examples(alphabet, '110011', 'endswith')

    print_fsm_and_examples(alphabet, '110011', 'startswith')

    print_fsm_and_examples(alphabet, '001100', 'endswith')

    print_fsm_and_examples(alphabet, '001100', 'startswith')


if __name__ == "__main__":
    main()
