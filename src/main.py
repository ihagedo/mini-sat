import sys
from cnf_parser import parse_dimacs
from dpll import dpll

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_dimacs_file>")
        return

    file_path = sys.argv[1]
    num_vars, clauses = parse_dimacs(file_path)
    assignment = {}

    result = dpll(clauses, assignment)

    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print("Assignment:", result)

if __name__ == '__main__':
    main()
