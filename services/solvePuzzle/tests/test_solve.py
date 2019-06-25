import pytest
from solve_puzzle import solve


# Fixtures
# Classes

def test_solve_puzzle1():
    puzzle = [
        [0, 8, 0, 0, 6, 4, 7, 0, 3],
        [7, 2, 0, 5, 0, 3, 6, 9, 8],
        [0, 0, 0, 0, 0, 2, 4, 1, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 9],
        [0, 9, 6, 3, 0, 8, 1, 5, 0],
        [8, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 4, 2, 8, 0, 0, 0, 0, 0],
        [9, 7, 8, 6, 0, 5, 0, 4, 1],
        [6, 0, 5, 4, 7, 0, 0, 8, 0]
    ]

    puzzle_result = [
        [5, 8, 1, 9, 6, 4, 7, 2, 3],
        [7, 2, 4, 5, 1, 3, 6, 9, 8],
        [3, 6, 9, 7, 8, 2, 4, 1, 5],
        [4, 1, 3, 2, 5, 7, 8, 6, 9],
        [2, 9, 6, 3, 4, 8, 1, 5, 7],
        [8, 5, 7, 1, 9, 6, 2, 3, 4],
        [1, 4, 2, 8, 3, 9, 5, 7, 6],
        [9, 7, 8, 6, 2, 5, 3, 4, 1],
        [6, 3, 5, 4, 7, 1, 9, 8, 2]
    ]
    result = solve.solve_puzzle(puzzle)
    assert result['status'], "Puzzle should be solved."
    assert result['puzzle'] == puzzle_result, "Solution should match solution provided."


def test_solve_puzzle5():
    puzzle = [
        [4, 5, 0, 0, 0, 0, 3, 0, 0],
        [1, 0, 0, 9, 0, 7, 4, 0, 0],
        [0, 7, 0, 0, 5, 0, 0, 1, 6],
        [0, 0, 0, 0, 0, 0, 5, 0, 3],
        [0, 8, 0, 0, 0, 0, 0, 2, 0],
        [7, 0, 6, 0, 0, 0, 0, 0, 0],
        [6, 1, 0, 0, 2, 0, 0, 3, 0],
        [0, 0, 2, 6, 0, 5, 0, 0, 9],
        [0, 0, 4, 0, 0, 0, 0, 6, 1]
    ]

    puzzle_result = [
         [4, 5, 9, 1, 6, 2, 3, 8, 7],
         [1, 6, 8, 9, 3, 7, 4, 5, 2],
         [2, 7, 3, 8, 5, 4, 9, 1, 6],
         [9, 4, 1, 2, 8, 6, 5, 7, 3],
         [3, 8, 5, 7, 9, 1, 6, 2, 4],
         [7, 2, 6, 5, 4, 3, 1, 9, 8],
         [6, 1, 7, 4, 2, 9, 8, 3, 5],
         [8, 3, 2, 6, 1, 5, 7, 4, 9],
         [5, 9, 4, 3, 7, 8, 2, 6, 1]
    ]
    result = solve.solve_puzzle(puzzle)
    assert result['status'], "Puzzle should be solved."
    assert result['puzzle'] == puzzle_result, "Solution should match solution provided."


def test_solve_puzzle7():
    puzzle = [
        [0, 0, 6, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 4, 3, 5, 0, 0, 0],
        [9, 0, 4, 0, 0, 0, 0, 0, 2],
        [0, 7, 0, 5, 4, 0, 0, 0, 0],
        [3, 6, 0, 0, 0, 0, 0, 8, 4],
        [0, 0, 0, 0, 8, 2, 0, 3, 0],
        [7, 0, 0, 0, 0, 0, 8, 0, 1],
        [0, 0, 0, 8, 7, 4, 0, 0, 9],
        [0, 4, 0, 0, 0, 0, 3, 0, 0]
    ]

    puzzle_result = [
        [5, 8, 6, 2, 9, 7, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 9, 6, 8],
        [9, 3, 4, 1, 6, 8, 5, 7, 2],
        [8, 7, 2, 5, 4, 3, 1, 9, 6],
        [3, 6, 5, 7, 1, 9, 2, 8, 4],
        [4, 9, 1, 6, 8, 2, 7, 3, 5],
        [7, 5, 9, 3, 2, 6, 8, 4, 1],
        [2, 1, 3, 8, 7, 4, 6, 5, 9],
        [6, 4, 8, 9, 5, 1, 3, 2, 7]
    ]

    result = solve.solve_puzzle(puzzle)
    assert result['status'], "Puzzle should be solved."
    assert result['puzzle'] == puzzle_result, "Solution should match solution provided."


