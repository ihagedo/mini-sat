def parse_dimacs(filepath):
    clauses = []
    num_vars = 0
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c') or line.startswith('%') or line.startswith('0'):
                continue
            if line.startswith('p'):
                parts = line.split()
                num_vars = int(parts[2])
                continue
            clause = list(map(int, line.split()))
            if clause and clause[-1] == 0:
                clause.pop()
            if clause:
                clauses.append(clause)
    return clauses, num_vars