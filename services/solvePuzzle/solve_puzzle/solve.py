import json
import copy
from solve_puzzle import common
from solve_puzzle import brute_force


def solve_puzzle(puzzle):
    attempt = solve_with_methods_1_to_4(puzzle)
    if (attempt['status']):
        return {'puzzle': attempt['puzzle'], 'status': True}
    else:
        puzzle = attempt['puzzle']

    # Method 5 - Find pairs
    method5_result = solve_with_method_5(puzzle)
    if (method5_result['status']):
        return {'puzzle': method5_result['puzzle'], 'status': True}

    # Method 6 - brute force
    bf_result = brute_force.solve_wrapper(puzzle)
    print("DEBUG: Brute force result ({})".format(bf_result))
    if (bf_result['status']):
        return {'puzzle': bf_result['puzzle'], 'status': True}

    return {'puzzle': puzzle, 'status': False}


def solve_with_methods_1_to_4(puzzle):
    for loop in range(0, 5):
        # Method 1 - Cell Elimination
        for r in range(0, 9):
            for c in range(0, 9):
                puzzle = cell_elimination(puzzle, r, c)

        # Method 2, 3 & 4 - Row Col, Grid elimination
        for r in range(0, 9):
            puzzle = row_elimination(puzzle, r)

        for c in range(0, 9):
            puzzle = col_elimination(puzzle, c)

        for g in range(0, 9):
            puzzle = grid_elimination(puzzle, g)

        print("INFO: Finished Loop (" + str(loop) + "), puzzle update: " + json.dumps(puzzle))

        if puzzle_complete(puzzle):
            return {'puzzle': puzzle, 'status': True}

    return {'puzzle': puzzle, 'status': False}


def solve_with_method_5(puzzle):
    # Method 5 - Find pairs
    pairs = find_pairs_by_row_col_grid(puzzle)

    # Rows
    rows_with_pairs = list(pairs['rows'].keys())   # list of rows with empty pairs

    for row_num in rows_with_pairs:
        row = common.get_row(puzzle, row_num)
        empty_cell_pair = common.get_empty_row_col_grid_cell_refs(row)

        cell_num = empty_cell_pair[0]
        possible_values = pairs['rows'][row_num]
        print("DEBUG: Row {} ({}) has a missing value pair ({})".format(row_num, row, possible_values))
        print("DEBUG: Remaining empty cell references for row {} ({}) are ({})".format(row_num, row, empty_cell_pair))

        for value in possible_values:
            puzzle_copy = copy.deepcopy(puzzle)
            print("INFO: Attempting to solve puzzle again by updating Row {}, Col {} with value {}".format(row_num, cell_num, value))
            puzzle_attempt = update_cell(puzzle_copy, row_num, cell_num, value)
            puzzle_attempt = solve_with_methods_1_to_4(puzzle_attempt)
            if (puzzle_attempt['status']):
                return {'puzzle': puzzle_attempt['puzzle'], 'status': True}

    # Cols
    # cols_with_pairs = list(pairs['rows'].keys())   # list of rows with empty pairs
    #
    # for row_num in rows_with_pairs:
    #     row = common.get_row(puzzle, row_num)
    #     empty_cell_pair = common.get_empty_row_col_grid_cell_refs(row)
    #
    #     cell_num = empty_cell_pair[0]
    #     possible_values = pairs['rows'][row_num]
    #     print("DEBUG: Row {} ({}) has a missing value pair ({})".format(row_num, row, possible_values))
    #     print("DEBUG: Remaining empty cell references for row {} ({}) are ({})".format(row_num, row, empty_cell_pair))
    #
    #     for value in possible_values:
    #         puzzle_copy = copy.deepcopy(puzzle)
    #         print("INFO: Attempting to solve puzzle again by updating Row {}, Col {} with value {}".format(row_num, cell_num, value))
    #         puzzle_attempt = update_cell(puzzle_copy, row_num, cell_num, value)
    #         puzzle_attempt = solve_with_methods_1_to_4(puzzle_attempt)
    #         if (puzzle_attempt['status']):
    #             return {'puzzle': puzzle_attempt['puzzle'], 'status': True}

    # list of grids

    return {'puzzle': puzzle, 'status': False}


def cell_elimination(puzzle, row_num, col_num):
    cell_contains_value = common.cell_contains_number(puzzle, row_num, col_num)
    if not cell_contains_value:
        result = eliminate_cell_values(puzzle, row_num, col_num)

        if result['status']:
            puzzle = update_cell(puzzle, row_num, col_num, result['values'][0])

    return puzzle


