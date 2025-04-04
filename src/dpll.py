def dpll(clauses, assignment):
    if not clauses:
        return assignment
    if any([clause == [] for clause in clauses]):
        return None

    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    while unit_clauses:
        lit = unit_clauses[0]
        assignment[abs(lit)] = lit > 0
        clauses = simplify(clauses, lit)
        if any([clause == [] for clause in clauses]):
            return None
        unit_clauses = [c[0] for c in clauses if len(c) == 1]

    for clause in clauses:
        for lit in clause:
            break
        break

    for value in [True, False]:
        chosen_lit = lit if value else -lit
        assignment[abs(chosen_lit)] = value
        new_clauses = simplify(clauses, chosen_lit)
        result = dpll(new_clauses, assignment.copy(), graph)
        if result is not None:
            return result

    return None

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
