def run_solver(file_path, heuristic='dlis', switch_after=10, decay_factor=0.95, benchmark=False):
    """Run the DPLL solver from a Python console with specified options."""
    from src.cnf_parser import parse_dimacs
    from src.dpll import dpll, dpll_norm
    from src.implication_graph import ImplicationGraph
    import csv, os
    from datetime import datetime

    num_vars, clauses = parse_dimacs(file_path)
    assignment = {}
    graph = ImplicationGraph()

    actual_heuristic = heuristic if heuristic != 'none' else None

    if heuristic == 'auto':
        result, dlis_count, vsids_count, vsids_improvement = dpll(
            clauses, assignment, graph,
            heuristic='dlis',
            activity=None,
            switch_after=switch_after,
            decay_factor=decay_factor
        )
    elif heuristic == 'none':
        result = dpll_norm(clauses, assignment, graph,)
    else:
        activity = {} if heuristic == 'vsids' else None
        result, dlis_count, vsids_count, vsids_improvement = dpll(
            clauses, assignment, graph,
            heuristic=actual_heuristic,
            activity=activity,
            switch_after=switch_after,
            decay_factor=decay_factor
        )

    status = "SATISFIABLE" if result else "UNSATISFIABLE"
    print(f"{status} Heuristic: {heuristic}")
    if result:
        print("Assignment (first 10 vars):", dict(list(result.items())[:10]))

    if benchmark:
        output_file = "benchmark_results.csv"
        file_exists = os.path.isfile(output_file)
        with open(output_file, mode="a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["timestamp", "file", "heuristic", "status", "dlis_count", "vsids_count", "vsids_improvement", "switch_after", "decay_factor"])
            writer.writerow([
                datetime.now().isoformat(),
                os.path.basename(file_path),
                heuristic,
                status,
                dlis_count,
                vsids_count,
                f"{vsids_improvement:.2f}",
                switch_after,
                decay_factor
            ])
    return result

import argparse
import csv
import os
from datetime import datetime
from src.cnf_parser import parse_dimacs
from src.dpll import dpll
from src.implication_graph import ImplicationGraph

def main():
    parser = argparse.ArgumentParser(description="DPLL SAT Solver with Heuristics")
    parser.add_argument("file", help="Path to DIMACS CNF file")
    parser.add_argument("--heuristic", choices=["dlis", "vsids", "lookahead", "none", "auto"], default="dlis", help="Heuristic to use")
    parser.add_argument("--switch_after", type=int, default=10, help="Depth after which to switch from DLIS to VSIDS in auto mode")
    parser.add_argument("--decay_factor", type=float, default=0.95, help="Decay factor for VSIDS activity")
    parser.add_argument("--benchmark", action="store_true", help="Output results to CSV benchmark file")

    args = parser.parse_args()

    num_vars, clauses = parse_dimacs(args.file)
    assignment = {}
    graph = ImplicationGraph()

    heuristic = args.heuristic if args.heuristic != "none" else None

    if args.heuristic == "auto":
        result, dlis_count, vsids_count, vsids_improvement = dpll(
            clauses, assignment, graph,
            heuristic="dlis",
            activity=None,
            switch_after=args.switch_after,
            decay_factor=args.decay_factor
        )
    else:
        activity = {} if args.heuristic == "vsids" else None
        result, dlis_count, vsids_count, vsids_improvement = dpll(
            clauses, assignment, graph,
            heuristic=heuristic,
            activity=activity,
            decay_factor=args.decay_factor,
            switch_after=args.switch_after
        )

    status = "SATISFIABLE" if result is not None else "UNSATISFIABLE"
    print(status)
    if result is not None:
        print("Assignment:", result)

    graph.visualize()

    if args.benchmark:
        output_file = "benchmark_results.csv"
        file_exists = os.path.isfile(output_file)
        with open(output_file, mode="a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["timestamp", "file", "heuristic", "status", "dlis_count", "vsids_count", "vsids_improvement", "switch_after", "decay_factor"])
            writer.writerow([
                datetime.now().isoformat(),
                os.path.basename(args.file),
                args.heuristic,
                status,
                dlis_count,
                vsids_count,
                f"{vsids_improvement:.2f}",
                args.switch_after,
                args.decay_factor
            ])

if __name__ == '__main__':
    main()