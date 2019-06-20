import json
from solve_puzzle import validate
from solve_puzzle import common


def handler(event, context):
    # TODO Add checks to validate that was a json object and was a sudoku puzzle
    try:
        unsolved_puzzle_form_data = json.dumps(event, indent=2)
    except Exception as e:
        print(e)
        return {'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}

    puzzle_object = get_puzzle_object(unsolved_puzzle_form_data)

    data_result = validate.validata_data_types(puzzle_object)

    if not data_result:
        return {'statusCode': 500,
                'body': 'Puzzle was not validated due to wrong data types',
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}

    val_result = validate.validate_puzzle(puzzle_object)

    if not val_result:
        return {'statusCode': 500,
                'body': 'Puzzle was not validated due to invalid row, column or grid.',
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}

    solved_result = solve_puzzle(puzzle_object)

    if solved_result['status']:
        data = {
            'status': 'Solved',
            'message': 'Puzzle successfully solved.',
            'puzzle_rows': solved_result['puzzle']
        }

        return {'statusCode': 200,
                'body': json.dumps(data),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}
    else:
        data = {
            'status': 'Unsolved',
            'message': 'Puzzle could not be solved.',
            'puzzle_rows': solved_result['puzzle']
        }

        return {'statusCode': 200,
                'body': json.dumps(data),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}


def get_puzzle_object(unsolved_puzzle_form_data):
    # print("DEBUG: form data: " + unsolved_puzzle_form_data)

    data = json.loads(unsolved_puzzle_form_data)
    body = data['body']
    # print("DEBUG: Body data: " + body)

    body_data = json.loads(body)
    puzzle = body_data['puzzle_rows']

    print("DEBUG: Unsolved puzzle object: " + json.dumps(puzzle))
    return puzzle


def solve_puzzle(puzzle):
    # Start - for each cell, elimate numbers that it can't be by row, column and cell
    # If left with only one number, then update the puzzle.
    for loop in range(0, 10):
        for r in range(0, 9):
            for c in range(0, 9):
                cell_contains_value = common.cell_contains_number(puzzle, r, c)
                if not cell_contains_value:
                    result = eliminate_cell_values(puzzle, r, c)

                    if result['status']:
                        puzzle = update_cell(puzzle, r, c, result['values'][0])

        print("DEBUG: Loop (" + str(loop) + "), puzzle update: " + json.dumps(puzzle))

        if puzzle_complete(puzzle):
            return {'puzzle': puzzle, 'status': True}

    # Puzzle not solved
    return {'puzzle': puzzle, 'status': False}


def puzzle_complete(puzzle):
    if row_col_grid_complete(puzzle, "rows"):
        if row_col_grid_complete(puzzle, "cols"):
            if row_col_grid_complete(puzzle, "grids"):
                print("DEBUG: Puzzle complete")
                return True

    print("DEBUG: Puzzle not complete")
    return False


def row_col_grid_complete(puzzle, type):
    test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(0, 9):
        type_list = []
        if type == "rows":
            type_list = common.get_row(puzzle, i)
        elif type == "cols":
            type_list = common.get_column(puzzle, i)
        elif type == "grids":
            type_list = common.get_grid(puzzle, i)
        else:
            # if type not row, col or grid, throw exception.
            print("ERROR....")

        if not set(type_list) == set(test_list):
            print("DEBUG: " + type + " (" + str(i) + ") with values (" + str(type_list) + ") is not complete.")
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
    print("DEBUG: Updated row (" + str(row) + "), col (" + str(col) + ") with value (" + str(value) + ").")
    return puzzle


def elimate_list_values(possible_vals, number_list):
    for val in number_list:
        if possible_vals.count(val) > 0:
            possible_vals.remove(val)
            # print("DEBUG: Elimated value (" + str(val) + ").  List of cell possibilities now (" + str(possible_vals) + ")")

    return possible_vals
