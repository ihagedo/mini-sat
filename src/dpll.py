from src.implication_graph import ImplicationGraph
import random
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

dlis_count = 0
vsids_count = 0
vsids_improvement = 0.0
max_depth_reached = 0

def dpll(clauses, assignment, graph, heuristic='dlis', activity=None, decay_factor=0.95, switch_after=10, depth=0):
    global dlis_count, vsids_count, vsids_improvement, max_depth_reached

    max_depth_reached = max(max_depth_reached, depth)

    if not clauses:
        logging.info(f"SAT solved with {dlis_count} DLIS decisions and {vsids_count} VSIDS decisions.")
        logging.info(f"Cumulative VSIDS improvement score: {vsids_improvement:.2f}")
        logging.info(f"Max recursion depth reached: {max_depth_reached}")
        return assignment, dlis_count, vsids_count, vsids_improvement
    if any([clause == [] for clause in clauses]):
        return None, dlis_count, vsids_count, vsids_improvement

    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    while unit_clauses:
        lit = unit_clauses[0]
        assignment[abs(lit)] = lit > 0
        clauses = simplify(clauses, lit)
        graph.add_implication(f"{lit}", f"assign {lit}")
        if any([clause == [] for clause in clauses]):
            return None, dlis_count, vsids_count, vsids_improvement
        unit_clauses = [c[0] for c in clauses if len(c) == 1]

    if heuristic == 'dlis' and depth >= switch_after:
        logging.info(f"Switching heuristic from DLIS to VSIDS at depth {depth}")
        graph.add_implication(f"depth {depth}", "Switch DLIS→VSIDS")
        heuristic = 'vsids'
        if activity is None:
            activity = {}

    lit = select_literal(clauses, assignment, heuristic, activity)

    for value in [True, False]:
        chosen_lit = lit if value else -lit
        assignment[abs(chosen_lit)] = value
        graph.add_implication(f"branch {lit}", f"assign {chosen_lit}")
        new_clauses = simplify(clauses, chosen_lit)

        if heuristic == 'vsids':
            var = abs(chosen_lit)
            prev_score = activity.get(var, 1.0)
            activity[var] = prev_score + 1
            for v in activity:
                activity[v] *= decay_factor
            improvement = activity[var] - prev_score
            vsids_improvement += improvement
            vsids_count += 1
            logging.info(f"VSIDS chose var {var}, improvement: {improvement:.2f}, total activity: {activity[var]:.2f}")

        elif heuristic == 'dlis':
            dlis_count += 1
            logging.info(f"DLIS chose literal {lit} at depth {depth}")

        result, _, _, _ = dpll(new_clauses, assignment.copy(), graph, heuristic, activity, decay_factor, switch_after, depth + 1)
        if result is not None:
            return result, dlis_count, vsids_count, vsids_improvement

    return None, dlis_count, vsids_count, vsids_improvement

def simplify(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        if -literal in clause:
            new_clause = [l for l in clause if l != -literal]
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

def select_literal(clauses, assignment, heuristic, activity):
    unassigned = set(abs(lit) for clause in clauses for lit in clause if abs(lit) not in assignment)

    if heuristic == 'vsids':
        return max(unassigned, key=lambda x: activity.get(x, 1.0))

    elif heuristic == 'dlis':
        score = {}
        for clause in clauses:
            for lit in clause:
                if abs(lit) not in assignment:
                    score[lit] = score.get(lit, 0) + 1
        return max(score, key=score.get)

    elif heuristic == 'lookahead':
        best_literal = None
        best_reduction = -1
        for lit in unassigned:
            for val in [lit, -lit]:
                reduced = len(simplify(clauses, val))
                reduction = len(clauses) - reduced
                if reduction > best_reduction:
                    best_literal = val
                    best_reduction = reduction
        logging.info(f"Look-ahead selected literal {best_literal} with reduction {best_reduction}")
        return abs(best_literal)

    else:
        return next(iter(unassigned))