def test_solve_puzzle_hardest():
    puzzle = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]

    puzzle_result = [
        [8, 1, 2, 7, 5, 3, 6, 4, 9],
        [9, 4, 3, 6, 8, 2, 1, 7, 5],
        [6, 7, 5, 4, 9, 1, 2, 8, 3],
        [1, 5, 4, 2, 3, 7, 8, 9, 6],
        [3, 6, 9, 8, 4, 5, 7, 2, 1],
        [2, 8, 7, 1, 6, 9, 5, 3, 4],
        [5, 2, 1, 9, 7, 4, 3, 6, 8],
        [4, 3, 8, 5, 2, 6, 9, 1, 7],
        [7, 9, 6, 3, 1, 8, 4, 5, 2]
    ]

    result = solve.solve_puzzle(puzzle)
    assert result['status'], "Puzzle should be solved."
    assert result['puzzle'] == puzzle_result, "Solution should match solution provided."


def test_solve_with_method_5_rows():
    puzzle = [
        [5, 8, 6, 0, 0, 0, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 0, 0, 8],
        [9, 3, 4, 1, 6, 8, 0, 0, 2],
        [0, 7, 0, 5, 4, 3, 0, 0, 6],
        [3, 6, 0, 0, 0, 0, 0, 8, 4],
        [4, 0, 0, 6, 8, 2, 0, 3, 0],
        [7, 0, 0, 3, 0, 6, 8, 4, 1],
        [0, 1, 3, 8, 7, 4, 0, 0, 9],
        [0, 4, 0, 0, 0, 0, 3, 0, 0]
    ]

    puzzle_result = [
        [5, 8, 6, 2, 9, 7, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 9, 6, 8],
        [9, 3, 4, 1, 6, 8, 5, 7, 2],
        [8, 7, 2, 5, 4, 3, 1, 9, 6],
        [3, 6, 5, 7, 1, 9, 2, 8, 4],
        [4, 9, 1, 6, 8, 2, 7, 3, 5],
        [7, 5, 9, 3, 2, 6, 8, 4, 1],
        [2, 1, 3, 8, 7, 4, 6, 5, 9],
        [6, 4, 8, 9, 5, 1, 3, 2, 7]
    ]

    result = solve.solve_with_method_5(puzzle, 'rows')
    assert result['status'], "Puzzle should be solved."
    assert result['puzzle'] == puzzle_result, "Solution should match solution provided."


def test_solve_with_method_5_cols():
    puzzle = [
        [5, 8, 6, 0, 0, 0, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 0, 0, 8],
        [9, 3, 4, 1, 6, 8, 0, 0, 2],
        [0, 7, 0, 5, 4, 3, 0, 0, 6],
        [3, 6, 0, 0, 0, 0, 0, 8, 4],
        [4, 0, 0, 6, 8, 2, 0, 3, 0],
        [7, 0, 0, 3, 0, 6, 8, 4, 1],
        [0, 1, 3, 8, 7, 4, 0, 0, 9],
        [0, 4, 0, 0, 0, 0, 3, 0, 0]
    ]

    puzzle_result = [
        [5, 8, 6, 2, 9, 7, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 9, 6, 8],
        [9, 3, 4, 1, 6, 8, 5, 7, 2],
        [8, 7, 2, 5, 4, 3, 1, 9, 6],
        [3, 6, 5, 7, 1, 9, 2, 8, 4],
        [4, 9, 1, 6, 8, 2, 7, 3, 5],
        [7, 5, 9, 3, 2, 6, 8, 4, 1],
        [2, 1, 3, 8, 7, 4, 6, 5, 9],
        [6, 4, 8, 9, 5, 1, 3, 2, 7]
    ]

    result = solve.solve_with_method_5(puzzle, 'cols')
    assert result['status'], "Puzzle should be solved."
    assert result['puzzle'] == puzzle_result, "Solution should match solution provided."


