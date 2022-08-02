import re
from typing import Any, Tuple, Dict, Union, Set, List, Literal


def to_flatten_tuple(any_arg: Any) -> Tuple[str]:
    return tuple(re.findall(pattern=r'\w+', string=str(any_arg)))


def determine_alphabet(fsm: Dict[Any, Dict[Union[str, Tuple[str]], Any]]) -> Set[str]:
    alphabet = set()
    for alphas in fsm.values():
        alphabet.update(alphas.keys())
    return alphabet


def fsm_plot(filename: str,
             fsm: Dict[Union[str, Tuple[str]],
                       Dict[str, Union[str, Tuple[str], Set[Union[str, Tuple[str]]]]]],
             initial_states: Union[str, Tuple[str],
                                   List[Union[str, Tuple[str]]], Set[Union[str, Tuple[str]]]],
             final_states: Union[str, Tuple[str],
                                 List[Union[str, Tuple[str]]], Set[Union[str, Tuple[str]]]],
             rankdir: Union[Literal['TB'], Literal['BT'], Literal['LR'], Literal['RL']] = 'TB') -> None:
    import graphviz
    G = graphviz.Digraph()
    G.attr('graph', rankdir=rankdir)
    G.node('start', None, {'shape': 'point'})
    initial_states = set(initial_states) if isinstance(initial_states, (set, list)) else {initial_states}
    final_states = set(final_states) if isinstance(final_states, (set, list)) else {final_states}
    for state in fsm:
        G.attr('node', shape='doublecircle' if state in final_states else 'circle')
        G.node(','.join(map(str, state)) if isinstance(state, tuple) else str(state))
    G.attr('node', shape='point')
    for state, alphas in fsm.items():
        if state in initial_states:
            G.edge(tail_name='start', head_name=str(state), label='')
        arcs = dict()
        for alpha, alpha_states in alphas.items():
            if isinstance(alpha_states, (str, tuple)):
                alpha_states = {alpha_states}
            for alpha_state in alpha_states:
                if state != alpha_state:
                    arcs.setdefault(alpha_state, set())
                    arcs[alpha_state].add(alpha)
        for alpha_state, alpha_state_alphas in arcs.items():
            G.edge(tail_name=','.join(map(str, state)) if isinstance(state, tuple) else str(state),
                   head_name=','.join(map(str, alpha_state)) if isinstance(alpha_state, tuple) else str(alpha_state),
                   label=','.join(sorted(map(str, alpha_state_alphas), key=to_flatten_tuple)))
        state_alpha_state = set()
        for alpha, alpha_states in alphas.items():
            if isinstance(alpha_states, (str, tuple)):
                alpha_states = {alpha_states}
            for alpha_state in alpha_states:
                if state == alpha_state:
                    state_alpha_state.add(alpha)
                    break
        if state_alpha_state:
            G.edge(tail_name=','.join(map(str, state)) if isinstance(state, tuple) else str(state),
                   head_name=','.join(map(str, state)) if isinstance(state, tuple) else str(state),
                   label=','.join(sorted(map(str, state_alpha_state), key=to_flatten_tuple)))
    G.render(filename, format='png', cleanup=True)
