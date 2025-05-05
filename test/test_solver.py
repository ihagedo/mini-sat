import os
import tempfile
import subprocess
import pytest
from src.cnf_parser import parse_dimacs
from src.dpll import dpll
from src.implication_graph import ImplicationGraph

examples = [
    ("p cnf 2 2\n1 -2 0\n2 0\n", True),    # SAT
    ("p cnf 2 2\n1 0\n-1 0\n", False),      # UNSAT
    ("p cnf 3 3\n1 2 0\n-1 3 0\n-2 -3 0\n", True), # SAT
]

def write_temp_dimacs(content):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.cnf') as f:
        f.write(content)
        return f.name

@pytest.mark.parametrize("dimacs_str, expected", examples)
def test_dpll_solver_no_heuristic(dimacs_str, expected):
    path = write_temp_dimacs(dimacs_str)
    num_vars, clauses = parse_dimacs(path)
    graph = ImplicationGraph()
    result, dlis_count, vsids_count, _ = dpll(clauses, {}, graph, heuristic=None)
    assert (result is not None) == expected
    os.remove(path)

@pytest.mark.parametrize("dimacs_str, expected", examples)
def test_dpll_solver_vsids(dimacs_str, expected):
    path = write_temp_dimacs(dimacs_str)
    num_vars, clauses = parse_dimacs(path)
    graph = ImplicationGraph()
    result, dlis_count, vsids_count, _ = dpll(clauses, {}, graph, heuristic='vsids', activity={})
    assert (result is not None) == expected
    assert vsids_count > 0 or not expected
    os.remove(path)

@pytest.mark.parametrize("dimacs_str, expected", examples)
def test_dpll_solver_dlis(dimacs_str, expected):
    path = write_temp_dimacs(dimacs_str)
    num_vars, clauses = parse_dimacs(path)
    graph = ImplicationGraph()
    result, dlis_count, vsids_count, _ = dpll(clauses, {}, graph, heuristic='dlis')
    assert (result is not None) == expected
    assert dlis_count > 0 or not expected
    os.remove(path)

@pytest.mark.parametrize("dimacs_str, expected", examples)
def test_dpll_solver_lookahead(dimacs_str, expected):
    path = write_temp_dimacs(dimacs_str)
    num_vars, clauses = parse_dimacs(path)
    graph = ImplicationGraph()
    result, dlis_count, vsids_count, _ = dpll(clauses, {}, graph, heuristic='lookahead')
    assert (result is not None) == expected
    os.remove(path)