def test_solve_with_method_5_grids():
    puzzle = [
        [5, 8, 6, 0, 0, 0, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 0, 0, 8],
        [9, 3, 4, 1, 6, 8, 0, 0, 2],
        [0, 7, 0, 5, 4, 3, 0, 0, 6],
        [3, 6, 0, 0, 0, 0, 0, 8, 4],
        [4, 0, 0, 6, 8, 2, 0, 3, 0],
        [7, 0, 0, 3, 0, 6, 8, 4, 1],
        [0, 1, 3, 8, 7, 4, 6, 0, 9],
        [0, 4, 0, 0, 0, 0, 3, 2, 0]
    ]

    puzzle_result = [
        [5, 8, 6, 2, 9, 7, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 9, 6, 8],
        [9, 3, 4, 1, 6, 8, 5, 7, 2],
        [8, 7, 2, 5, 4, 3, 1, 9, 6],
        [3, 6, 5, 7, 1, 9, 2, 8, 4],
        [4, 9, 1, 6, 8, 2, 7, 3, 5],
        [7, 5, 9, 3, 2, 6, 8, 4, 1],
        [2, 1, 3, 8, 7, 4, 6, 5, 9],
        [6, 4, 8, 9, 5, 1, 3, 2, 7]
    ]

    result = solve.solve_with_method_5(puzzle, 'grids')
    assert result['status'], "Puzzle should be solved."
    assert result['puzzle'] == puzzle_result, "Solution should match solution provided."


def test_update_cell():
    puzzle = [
        [0, 0, 0, 0, 1, 0, 2, 9, 0],
        [9, 7, 0, 0, 0, 8, 0, 6, 0],
        [3, 0, 1, 0, 0, 4, 0, 0, 8],
        [2, 4, 3, 9, 6, 0, 5, 0, 1],
        [0, 1, 6, 0, 0, 0, 9, 3, 0],
        [5, 0, 8, 0, 3, 1, 6, 7, 2],
        [8, 0, 0, 5, 0, 0, 0, 0, 6],
        [0, 2, 0, 3, 0, 0, 0, 4, 9],
        [0, 6, 9, 0, 8, 0, 0, 0, 0]
    ]

    updated_puzzle = [
        [4, 0, 0, 0, 1, 0, 2, 9, 0],
        [9, 7, 0, 0, 0, 8, 0, 6, 0],
        [3, 0, 1, 0, 0, 4, 0, 0, 8],
        [2, 4, 3, 9, 6, 0, 5, 0, 1],
        [0, 1, 6, 0, 0, 0, 9, 3, 0],
        [5, 0, 8, 0, 3, 1, 6, 7, 2],
        [8, 0, 0, 5, 0, 0, 0, 0, 6],
        [0, 2, 0, 3, 0, 0, 0, 4, 9],
        [0, 6, 9, 0, 8, 0, 0, 0, 0]
    ]
    puzzle_result = solve.update_cell(puzzle, 0, 0, 4)
    assert puzzle_result == updated_puzzle, "Cell was not updated."


def test_eliminate_row_values():
    remaining_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    row = [0, 2, 3, 4, 5, 6, 7, 8, 9]
    result = solve.elimate_list_values(remaining_values, row)
    assert result == [1], "All values except the number 1 should have been eliminated."

    remaining_values2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    row = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    result = solve.elimate_list_values(remaining_values2, row)
    assert result == [9], "All values except the number 9 should have been eliminated."

    remaining_values3 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    row = [1, 2, 3, 4, 5, 6, 7, 0, 0]
    result = solve.elimate_list_values(remaining_values3, row)
    assert result == [8, 9], "All values except the numbers 8 & 9 should have been eliminated."


