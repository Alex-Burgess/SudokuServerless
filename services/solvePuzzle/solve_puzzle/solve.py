import json


def handler(event, context):
    # TODO Add checks to validate that was a json object and was a sudoku puzzle
    unsolved_puzzle_form_data = json.dumps(event, indent=2)

    puzzle_object = get_puzzle_object(unsolved_puzzle_form_data)

    solved_puzzle = solve_puzzle(puzzle_object)

    data = {
        'output': 'Puzzle successfully solved.',
        'Solved Puzzle': solved_puzzle
    }

    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}


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
