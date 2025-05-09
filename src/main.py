import sys
import argparse
import logging
import time
import csv
import os
from src.cnf_parser import parse_dimacs
from src.solver import backtracking, heuristics_arbiter, dlis_improvements, vsids_improvements, lookahead_scores
from src.utils import init_watch_list

def main():
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger("sat")
    parser = argparse.ArgumentParser(
        description="DPLL SAT Solver",
        formatter_class=argparse.RawTextHelpFormatter,
        allow_abbrev=False
    )
    parser.add_argument(
        "cnf_file",
        help="Path to CNF file in DIMACS format",
        nargs="?",
        default=None
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose debug logging"
    )
    parser.add_argument(
        "--heuristic",
        default="BASE",
        help="""
    Branching heuristic to use. Options:
      BASE   : Combined max weight and max differentials
      BASE2  : Better not best
      DLIS   : Dynamic Largest Individual Sum
      VSIDS  : Variable State Independent Decaying Sum
      LA     : Look-Ahead
    """)
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Enable profiling to time the solver execution"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Enable benchmarking of execution statistics"
    )

    args = parser.parse_args()

    if not args.cnf_file:
        parser.print_help()
        sys.exit(1)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    heuristic = heuristics_arbiter(args.heuristic)
    clauses, n_vars = parse_dimacs(args.cnf_file)
    watch_list = init_watch_list(clauses)

    start_time = time.time()
    solution = backtracking(clauses, [], heuristic)
    end_time = time.time()
    duration = end_time - start_time

    result = "SAT" if solution else "UNSAT"

    if solution:
        assignment_dict = {abs(x): int(x > 0) for x in solution}
        for var in range(1, n_vars + 1):
            if var not in assignment_dict:
                assignment_dict[var] = 0
        print("RESULT:SAT")
        print('ASSIGNMENT:' + ' '.join(f"{var}={val}" for var, val in sorted(assignment_dict.items())))
    else:
        print("RESULT:UNSAT")

    # Log benchmark results
    output_file = "benchmark_results.csv"
    file_exists = os.path.isfile(output_file)
    heuristic_name = args.heuristic.upper()
    cnf_name = args.cnf_file
    improvements = {
        'DLIS': sum(dlis_improvements),
        'VSIDS': sum(vsids_improvements),
        'LA': sum(lookahead_scores),
        'BASE': 0,
        'BASE2': 0
    }

    if args.benchmark:
        with open(output_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "benchmark", "heuristic", "result", "time", "improvement"])
            from datetime import datetime
            timestamp = datetime.now().isoformat()
            writer.writerow([timestamp, cnf_name, heuristic_name, result, f"{duration:.6f}", improvements.get(heuristic_name, 0)])


if __name__ == '__main__':
    main()
