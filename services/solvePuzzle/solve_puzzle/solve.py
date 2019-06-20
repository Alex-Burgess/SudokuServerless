import json
from solve_puzzle import validate


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
    # row1_col1 = puzzle[0][0]
    # print("DEBUG: Row 1, col 1: " + str(row1_col1))

    # Start - for each cell, elimate numbers that it can't be by row, column and cell
    # If left with only one number, then update the puzzle.

    value = 4
    update_cell[puzzle, 0, 0, value]
    print("DEBUG: puzzle updated: " + json.dumps(puzzle))

    # if puzzle solved:
    #     return {'puzzle': puzzle, 'status': True }

    # Puzzle not solved
    return {'puzzle': puzzle, 'status': False}


def update_cell(puzzle, row, col, value):
    puzzle[row][col] = value
    print("DEBUG: Updated row (" + str(row) + "), col (" + str(col) + ") with value (" + str(value) + ").")
    return puzzle