def test_eliminate_cell_values():
    puzzle = [
        [0, 0, 0, 0, 1, 0, 2, 9, 0],
        [9, 7, 0, 0, 0, 8, 0, 6, 0],
        [3, 0, 1, 0, 0, 4, 0, 0, 8],
        [2, 4, 3, 9, 6, 0, 5, 0, 1],
        [0, 1, 6, 0, 0, 0, 9, 3, 0],
        [5, 0, 8, 0, 3, 1, 6, 7, 2],
        [8, 0, 0, 5, 0, 0, 0, 0, 6],
        [0, 2, 0, 3, 0, 0, 0, 4, 9],
        [0, 6, 9, 0, 8, 0, 0, 0, 0]
    ]

    result = solve.eliminate_cell_values(puzzle, 3, 5)
    assert result['status'], "Cell should be solved as row 3 and col 5 eliminate all values except 7."
    assert result['values'] == [7], "Value for cell should be 7."

    result = solve.eliminate_cell_values(puzzle, 4, 8)
    assert result['values'] == [4], "Value for cell should be 4."

    result = solve.eliminate_cell_values(puzzle, 0, 0)
    assert not result['status'], "Cell is not solved as row 0 and col 0 leave a number of values."
    assert result['values'] == [4, 6], "List of values for cell should be [4, 6]."

    result = solve.eliminate_cell_values(puzzle, 8, 8)
    assert not result['status'], "Cell is not solved as row 8 and col 8 leave a number of values."
    assert result['values'] == [3, 5, 7], "List of values for cell should be [3, 5, 7]."


def test_row_col_grid_complete():
    puzzle = [
        [0, 8, 0, 0, 6, 4, 7, 0, 3],
        [7, 2, 0, 5, 0, 3, 6, 9, 8],
        [0, 0, 0, 0, 0, 2, 4, 1, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 9],
        [0, 9, 6, 3, 0, 8, 1, 5, 0],
        [8, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 4, 2, 8, 0, 0, 0, 0, 0],
        [9, 7, 8, 6, 0, 5, 0, 4, 1],
        [6, 0, 5, 4, 7, 0, 0, 8, 0]
    ]

    result = solve.row_col_grid_complete(puzzle, "rows")
    assert not result, "Rows should not be complete."

    result = solve.row_col_grid_complete(puzzle, "cols")
    assert not result, "Cols should not be complete."

    result = solve.row_col_grid_complete(puzzle, "grids")
    assert not result, "Grids should not be complete."

    puzzle_result = [
        [5, 8, 1, 9, 6, 4, 7, 2, 3],
        [7, 2, 4, 5, 1, 3, 6, 9, 8],
        [3, 6, 9, 7, 8, 2, 4, 1, 5],
        [4, 1, 3, 2, 5, 7, 8, 6, 9],
        [2, 9, 6, 3, 4, 8, 1, 5, 7],
        [8, 5, 7, 1, 9, 6, 2, 3, 4],
        [1, 4, 2, 8, 3, 9, 5, 7, 6],
        [9, 7, 8, 6, 2, 5, 3, 4, 1],
        [6, 3, 5, 4, 7, 1, 9, 8, 2]
    ]

    result = solve.row_col_grid_complete(puzzle_result, "rows")
    assert result, "Rows should be complete."

    result = solve.row_col_grid_complete(puzzle_result, "cols")
    assert result, "Cols should be complete."

    result = solve.row_col_grid_complete(puzzle_result, "grids")
    assert result, "Grids should be complete."


def puzzle_complete():
    puzzle = [
        [0, 8, 0, 0, 6, 4, 7, 0, 3],
        [7, 2, 0, 5, 0, 3, 6, 9, 8],
        [0, 0, 0, 0, 0, 2, 4, 1, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 9],
        [0, 9, 6, 3, 0, 8, 1, 5, 0],
        [8, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 4, 2, 8, 0, 0, 0, 0, 0],
        [9, 7, 8, 6, 0, 5, 0, 4, 1],
        [6, 0, 5, 4, 7, 0, 0, 8, 0]
    ]

    result = solve.puzzle_complete(puzzle)
    assert not result, "Puzzle should not be complete."

    puzzle_result = [
        [5, 8, 1, 9, 6, 4, 7, 2, 3],
        [7, 2, 4, 5, 1, 3, 6, 9, 8],
        [3, 6, 9, 7, 8, 2, 4, 1, 5],
        [4, 1, 3, 2, 5, 7, 8, 6, 9],
        [2, 9, 6, 3, 4, 8, 1, 5, 7],
        [8, 5, 7, 1, 9, 6, 2, 3, 4],
        [1, 4, 2, 8, 3, 9, 5, 7, 6],
        [9, 7, 8, 6, 2, 5, 3, 4, 1],
        [6, 3, 5, 4, 7, 1, 9, 8, 2]
    ]

    result = solve.puzzle_complete(puzzle_result)
    assert result, "Puzzle should be complete."


def test_row_elimination():
    puzzle = [
        [0, 0, 0, 0, 5, 6, 0, 0, 0],
        [0, 1, 9, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 7, 2, 3],
        [0, 0, 5, 0, 6, 0, 0, 3, 7],
        [2, 0, 0, 7, 0, 5, 0, 0, 4],
        [8, 7, 0, 0, 2, 0, 6, 0, 0],
        [1, 2, 7, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 8, 6, 0],
        [0, 0, 0, 1, 3, 0, 0, 0, 0]
    ]

    puzzle_result = [
        [0, 0, 0, 0, 5, 6, 0, 0, 0],
        [0, 1, 9, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 7, 2, 3],
        [0, 0, 5, 0, 6, 0, 2, 3, 7],
        [2, 0, 0, 7, 0, 5, 0, 0, 4],
        [8, 7, 0, 0, 2, 0, 6, 0, 0],
        [1, 2, 7, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 8, 6, 0],
        [0, 0, 0, 1, 3, 0, 0, 0, 0]
    ]

    result = solve.row_elimination(puzzle, 3)
    assert result == puzzle_result, "Row should be solved"


def test_col_elimination():
    puzzle = [
        [0, 0, 0, 0, 5, 6, 0, 0, 0],
        [0, 1, 9, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 7, 2, 3],
        [0, 0, 5, 0, 6, 0, 0, 3, 7],
        [2, 0, 0, 7, 0, 5, 0, 0, 4],
        [8, 7, 0, 0, 2, 0, 6, 0, 0],
        [1, 2, 7, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 8, 6, 0],
        [0, 0, 0, 1, 3, 0, 0, 0, 0]
    ]

    puzzle_result = [
        [0, 0, 0, 0, 5, 6, 0, 0, 0],
        [0, 1, 9, 0, 0, 0, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 7, 2, 3],
        [0, 0, 5, 0, 6, 0, 0, 3, 7],
        [2, 0, 0, 7, 0, 5, 0, 0, 4],
        [8, 7, 0, 0, 2, 0, 6, 0, 0],
        [1, 2, 7, 0, 0, 0, 3, 0, 5],
        [0, 0, 0, 0, 0, 0, 8, 6, 0],
        [0, 0, 0, 1, 3, 0, 0, 0, 0]
    ]

    result = solve.col_elimination(puzzle, 6)
    assert result == puzzle_result, "Col should be solved"


def test_grid_elimination():
    puzzle = [
        [0, 0, 0, 0, 5, 6, 0, 0, 0],
        [0, 1, 9, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 7, 2, 3],
        [0, 0, 5, 0, 6, 0, 0, 3, 7],
        [2, 0, 0, 7, 0, 5, 0, 0, 4],
        [8, 7, 0, 0, 2, 0, 6, 0, 0],
        [1, 2, 7, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 8, 6, 0],
        [0, 0, 0, 1, 3, 0, 0, 0, 0]
    ]

    puzzle_result = [
        [0, 0, 0, 0, 5, 6, 0, 0, 0],
        [0, 1, 9, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 7, 2, 3],
        [0, 0, 5, 0, 6, 0, 0, 3, 7],
        [2, 0, 0, 7, 0, 5, 0, 0, 4],
        [8, 7, 0, 0, 2, 0, 6, 0, 0],
        [1, 2, 7, 0, 0, 0, 3, 0, 5],
        [0, 0, 0, 0, 0, 0, 8, 6, 1],
        [0, 0, 0, 1, 3, 0, 0, 7, 0]
    ]

    result = solve.grid_elimination(puzzle, 8)
    assert result == puzzle_result, "Grid should be solved"


