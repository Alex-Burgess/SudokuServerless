import json
import copy
from solve_puzzle import common
from solve_puzzle import brute_force
from solve_puzzle import validate
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.handlers:
    handler = logger.handlers[0]
    handler.setFormatter(logging.Formatter("[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(module)s:%(funcName)s\t%(message)s\n", "%Y-%m-%dT%H:%M:%S"))


def handler(event, context):
    response = solve_main(event)
    return response


def solve_main(event):
    try:
        puzzle_object = common.get_puzzle_from_event(event)
    except Exception as e:
        logger.error("Exception: {}".format(e))
        response = create_response(500, json.dumps({'error': str(e)}))
        return response

    if not validate.validata_data_types(puzzle_object):
        logger.error('Puzzle was not validated due to wrong data types')
        response = create_response(500, json.dumps({'error': 'Puzzle was not validated due to wrong data types.'}))
        return response

    if not validate.validate_puzzle(puzzle_object):
        logger.error('Puzzle was not validated due to invalid row, column or grid.')
        response = create_response(500, json.dumps({'error': 'Puzzle was not validated due to invalid row, column or grid.'}))
        return response

    solved_result = solve_puzzle(puzzle_object)

    if solved_result['status']:
        data = {'status': 'Solved', 'message': 'Puzzle successfully solved.', 'puzzle_rows': solved_result['puzzle']}
    else:
        data = {'status': 'Unsolved', 'message': 'Puzzle could not be solved.', 'puzzle_rows': solved_result['puzzle']}

    response = create_response(200, json.dumps(data))
    return response


def solve_puzzle(puzzle):
    logger.info("Attempting to solve using methods 1, 2, 3 and 4")
    attempt = solve_with_methods_1_to_4(puzzle)
    if (attempt['status']):
        return {'puzzle': attempt['puzzle'], 'status': True}
    else:
        puzzle = attempt['puzzle']

    # Method 5 - Find pairs
    logger.info("Attempting to solve using method 5")
    for type in ["rows", "cols", "grids"]:
        method5_result = solve_with_method_5(puzzle, type)
        if (method5_result['status']):
            return {'puzzle': method5_result['puzzle'], 'status': True}

    # Method 6 - brute force
    logger.info("Attempting to solve using brute force.")
    bf_result = brute_force.solve_wrapper(puzzle)
    logger.info("Brute force result ({})".format(bf_result))
    if (bf_result['status']):
        return {'puzzle': bf_result['puzzle'], 'status': True}

    logger.info("Puzzle could not be solved by any method.  Puzzle ({})".format(puzzle))
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

        logger.info("Finished Loop ({}), puzzle update: ({})".format(loop, puzzle))

        if puzzle_complete(puzzle):
            return {'puzzle': puzzle, 'status': True}

    return {'puzzle': puzzle, 'status': False}


# Method 5 - Find pairs
def solve_with_method_5(puzzle, type):
    pairs = find_pairs_by_type(puzzle, type)

    if type == 'rows':
        remaining_type_list = list(pairs['rows'].keys())
    elif type == 'cols':
        remaining_type_list = list(pairs['cols'].keys())
    else:
        remaining_type_list = list(pairs['grids'].keys())

    for x in remaining_type_list:
        if type == 'rows':
            type_list = common.get_row(puzzle, x)
        elif type == 'cols':
            type_list = common.get_column(puzzle, x)
        else:
            type_list = common.get_grid(puzzle, x)

        empty_cell_pair = common.get_empty_cell_refs(type_list)
        possible_values = pairs[type][x]
        logger.debug("{} {} ({}) has a missing value pair ({})".format(type, x, type_list, possible_values))

        for value in possible_values:
            puzzle_copy = copy.deepcopy(puzzle)
            cell_ref = empty_cell_pair[0]

            if type == 'rows':
                r = x
                c = cell_ref
            elif type == 'cols':
                r = cell_ref
                c = x
            else:
                r = common.get_row_number_from_grid(puzzle, x, cell_ref)
                c = common.get_col_number_from_grid(puzzle, x, cell_ref)

            logger.info("Attempting to solve puzzle again by updating Row {}, Col {} with value {}".format(r, c, value))
            puzzle_attempt = update_cell(puzzle_copy, r, c, value)
            puzzle_attempt = solve_with_methods_1_to_4(puzzle_attempt)
            if (puzzle_attempt['status']):
                return {'puzzle': puzzle_attempt['puzzle'], 'status': True}

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
    remaining_values = elimate_list_values([1, 2, 3, 4, 5, 6, 7, 8, 9], row)
    logger.debug("Row ({}) has remaining values ({})".format(row_num, remaining_values))

    for test_val in remaining_values:
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
                continue

            # Test if a cell can be eliminated, due to grid match.
            grid_num = common.get_grid_number(puzzle, row_num, cell)
            grid = common.get_grid(puzzle, grid_num)
            if test_val in grid:
                unsolved_cell_list.remove(cell)
                continue

        if len(unsolved_cell_list) == 1:
            logger.debug("Eliminated all cells in row {} ({}) for value ({}) to reference ({})".format(row_num, row, test_val, unsolved_cell_list))
            puzzle = update_cell(puzzle, row_num, unsolved_cell_list[0], test_val)
        else:
            logger.debug("All cells in row {} ({}) could not be eliminated for value ({}). Remaining cell references ({})".format(
                row_num, row, test_val, unsolved_cell_list))

    return puzzle


def col_elimination(puzzle, col_num):
    col = common.get_column(puzzle, col_num)
    remaining_values = elimate_list_values([1, 2, 3, 4, 5, 6, 7, 8, 9], col)

    for test_val in remaining_values:
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
                continue

            # Test if a cell can be eliminated, due to grid match.
            grid_num = common.get_grid_number(puzzle, cell, col_num)
            grid = common.get_grid(puzzle, grid_num)
            if test_val in grid:
                unsolved_cell_list.remove(cell)
                continue

        if len(unsolved_cell_list) == 1:
            logger.debug("Eliminated all cells in Col {} ({}) for value ({}) to reference ({})".format(col_num, col, test_val, unsolved_cell_list))
            puzzle = update_cell(puzzle, unsolved_cell_list[0], col_num, test_val)
        else:
            logger.debug("All cells in Col {} ({}) could not be eliminated for value ({}). Remaining cell references ({})".format(
                col_num, col, test_val, unsolved_cell_list))

    return puzzle


def grid_elimination(puzzle, grid_num):
    grid = common.get_grid(puzzle, grid_num)
    remaining_values = elimate_list_values([1, 2, 3, 4, 5, 6, 7, 8, 9], grid)

    for test_val in remaining_values:
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
                continue

            # Test if cell can be eliminated, due to a col match.
            col_num = common.get_col_number_from_grid(puzzle, grid_num, cell)
            col = common.get_column(puzzle, col_num)
            if test_val in col:
                unsolved_cell_list.remove(cell)
                continue

        if len(unsolved_cell_list) == 1:
            logger.debug("Eliminated all cells in grid {} ({}) for value ({}) to reference ({})".format(grid_num, grid, test_val, unsolved_cell_list[0]))
            row_num = common.get_row_number_from_grid(puzzle, grid_num, unsolved_cell_list[0])
            col_num = common.get_col_number_from_grid(puzzle, grid_num, unsolved_cell_list[0])
            puzzle = update_cell(puzzle, row_num, col_num, test_val)
        else:
            logger.debug("All cells in row {} ({}) could not be eliminated for value ({}). Remaining cell references ({})".format(
                grid_num, grid, test_val, unsolved_cell_list))

    return puzzle


def puzzle_complete(puzzle):
    if row_col_grid_complete(puzzle, "rows"):
        if row_col_grid_complete(puzzle, "cols"):
            if row_col_grid_complete(puzzle, "grids"):
                logger.info("Puzzle complete")
                return True

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
    logger.info("Updated row ({}), col ({}), with value ({})".format(row, col, value))
    return puzzle


def elimate_list_values(possible_vals, number_list):
    for val in number_list:
        if possible_vals.count(val) > 0:
            possible_vals.remove(val)
            logger.debug("Eliminated value ({}), List of cell possibilities now ({})".format(val, possible_vals))

    return possible_vals


def find_pairs_by_type(puzzle, type):
    pairs = {'rows': {}, 'cols': {}, 'grids': {}}

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
            logger.debug("{} ({}) had 2 cells remaining ({})".format(type, type_list, remaining_pair))
            pairs[type][num] = remaining_pair

    logger.info("Pairs : {}".format(json.dumps(pairs)))

    return pairs


def create_response(code, message):
    logger.info("Creating response with status code ({}) and message ({})".format(code, message))
    response = {'statusCode': code,
                'body': message,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}
    logger.info("Returning response: {}".format(response))
    return response
