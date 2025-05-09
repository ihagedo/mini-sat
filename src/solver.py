import random
import sys
import logging
from src.utils import bcp, unit_propagation, pure_literal, get_counter
from copy import deepcopy

def is_satisfied(clause, assignment):
    for lit in clause:
        val = assignment.get(abs(lit))
        if val is not None and ((lit > 0 and val) or (lit < 0 and not val)):
            return True
    return False

def backtracking(formula, assignment, heuristic, watch_list=None):
    formula, pure_assignment = pure_literal(formula)
    assignment += pure_assignment
    formula, unit_assignment = unit_propagation(formula, watch_list)
    assignment += unit_assignment
    if formula == -1:
        return []

    if all(is_satisfied(clause, {abs(l): l > 0 for l in assignment}) for clause in formula):
        return assignment

    variable = heuristic(formula)
    for val in [variable, -variable]:
        solution = backtracking(bcp(formula, val, watch_list), assignment + [val], heuristic, deepcopy(watch_list))
        if solution:
            return solution
    return []

def heuristics_arbiter(name):
    return {
        'BASE': base_heuristic_orig,
        'BASE2': base_heuristic_better,
        'DLIS': dlis,
        'VSIDS': vsids,
        'LA': look_ahead,
    }.get(name.upper(), base_heuristic_orig)


def base_heuristic_orig(formula):
    weighted = get_counter(formula, mode='weighted')
    differential = get_counter(formula, mode='diff')
    max_weight = max(weighted.values())
    candidates = [lit for lit, w in weighted.items() if w == max_weight]
    if len(candidates) == 1:
        return candidates[0]

    max_differential = max(differential.get(abs(lit), 0) for lit in candidates)
    rand_candidates = [lit for lit in candidates if differential.get(abs(lit), 0) == max_differential]
    return random.choice(rand_candidates)

def base_heuristic_better(formula):
    counter = {}
    for clause in formula:
        weight = 2 ** -len(clause)
        for lit in clause:
            counter[lit] = counter.get(lit, 0) + weight
    return max(counter, key=counter.get)

dlis_improvements = []

def dlis(formula):
    logger = logging.getLogger("sat")
    global dlis_improvements
    counter = get_counter(formula)
    chosen = max(counter, key=counter.get)
    improvement = counter[chosen]
    dlis_improvements.append(improvement)
    logger.debug(f"[DLIS] Chose literal {chosen} with score {improvement}")
    return chosen

vsids_scores = {}
vsids_improvements = []

def vsids(formula):
    logger = logging.getLogger("sat")
    global vsids_scores
    counter = get_counter(formula)
    for literal, count in counter.items():
        vsids_scores[literal] = vsids_scores.get(literal, 0) + count
    for literal in vsids_scores:
        vsids_scores[literal] *= 0.95
    chosen = max(vsids_scores, key=vsids_scores.get)
    improvement = vsids_scores[chosen]
    vsids_improvements.append(improvement)
    logger.debug(f"[VSIDS] Chose literal {chosen} with score {improvement:.4f}")
    return chosen

lookahead_scores = []

def look_ahead(formula):
    logger = logging.getLogger("sat")
    scores = {}
    for clause in formula:
        for lit in clause:
            try_pos = bcp(formula, lit)
            try_neg = bcp(formula, -lit)
            if try_pos == -1 and try_neg == -1:
                score = float('-inf')
            elif try_pos == -1 or try_neg == -1:
                score = float('inf')
            else:
                score = -len(try_pos) - len(try_neg)
            scores[lit] = score
    chosen = max(scores, key=scores.get)
    lookahead_scores.append(scores[chosen])
    logger.debug(f"[LA] Chose literal {chosen} with score {scores[chosen]}")
    return chosen