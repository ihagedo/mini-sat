import sys
from cnf_parser import parse_dimacs

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_dimacs_file>")
        return

    file_path = sys.argv[1]
    num_vars, clauses = parse_dimacs(file_path)

if __name__ == '__main__':
    main()
