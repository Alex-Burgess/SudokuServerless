from solve_puzzle import common


def validate_puzzle(puzzle):
    print("INFO: Validating puzzle (" + str(puzzle) + ")")

    for r in range(0, 9):
        row = puzzle[r]
        if not validate_row_col_grid(row, "row"):
            return False

    for c in range(0, 9):
        column = common.get_column(puzzle, c)
        if not validate_row_col_grid(column, "column"):
            return False

    for g in range(0, 9):
        grid = common.get_grid(puzzle, g)
        if not validate_row_col_grid(grid, "grid"):
            return False

    return True


def validata_data_types(puzzle):
    for r in range(0, 9):
        row = puzzle[r]
        for x in row:
            if not isinstance(x, int):
                return False
    return True


def validate_row_col_grid(number_list, type):
    print("\nINFO: Validating " + type + " (" + str(number_list) + ")")
    max_cell_value_occurences = 1
    for x in range(1, 10):
        if number_list.count(x) > max_cell_value_occurences:
            print("ERROR: Number (" + str(x) + ") occurred more than once in row (" + str(number_list) + ")")
            return False

    print("INFO: No duplicates found in " + type + " (" + str(number_list) + ")")
    return True
