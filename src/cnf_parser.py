def parse_dimacs(file_path):
    clauses = []
    num_vars = 0
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('c'):
                continue
            if line.startswith('p'):
                parts = line.split()
                num_vars = int(parts[2])
            else:
                clause = list(map(int, line.strip().split()))
                if clause[-1] == 0:
                    clause.pop()
                clauses.append(clause)
    return num_vars, clauses
