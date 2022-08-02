import collections
import string
import unittest
from copy import deepcopy

from fsm_lib import FSM, DeterministicFSM
from utils import is_dfa_equals, is_dfa_isomorphic


class DeterminationTests(unittest.TestCase):

    def test_example_01(self):
        print('Sample test #1. Minimal DFA (nothing is required)')
        dfa = {
            '1': {'a': '1', 'b': '2'},
            '2': {'a': '1', 'b': '2'}
        }
        initial_states = {'1'}
        final_states = {'2'}
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states).minimize()
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)._brzozowski()
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')

    def test_example_02(self):
        print('Sample test #2. Simple DFA (minimization required)')
        dfa = {
            '1': {'a': '2', 'b': '3'},
            '2': {'a': '2', 'b': '3'},
            '3': {'a': '4', 'b': '4'},
            '4': {}
        }
        min_dfa = {
            '1': {'a': '1', 'b': '3'},
            '3': {'a': '4', 'b': '4'},
            '4': {}
        }
        initial_states = {'1'}
        final_states = {'4'}
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states).minimize()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)._brzozowski()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')

    def test_example_03(self):
        print('Sample test #3. DFA (ids of states and labels of transitions with length > 1)')
        dfa = {
            '.1.': {'-a-': '.2.', '-b-': '.3.', '-c-': '.4.', '-d-': '.5.', '-e-': '.6.'},
            '.2.': {'-a-': '.2.', '-b-': '.3.', '-c-': '.4.', '-d-': '.5.', '-e-': '.6.'},
            '.3.': {'-a-': '.2.', '-b-': '.3.', '-c-': '.4.', '-d-': '.5.', '-e-': '.6.'},
            '.4.': {'-a-': '.2.', '-b-': '.3.', '-c-': '.4.', '-d-': '.5.', '-e-': '.6.'},
            '.5.': {'-a-': '.2.', '-b-': '.3.', '-c-': '.4.', '-d-': '.5.', '-e-': '.6.'},
            '.6.': {'-a-': '.2.', '-b-': '.3.', '-c-': '.4.', '-d-': '.5.', '-e-': '.7.'},
            '.7.': {},
        }
        min_dfa = {
            '.1.': {'-c-': '.1.', '-b-': '.1.', '-e-': '.6.', '-a-': '.1.', '-d-': '.1.'},
            '.6.': {'-c-': '.1.', '-b-': '.1.', '-e-': '.7.', '-a-': '.1.', '-d-': '.1.'},
            '.7.': {}
        }
        initial_states = {'.1.'}
        final_states = {'.7.'}
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states).minimize()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)._brzozowski()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')

    def test_example_04(self):
        print('Sample test #4. Simple NFA')
        nfa = {
            '0': {'a': {'1', '2'}, 'b': '2'},
            '1': {'a': '2', 'b': '3'},
            '2': {'a': {'1', '2'}, 'b': '3'},
            '3': {}
        }
        dfa = {
            '0': {'a': '1', 'b': '2'},
            '1': {'a': '1', 'b': '3'},
            '2': {'a': '1', 'b': '3'},
            '3': {}
        }
        min_dfa = {
            '0': {'a': '1', 'b': '1'},
            '1': {'a': '1', 'b': '3'},
            '3': {}
        }
        initial_states = {'0'}
        final_states = {'3'}
        _nfa, _dfa = deepcopy(nfa), deepcopy(dfa)
        _initial_states, _final_states = deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states).minimize()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)._brzozowski()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')

    def test_example_05(self):
        print('Sample test #5. Simple NFA (ids of states and labels of transitions with length > 1)')
        nfa = {
            '.0.': {'-a-': {'.1.', '.2.'}, '-b-': '.2.'},
            '.1.': {'-a-': '.2.', '-b-': '.3.'},
            '.2.': {'-a-': {'.1.', '.2.'}, '-b-': '.3.'},
            '.3.': {}
        }
        dfa = {
            '.0.': {'-a-': '.1.', '-b-': '.2.'},
            '.1.': {'-a-': '.1.', '-b-': '.3.'},
            '.2.': {'-a-': '.1.', '-b-': '.3.'},
            '.3.': {}
        }
        min_dfa = {
            '.0.': {'-a-': '.1.', '-b-': '.1.'},
            '.1.': {'-a-': '.1.', '-b-': '.3.'},
            '.3.': {}
        }
        initial_states = {'.0.'}
        final_states = {'.3.'}
        _nfa, _dfa = deepcopy(nfa), deepcopy(dfa)
        _initial_states, _final_states = deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states).minimize()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)._brzozowski()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')

    def test_example_06(self):
        print('Sample test #6. Epsilon-NFA')
        nfa = {
            '.1.': {'-b-': '.2.'},
            '.2.': {'-b-': '.4.', 'ε': '.3.'},
            '.3.': {'-c-': '.5.', 'ε': '.1.'},
            '.4.': {'-a-': '.2.', '-c-': '.5.'},
            '.5.': {'-b-': '.4.', 'ε': '.3.'}
        }
        dfa = {
            '.1.': {'-b-': '.2.'},
            '.2.': {'-b-': '.4.', '-c-': '.3.'},
            '.3.': {'-b-': '.4.', '-c-': '.3.'},
            '.4.': {'-a-': '.2.', '-c-': '.3.', '-b-': '.4.'},
        }
        min_dfa = {
            '.1.': {'-b-': '.2.'},
            '.2.': {'-b-': '.4.', '-c-': '.2.'},
            '.4.': {'-a-': '.2.', '-b-': '.4.', '-c-': '.2.'},
        }
        initial_states = {'.1.'}
        final_states = {'.4.'}
        _nfa, _dfa = deepcopy(nfa), deepcopy(dfa)
        _initial_states, _final_states = deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states).minimize()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')
        _dfa, _initial_states, _final_states = deepcopy(dfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_dfa, _initial_states, _final_states)._brzozowski()
        self.assertTrue(is_dfa_equals(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, initial_states, final_states, *mdfsm.to_original()),
                        'Not isomorphic')

    def test_example_07(self):
        print('Sample test #7. Empty FSM OR Empty initial states')
        dfsm = DeterministicFSM.from_original(dict(), {'.1.'}, {'.7.'})
        self.assertTrue(is_dfa_isomorphic(dict(), set(), set(), *dfsm.to_original()), 'Not isomorphic')
        mdfsm = DeterministicFSM.from_original(dict(), {'.1.'}, {'.7.'}).minimize()
        self.assertTrue(is_dfa_isomorphic(dict(), set(), set(), *mdfsm.to_original()), 'Not isomorphic')

        dfsm = DeterministicFSM.from_original({'1': {'a': '1'}}, set(), {'1'})
        self.assertTrue(is_dfa_isomorphic(dict(), set(), set(), *dfsm.to_original()), 'Not isomorphic')
        mdfsm = DeterministicFSM.from_original({'1': {'a': '1'}}, set(), {'1'}).minimize()
        self.assertTrue(is_dfa_isomorphic(dict(), set(), set(), *mdfsm.to_original()), 'Not isomorphic')

        dfsm = DeterministicFSM.from_original(dict(), set(), {'1'})
        self.assertTrue(is_dfa_isomorphic(dict(), set(), set(), *dfsm.to_original()), 'Not isomorphic')
        mdfsm = DeterministicFSM.from_original(dict(), set(), {'1'}).minimize()
        self.assertTrue(is_dfa_isomorphic(dict(), set(), set(), *mdfsm.to_original()), 'Not isomorphic')

    def test_example_08(self):
        print('Sample test #8. Complex NFA #1')
        nfa = {
            3: {'e': {3, 4, 5}, 'b': {4, 5}, 'f': {4, 5}},
            4: {'b': {4}, 'f': {3}},
            5: {'e': {4}, 'b': {4, 5}}
        }
        initial_states = {4, 5}
        final_states = {3, 4}
        dfa = {
            1: {'b': 1, 'f': 5},
            2: {'e': 1, 'b': 4},
            3: {'e': 3, 'b': 4, 'f': 3},
            4: {'b': 4, 'f': 5, 'e': 1},
            5: {'e': 3, 'b': 4, 'f': 4},
        }
        dfa_initial_states = {1, 2}
        dfa_final_states = {1, 3, 4, 5}
        min_dfa = {
            1: {'b': 1, 'f': 2, 'e': 4},
            2: {'e': 3, 'b': 1, 'f': 1},
            3: {'e': 3, 'b': 1, 'f': 3},
            4: {'b': 4, 'f': 2}
        }
        min_dfa_initial_states = {1}
        min_dfa_final_states = {1, 2, 3, 4}
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, dfa_initial_states, dfa_final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, dfa_initial_states, dfa_final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, dfa_initial_states, dfa_final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, dfa_initial_states, dfa_final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states).minimize()
        self.assertTrue(is_dfa_equals(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not isomorphic')
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)._brzozowski()
        self.assertTrue(is_dfa_equals(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not isomorphic')

    def test_example_09(self):
        print('Sample test #9. Complex NFA #2')
        nfa = {
            1: {'c': {1, 3, 4}, 'ε': {4}},
            3: {'c': {1, 3, 5}, 'd': {1}, 'ε': {1, 3, 5}},
            5: {'d': {1, 5}}, 4: {'d': {1}}
        }
        initial_states = {4, 5}
        final_states = {1, 3, 4}
        dfa = {
            1: {'d': 3},
            2: {'d': 4},
            3: {'c': 5, 'd': 3},
            4: {'c': 5, 'd': 4},
            5: {'c': 6, 'd': 4},
            6: {'c': 6, 'd': 4}
        }
        dfa_initial_states = {1, 2}
        dfa_final_states = {1, 3, 4, 5, 6}
        min_dfa = {
            1: {'d': 2},
            2: {'c': 2, 'd': 2}
        }
        min_dfa_initial_states = {1}
        min_dfa_final_states = {1, 2}
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, dfa_initial_states, dfa_final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, dfa_initial_states, dfa_final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, dfa_initial_states, dfa_final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, dfa_initial_states, dfa_final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states).minimize()
        self.assertTrue(is_dfa_equals(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not isomorphic')
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)._brzozowski()
        self.assertTrue(is_dfa_equals(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not isomorphic')

    def test_example_10(self):
        print('Sample test #10. Complex NFA #3')
        nfa = {
            5: {'c': {2}, 'a': {2}, 'd': {1, 2}},
            2: {'d': {1, 2, 5}},
            1: {'d': {1, 5}, 'c': {1, 2, 5}}
        }
        dfa = {
            2: {'c': 5, 'a': 5, 'd': 4},
            3: {'d': 3, 'c': 3, 'a': 5},
            4: {'d': 3, 'c': 3},
            5: {'d': 3}
        }
        initial_states = {2, 5}
        final_states = set()
        min_dfa = {
            1: {'c': 2, 'a': 2, 'd': 3},
            2: {'d': 3},
            3: {'d': 3, 'c': 3, 'a': 2}
        }
        min_dfa_initial_states = {1}
        min_dfa_final_states = set()
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        dfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)
        self.assertTrue(is_dfa_equals(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(dfa, initial_states, final_states, *dfsm.to_original()),
                        'Not isomorphic')
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states).minimize()
        self.assertTrue(is_dfa_equals(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not isomorphic')
        _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
        mdfsm = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)._brzozowski()
        self.assertTrue(is_dfa_equals(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not equals')
        self.assertTrue(is_dfa_isomorphic(min_dfa, min_dfa_initial_states, min_dfa_final_states, *mdfsm.to_original()),
                        'Not isomorphic')

    def test_minimization(self):
        print('Minimization random tests')
        for _ in range(3000):
            while True:
                fsm = FSM.generate(deterministic=False, states_alphabet=range(1000),
                                   min_states=0, max_states=5, transitions_alphabet='ε' + string.ascii_lowercase[:5],
                                   min_transitions_from_state=0, max_transitions_from_state=5,
                                   min_initial_states=0, max_initial_states=5,
                                   min_final_states=0, max_final_states=5)
                q = collections.deque({x} for x in fsm._fsm.keys())
                next_fsm = False
                while q:
                    set_of_states = q.popleft()
                    updated = False
                    for state in list(set_of_states):
                        for transition, states_to in fsm._fsm[state].items():
                            is_set = isinstance(states_to, (set, frozenset))
                            if is_set and not set_of_states.issuperset(states_to):
                                set_of_states.update(states_to)
                                updated = True
                            elif not is_set and states_to not in set_of_states:
                                set_of_states.add(states_to)
                                updated = True
                    if updated:
                        q.append(set_of_states)
                        continue
                    if set_of_states.isdisjoint(fsm._final_states):
                        next_fsm = True
                        break
                if not next_fsm:
                    break

            nfa, initial_states, final_states = fsm.to_original()
            _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
            minimal_dfsm_1 = DeterministicFSM.from_original(_nfa, _initial_states, _final_states).minimize()
            _nfa, _initial_states, _final_states = deepcopy(nfa), deepcopy(initial_states), deepcopy(final_states)
            minimal_dfsm_2 = DeterministicFSM.from_original(_nfa, _initial_states, _final_states)._brzozowski()
            r = is_dfa_isomorphic(*minimal_dfsm_1.to_original(), *minimal_dfsm_2.to_original())
            if not r:
                print('FSM:', *fsm.to_original())
                print('Expected:', *minimal_dfsm_1.to_original())
                print('Actual:', *minimal_dfsm_2.to_original())
            self.assertTrue(r, 'Not isomorphic')

            r = is_dfa_equals(*minimal_dfsm_1.to_original(), *minimal_dfsm_2.to_original())
            if not r:
                print('FSM:', *fsm.to_original())
                print('Expected:', *minimal_dfsm_1.to_original())
                print('Actual:', *minimal_dfsm_2.to_original())
            self.assertTrue(r, 'Not equals')


if __name__ == '__main__':
    unittest.main()