def row_elimination(puzzle, row_num):
    row = common.get_row(puzzle, row_num)

    # Determine remaining values to solve in row.
    value_test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    remaining_values = elimate_list_values(value_test_list, row)
    # print("DEBUG: Row (" + str(row_num) + ") has remaining values (" + str(remaining_values) + ")")

    for test_val in remaining_values:
        # print("DEBUG: Checking if all but one of the cells in row ({}) can be elimindated for value ({}).".format(row_num, test_val))
        unsolved_cell_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]    # When one value remains, cell is solved.

        for cell in range(0, 9):
            # Test if cell can be eliminated, as already contains value
            if row[cell] > 0:
                unsolved_cell_list.remove(cell)
                continue

            # Test if cell can be eliminated, due to a column match.
            col = common.get_column(puzzle, cell)
            if test_val in col:
                unsolved_cell_list.remove(cell)
                # print("DEBUG: Removed cell ({},{}) as Col ({}) contains val ({}).".format(row_num, cell, col, test_val))
                continue

            # Test if a cell can be eliminated, due to grid match.
            grid_num = common.get_grid_number(puzzle, row_num, cell)
            grid = common.get_grid(puzzle, grid_num)
            if test_val in grid:
                unsolved_cell_list.remove(cell)
                # print("DEBUG: Removed cell ({},{}) as Grid ({}) contains val ({}).".format(row_num, cell, grid, test_val))
                continue

        if len(unsolved_cell_list) == 1:
            # print("INFO: Eliminated all cells in row {} ({}) for value ({}) to reference ({})".format(row_num, row, test_val, unsolved_cell_list))
            puzzle = update_cell(puzzle, row_num, unsolved_cell_list[0], test_val)
        # else:
        #     print("DEBUG: All cells in row {} ({}) could not be eliminated for value ({}). Remaining cell references ({})".format(
        #         row_num, row, test_val, unsolved_cell_list))

    return puzzle


def col_elimination(puzzle, col_num):
    col = common.get_column(puzzle, col_num)

    # Determine remaining values to solve in list.
    value_test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    remaining_values = elimate_list_values(value_test_list, col)
    # print("DEBUG: {} ({}) has remaining values ({})".format(type, col, remaining_values))

    for test_val in remaining_values:
        # print("DEBUG: Checking if all but one of the cells in Col ({}) can be elimindated for value ({}).".format(col_num, test_val))
        unsolved_cell_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]    # When one value remains, cell is solved.

        for cell in range(0, 9):
            # Test if cell can be eliminated, as already contains value
            if col[cell] > 0:
                unsolved_cell_list.remove(cell)
                continue

            # Test if cell can be eliminated, due to a row match.
            row = common.get_row(puzzle, cell)
            if test_val in row:
                unsolved_cell_list.remove(cell)
                # print("DEBUG: Removed cell ({},{}) as Row ({}) contains val ({}).".format(cell, col_num, row, test_val))
                continue

            # Test if a cell can be eliminated, due to grid match.
            grid_num = common.get_grid_number(puzzle, cell, col_num)
            grid = common.get_grid(puzzle, grid_num)
            if test_val in grid:
                unsolved_cell_list.remove(cell)
                # print("DEBUG: Removed cell ({},{}) as Grid ({}) contains val ({}).".format(cell, col_num, grid, test_val))
                continue

        if len(unsolved_cell_list) == 1:
            # print("INFO: Eliminated all cells in Col {} ({}) for value ({}) to reference ({})".format(col_num, col, test_val, unsolved_cell_list))
            puzzle = update_cell(puzzle, unsolved_cell_list[0], col_num, test_val)
        # else:
        #     print("DEBUG: All cells in Col {} ({}) could not be eliminated for value ({}). Remaining cell references ({})".format(
        #         col_num, col, test_val, unsolved_cell_list))

    return puzzle


