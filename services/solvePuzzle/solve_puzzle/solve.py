import json
from solve_puzzle import validate


def handler(event, context):
    # TODO Add checks to validate that was a json object and was a sudoku puzzle
    unsolved_puzzle_form_data = json.dumps(event, indent=2)

    try:
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

        solved_puzzle = solve_puzzle(puzzle_object)

        data = {
            'output': 'Puzzle successfully solved.',
            'puzzle_rows': solved_puzzle
        }

        return {'statusCode': 200,
                'body': json.dumps(data),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}
    except Exception as e:
        print(e)
        return {'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
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
    row1_col1 = puzzle[0][0]
    print("DEBUG: Row 1, col 1: " + str(row1_col1))

    puzzle[0][0] = 1

    print("DEBUG: Solved puzzle: " + json.dumps(puzzle))

    return puzzle
