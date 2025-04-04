import sys
from src.cnf_parser import parse_dimacs
from src.dpll import dpll
from src.implication_graph import ImplicationGraph

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_dimacs_file>")
        return

    file_path = sys.argv[1]
    num_vars, clauses = parse_dimacs(file_path)
    assignment = {}
    graph = ImplicationGraph()

    result = dpll(clauses, assignment, graph)

    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print("Assignment:", result)

    graph.visualize()

if __name__ == '__main__':
    main()
