import json
from solve_puzzle import common
from solve_puzzle import validate
from solve_puzzle import solve


def handler(event, context):
    # TODO Add checks to validate that was a json object and was a sudoku puzzle
    print("DEBUG: Incomming event: {}".format(event))

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

    puzzle_object = common.get_puzzle_object(unsolved_puzzle_form_data)

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

    solved_result = solve.solve_puzzle(puzzle_object)

    if solved_result['status']:
        print("INFO: Puzzle was solved, returning solved puzzle.  Puzzle ({})".format(solved_result['puzzle']))
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
        print("INFO: Puzzle could not be solved by any method, returning unsolved puzzle.  Puzzle ({})".format(solved_result['puzzle']))
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
