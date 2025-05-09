import logging
from collections import defaultdict

def get_counter(formula, mode='plain', weight=2):
    counter = {}
    for clause in formula:
        for literal in clause:
            if mode == 'diff':
                base = abs(literal)
                counter[base] = counter.get(base, 0) + (1 if literal > 0 else -1)
            elif mode == 'weighted':
                counter[literal] = counter.get(literal, 0) + weight ** -len(clause)
            else:
                counter[literal] = counter.get(literal, 0) + 1
    return counter

def bcp(formula, unit, watch_list=None):
    if watch_list is None:
        return _basic_bcp(formula, unit)

    new_formula = []
    for clause in formula:
        if clause in watch_list.get(-unit, []):
            if unit in clause:
                new_formula.append(clause)
                continue
            found_new_watch = False
            for lit in clause:
                if lit != -unit and lit != unit:
                    watch_list[lit].append(clause)
                    found_new_watch = True
                    break
            if not found_new_watch:
                reduced = [lit for lit in clause if lit != -unit]
                if not reduced:
                    return -1
                new_formula.append(reduced)
        else:
            new_formula.append(clause)
    return new_formula


def _basic_bcp(formula, unit):
    new_formula = []
    for clause in formula:
        if unit in clause:
            continue
        if -unit in clause:
            reduced = [lit for lit in clause if lit != -unit]
            if not reduced:
                return -1
            new_formula.append(reduced)
        else:
            new_formula.append(clause)
    return new_formula

def _update_watch_list(watch_list, old_clause, new_clause):
    for lit in set(old_clause):
        watch_list[lit].remove(old_clause)
    for lit in set(new_clause[:2]):
        watch_list[lit].append(new_clause)

def init_watch_list(formula):
    watch_list = defaultdict(list)
    for clause in formula:
        for lit in clause[:2]:
            watch_list[lit].append(clause)
    return watch_list

def pure_literal(formula):
    logger = logging.getLogger("sat")
    counter = get_counter(formula)
    pures = [lit for lit in counter if -lit not in counter]
    for pure in pures:
        formula = bcp(formula, pure)
        if formula == -1:
            logger.debug("[prune] Contradiction found in pure literal assignment")
            return -1, []
    return formula, pures

def unit_propagation(formula, watch_list=None):
    logger = logging.getLogger("sat")
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0][0]
        formula = bcp(formula, unit, watch_list)
        if formula == -1:
            logger.debug("[prune] Contradiction found in literal assignment")
            return -1, []
        assignment.append(unit)
        if not formula:
            break
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment