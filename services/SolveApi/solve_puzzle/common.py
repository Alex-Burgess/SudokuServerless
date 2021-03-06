# A collection of methods that help interact with the puzzle
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.handlers:
    handler = logger.handlers[0]
    handler.setFormatter(logging.Formatter("[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(module)s:%(funcName)s\t%(message)s\n", "%Y-%m-%dT%H:%M:%S"))


def get_puzzle_from_event(event):
    try:
        body = event['body']
        logger.info("Event body: " + json.dumps(body))
    except Exception:
        logger.error("API Event was empty.")
        raise Exception('API Event was empty.')

    try:
        body_data = json.loads(body)
    except Exception:
        logger.error("API Event did not contain a valid body.")
        raise Exception('API Event did not contain a valid body.')

    try:
        puzzle = body_data['puzzle_rows']
        logger.info("Unsolved puzzle object: " + json.dumps(puzzle))
    except Exception:
        logger.error("API Event did not contain a valid puzzle.")
        raise Exception('API Event did not contain a valid puzzle.')

    return puzzle


def get_row(puzzle, row_num):
    return puzzle[row_num]


def get_column(puzzle, col_num):
    column = []
    for r in range(0, 9):
        cell_value = puzzle[r][col_num]
        column.append(cell_value)

    logger.debug("Column number ({}) being returned ()".format(col_num, column))

    return column


def get_grid_number(puzzle, row_num, col_num):
    grid_num = 0
    if row_num < 3:
        if col_num < 3:
            grid_num = 0
        elif col_num < 6:
            grid_num = 1
        else:
            grid_num = 2
    elif row_num < 6:
        if col_num < 3:
            grid_num = 3
        elif col_num < 6:
            grid_num = 4
        else:
            grid_num = 5
    else:
        if col_num < 3:
            grid_num = 6
        elif col_num < 6:
            grid_num = 7
        else:
            grid_num = 8

    return grid_num


def get_grid(puzzle, grid_num):
    grid_coordinates = grid_top_left_cell_number(grid_num)

    first_row = grid_coordinates[0]
    last_row = first_row + 3
    first_col = grid_coordinates[1]
    last_col = first_col + 3

    grid = []

    for r in range(first_row, last_row):
        for c in range(first_col, last_col):
            grid.append(puzzle[r][c])

    logger.debug("Grid number ({}) being returned ()".format(grid_num, grid))

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
    return coordinates


def cell_contains_number(puzzle, row_num, col_num):
    cell_value = puzzle[row_num][col_num]
    if cell_value > 0:
        return True

    return False


def get_row_numbers_from_grid(puzzle, grid_num):
    grid_coordinates = grid_top_left_cell_number(grid_num)

    rows = [
        grid_coordinates[0],
        grid_coordinates[0] + 1,
        grid_coordinates[0] + 2
    ]

    return rows


def get_col_numbers_from_grid(puzzle, grid_num):
    grid_coordinates = grid_top_left_cell_number(grid_num)

    cols = [
        grid_coordinates[1],
        grid_coordinates[1] + 1,
        grid_coordinates[1] + 2
    ]

    return cols


def get_row_number_from_grid(puzzle, grid_num, cel_num):
    grid_coordinates = grid_top_left_cell_number(grid_num)

    row_num = 0
    if cel_num < 3:
        row_num = grid_coordinates[0]
    elif cel_num < 6:
        row_num = grid_coordinates[0] + 1
    else:
        row_num = grid_coordinates[0] + 2

    return row_num


def get_col_number_from_grid(puzzle, grid_num, cel_num):
    grid_coordinates = grid_top_left_cell_number(grid_num)

    col_num = 0

    if (cel_num == 0) or (cel_num == 3) or (cel_num == 6):
        col_num = grid_coordinates[1]
    elif (cel_num == 1) or (cel_num == 4) or (cel_num == 7):
        col_num = grid_coordinates[1] + 1
    else:
        col_num = grid_coordinates[1] + 2

    return col_num


def get_empty_cell_refs(num_list):
    cel_refs = []

    for x in range(0, 9):
        if num_list[x] == 0:
            cel_refs.append(x)

    return cel_refs