def grid_elimination(puzzle, grid_num):
    grid = common.get_grid(puzzle, grid_num)

    # Determine remaining values to solve in row.
    value_test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    remaining_values = elimate_list_values(value_test_list, grid)
    # print("DEBUG: Grid (" + str(grid_num) + ") has remaining values (" + str(remaining_values) + ")")

    for test_val in remaining_values:
        # print("DEBUG: Checking if all but one of the cells in grid ({}) can be elimindated for value ({}).".format(grid_num, test_val))
        unsolved_cell_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]       # When one value remains, cell is solved.

        for cell in range(0, 9):
            # Test if cell can be eliminated, as already contains value
            if grid[cell] > 0:
                unsolved_cell_list.remove(cell)
                continue

            # Test if cell can be eliminated, due to a row match.
            row_num = common.get_row_number_from_grid(puzzle, grid_num, cell)
            row = common.get_row(puzzle, row_num)
            if test_val in row:
                unsolved_cell_list.remove(cell)
                # print("DEBUG: Removed grid cell reference ({}) as Row ({}) contains val ({}).".format(cell, row, test_val))
                continue

            # Test if cell can be eliminated, due to a col match.
            col_num = common.get_col_number_from_grid(puzzle, grid_num, cell)
            col = common.get_column(puzzle, col_num)
            if test_val in col:
                unsolved_cell_list.remove(cell)
                # print("DEBUG: Removed grid cell reference ({}) as Col ({}) contains val ({}).".format(cell, col, test_val))
                continue

        if len(unsolved_cell_list) == 1:
            # print("INFO: Eliminated all cells in grid {} ({}) for value ({}) to reference ({})".format(grid_num, grid, test_val, unsolved_cell_list[0]))
            row_num = common.get_row_number_from_grid(puzzle, grid_num, unsolved_cell_list[0])
            col_num = common.get_col_number_from_grid(puzzle, grid_num, unsolved_cell_list[0])
            puzzle = update_cell(puzzle, row_num, col_num, test_val)
        # else:
        #     print("DEBUG: All cells in row {} ({}) could not be eliminated for value ({}). Remaining cell references ({})".format(
        #         grid_num, grid, test_val, unsolved_cell_list))

    return puzzle


def puzzle_complete(puzzle):
    if row_col_grid_complete(puzzle, "rows"):
        if row_col_grid_complete(puzzle, "cols"):
            if row_col_grid_complete(puzzle, "grids"):
                print("INFO: Puzzle complete")
                return True

    # print("DEBUG: Puzzle not complete")
    return False


def row_col_grid_complete(puzzle, type):
    for i in range(0, 9):
        type_list = []
        if type == "rows":
            type_list = common.get_row(puzzle, i)
        elif type == "cols":
            type_list = common.get_column(puzzle, i)
        else:
            type_list = common.get_grid(puzzle, i)

        if not set(type_list) == set([1, 2, 3, 4, 5, 6, 7, 8, 9]):
            # print("DEBUG: " + type + " (" + str(i) + ") with values (" + str(type_list) + ") is not complete.")
            return False

    return True


def eliminate_cell_values(puzzle, row_num, col_num):
    remaining_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    row = common.get_row(puzzle, row_num)
    remaining_values = elimate_list_values(remaining_values, row)

    col = common.get_column(puzzle, col_num)
    remaining_values = elimate_list_values(remaining_values, col)

    grid_num = common.get_grid_number(puzzle, row_num, col_num)
    grid = common.get_grid(puzzle, grid_num)
    remaining_values = elimate_list_values(remaining_values, grid)

    if len(remaining_values) == 1:
        return {'values': remaining_values, 'status': True}

    return {'values': remaining_values, 'status': False}


def update_cell(puzzle, row, col, value):
    puzzle[row][col] = value
    print("INFO: Updated row (" + str(row) + "), col (" + str(col) + ") with value (" + str(value) + ").")
    return puzzle


def elimate_list_values(possible_vals, number_list):
    for val in number_list:
        if possible_vals.count(val) > 0:
            possible_vals.remove(val)
            # print("DEBUG: Elimated value (" + str(val) + ").  List of cell possibilities now (" + str(possible_vals) + ")")

    return possible_vals


def find_pairs_by_row_col_grid(puzzle):
    pairs = {'rows': {}, 'cols': {}, 'grids': {}}

    for type in ["rows", "cols", "grids"]:
        for num in range(0, 9):
            type_list = []
            if type == "rows":
                type_list = common.get_row(puzzle, num)
            elif type == "cols":
                type_list = common.get_column(puzzle, num)
            else:
                type_list = common.get_grid(puzzle, num)

            if type_list.count(0) == 2:
                remaining_pair = elimate_list_values([1, 2, 3, 4, 5, 6, 7, 8, 9], type_list)
                print("DEBUG: {} ({}) had 2 cells remaining ({})".format(type, type_list, remaining_pair))
                pairs[type][num] = remaining_pair

    print("INFO: Pairs : {}".format(json.dumps(pairs)))

    return pairs
