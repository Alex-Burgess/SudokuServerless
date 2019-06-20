import pytest
from solve_puzzle import solve


def test_solve_puzzle():
    test_puzzle = [
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
    result = solve.solve_puzzle(test_puzzle)
    assert result['status'], "Puzzle should be solved."


def test_update_cell():
    test_puzzle = [
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
    puzzle_result = solve.update_cell(test_puzzle, 0, 0, 4)
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
    test_puzzle = [
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

    result = solve.eliminate_cell_values(test_puzzle, 3, 5)
    assert result['status'], "Cell should be solved as row 3 and col 5 eliminate all values except 7."
    assert result['values'] == [7], "Value for cell should be 7."

    result = solve.eliminate_cell_values(test_puzzle, 4, 8)
    assert result['values'] == [4], "Value for cell should be 4."

    result = solve.eliminate_cell_values(test_puzzle, 0, 0)
    assert not result['status'], "Cell is not solved as row 0 and col 0 leave a number of values."
    assert result['values'] == [4, 6], "List of values for cell should be [4, 6]."

    result = solve.eliminate_cell_values(test_puzzle, 8, 8)
    assert not result['status'], "Cell is not solved as row 8 and col 8 leave a number of values."
    assert result['values'] == [3, 5, 7], "List of values for cell should be [3, 5, 7]."