def test_find_pairs_by_type_rows():
    puzzle = [
        [5, 8, 6, 0, 0, 0, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 0, 0, 8],
        [9, 3, 4, 1, 6, 8, 0, 0, 2],
        [0, 7, 0, 5, 4, 3, 0, 0, 6],
        [3, 6, 0, 0, 0, 0, 0, 8, 4],
        [4, 0, 0, 6, 8, 2, 0, 3, 0],
        [7, 0, 0, 3, 0, 6, 8, 4, 1],
        [0, 1, 3, 8, 7, 4, 0, 0, 9],
        [0, 4, 0, 0, 0, 0, 3, 0, 0]
    ]

    result = solve.find_pairs_by_type(puzzle, 'rows')
    keys = list(result['rows'].keys())
    assert keys[0] == 1, "Row number should be 1"
    assert result['rows'][1] == [6, 9], "List of values for row pais should be [6, 9]."

    assert keys[1] == 2, "Row number should be 2"
    assert result['rows'][2] == [5, 7], "List of values for row pais should be [5, 7]."


def test_find_pairs_by_type_none():
    puzzle = [
        [5, 8, 6, 0, 0, 0, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 0, 0, 8],
        [9, 3, 4, 1, 6, 8, 0, 0, 2],
        [0, 7, 0, 5, 4, 3, 0, 0, 6],
        [3, 6, 0, 0, 0, 0, 0, 8, 4],
        [4, 0, 0, 6, 8, 2, 0, 3, 0],
        [7, 0, 0, 3, 0, 6, 8, 4, 1],
        [0, 1, 3, 8, 7, 4, 0, 0, 9],
        [0, 4, 0, 0, 0, 0, 3, 0, 0]
    ]

    result = solve.find_pairs_by_type(puzzle, 'grids')
    keys = result['grids'].keys()
    assert not keys, "There should be no grids with pairs"


def test_find_pairs_by_type_cols():
    puzzle = [
        [5, 8, 6, 0, 0, 0, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 0, 0, 8],
        [9, 3, 4, 1, 6, 8, 0, 0, 2],
        [0, 7, 0, 5, 4, 3, 0, 0, 6],
        [3, 6, 0, 0, 0, 0, 0, 8, 4],
        [4, 0, 0, 6, 8, 2, 0, 3, 0],
        [7, 0, 0, 3, 0, 6, 8, 4, 1],
        [0, 1, 3, 8, 7, 4, 0, 0, 9],
        [0, 4, 0, 0, 0, 0, 3, 0, 0]
    ]

    result = solve.find_pairs_by_type(puzzle, 'cols')
    keys = list(result['cols'].keys())
    assert keys[0] == 1, "Col number should be 1"
    assert result['cols'][1] == [5, 9], "List of values for col pairs should be [5, 9]."


def test_find_pairs_by_type_grids():
    puzzle = [
        [5, 8, 6, 0, 0, 0, 4, 1, 3],
        [1, 2, 7, 4, 3, 5, 0, 0, 8],
        [9, 3, 4, 1, 6, 8, 0, 0, 2],
        [0, 7, 0, 5, 4, 3, 0, 0, 6],
        [3, 6, 0, 0, 0, 0, 0, 8, 4],
        [4, 0, 0, 6, 8, 2, 0, 3, 0],
        [7, 0, 0, 3, 0, 6, 8, 4, 1],
        [0, 1, 3, 8, 7, 4, 6, 0, 9],
        [0, 4, 0, 0, 0, 0, 3, 2, 0]
    ]

    result = solve.find_pairs_by_type(puzzle, 'grids')
    keys = list(result['grids'].keys())
    assert keys[0] == 8, "Grid number should be 8"
    assert result['grids'][8] == [5, 7], "List of values for grid pairs should be [5, 7]."
