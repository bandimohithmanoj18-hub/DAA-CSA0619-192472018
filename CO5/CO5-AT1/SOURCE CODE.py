def get_candidates(grid, row, col)
    used = set(grid[row])
    used.update(grid[r][col] for r in range(9))

    start_row = (row  3)  3
    start_col = (col  3)  3

    for r in range(start_row, start_row + 3)
        for c in range(start_col, start_col + 3)
            used.add(grid[r][c])

    return set(range(1, 10)) - used


def find_empty(grid)
    best = None

    for r in range(9)
        for c in range(9)
            if grid[r][c] == 0
                candidates = get_candidates(grid, r, c)

                if not candidates
                    return r, c, set()

                if best is None or len(candidates)  len(best[2])
                    best = (r, c, candidates)

    return best


def solve(grid)
    cell = find_empty(grid)

    if cell is None
        return True

    row, col, candidates = cell

    if not candidates
        return False

    for value in sorted(candidates)
        grid[row][col] = value

        if solve(grid)
            return True

        grid[row][col] = 0

    return False


def is_valid_initial_grid(grid)
    if len(grid) != 9 or any(len(row) != 9 for row in grid)
        return False

    for row in grid
        if any(value  0 or value  9 for value in row)
            return False

    for i in range(9)
        row_values = [v for v in grid[i] if v != 0]
        if len(row_values) != len(set(row_values))
            return False

        col_values = [grid[r][i] for r in range(9) if grid[r][i] != 0]
        if len(col_values) != len(set(col_values))
            return False

    for br in range(0, 9, 3)
        for bc in range(0, 9, 3)
            values = []
            for r in range(br, br + 3)
                for c in range(bc, bc + 3)
                    if grid[r][c] != 0
                        values.append(grid[r][c])

            if len(values) != len(set(values))
                return False

    return True


def print_grid(grid)
    for row in grid
        print( .join(map(str, row)))


print(Enter the 9 rows. Use 0 for empty cells.)
grid = []

for _ in range(9)
    grid.append(list(map(int, input().split())))

if not is_valid_initial_grid(grid)
    print(Invalid Sudoku input.)
elif solve(grid)
    print(nSolved Sudoku)
    print_grid(grid)
else
    print(No solution exists for the given Sudoku.)
