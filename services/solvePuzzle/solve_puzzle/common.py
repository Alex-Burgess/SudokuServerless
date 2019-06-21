# A collection of methods that help interact with the puzzle
import json


def get_puzzle_object(unsolved_puzzle_form_data):
    # print("DEBUG: form data: " + unsolved_puzzle_form_data)

    data = json.loads(unsolved_puzzle_form_data)
    body = data['body']
    # print("DEBUG: Body data: " + body)

    body_data = json.loads(body)
    puzzle = body_data['puzzle_rows']

    print("DEBUG: Unsolved puzzle object: " + json.dumps(puzzle))
    return puzzle


def get_row(puzzle, row_num):
    # print("INFO: Row number (" + str(row_num) + ") being returned (" + str(puzzle[row_num]) + ")")
    return puzzle[row_num]


def get_column(puzzle, col_num):
    column = []
    for r in range(0, 9):
        cell_value = puzzle[r][col_num]
        column.append(cell_value)

    # print("INFO: Column number (" + str(col_num) + ") being returned (" + str(column) + ")")

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


def cell_contains_number(puzzle, row_num, col_num):
    cell_value = puzzle[row_num][col_num]
    if cell_value > 0:
        # print("Cell of row (" + str(row_num) + ") and col (" + str(col_num) + ") contains a value (" + str(cell_value) + ")")
        return True

    # print("Cell of row (" + str(row_num) + ") and col (" + str(col_num) + ") does not contain a value (" + str(cell_value) + ")")
    return False
