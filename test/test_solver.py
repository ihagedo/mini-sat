import os
import tempfile
import subprocess
import pytest

from src.cnf_parser import parse_dimacs
from src.dpll import dpll

# Example CNF formulas and expected outcomes
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
def test_dpll_solver(dimacs_str, expected):
    path = write_temp_dimacs(dimacs_str)
    num_vars, clauses = parse_dimacs(path)
    result = dpll(clauses, {})
    if expected:
        assert result is not None, "Expected SAT but got UNSAT"
    else:
        assert result is None, "Expected UNSAT but got SAT"
    os.remove(path)
