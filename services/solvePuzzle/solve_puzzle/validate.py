def validate_puzzle(puzzle):
    # print("INFO: Validating puzzle (" + str(puzzle) + ")")

    for r in range(0, 9):
        row = puzzle[r]
        if not validate_row_col_grid(row):
            return False

    for c in range(0, 9):
        column = get_column(c, puzzle)
        if not validate_row_col_grid(column):
            return False

    for g in range(0, 9):
        grid = get_grid(g, puzzle)
        if not validate_row_col_grid(grid):
            return False

    return True


def validate_row_col_grid(row):
    # print("\nINFO: Validating row (" + str(row) + ")")
    max_cell_value_occurences = 1
    for x in range(1, 10):
        if row.count(x) > max_cell_value_occurences:
            print("ERROR: Number (" + str(x) + ") occurred more than once in row (" + str(row) + ")")
            return False

    # print("INFO: No duplicates found in row (" + str(row) + ")")
    return True


def get_grid(grid_num, puzzle):
    grid_coordinates = grid_top_left_cell_number(grid_num)

    first_row = grid_coordinates[0]
    last_row = first_row + 3
    first_col = grid_coordinates[1]
    last_col = first_col + 3

    grid = []

    for r in range(first_row, last_row):
        for c in range(first_col, last_col):
            grid.append(puzzle[r][c])

    # print("Grid number (" + str(grid_num) + ") values are: " + str(grid))

    return grid


def grid_top_left_cell_number(number):
    grids = {
        0: [0, 0],
        1: [0, 3],
        2: [0, 6],
        3: [3, 0],
        4: [3, 3],
        5: [3, 6],
        6: [6, 0],
        7: [6, 3],
        8: [6, 6]
    }

    coordinates = grids[number]
    # print("Grid number (" + str(number) + ") coordinates: " + str(coordinates))
    return coordinates


def get_column(col_num, puzzle):
    column = []
    for r in range(0, 9):
        cell_value = puzzle[r][col_num]
        column.append(cell_value)

    # print("INFO: Column number (" + str(col_num) + ") being returned (" + str(column) + ")")

    return column
