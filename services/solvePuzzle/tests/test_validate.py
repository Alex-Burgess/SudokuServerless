import pytest
from solve_puzzle import validate


def test_validate_row_col_grid():
    row = [1, 1, 0, 0, 0, 0, 0, 0, 0]
    result = validate.validate_row_col_grid(row, "row")
    assert not result, "Validation should fail due to duplicate 1s."

    row = [0, 0, 0, 0, 0, 0, 0, 9, 9]
    result = validate.validate_row_col_grid(row, "row")
    assert not result, "Validation should fail due to duplicate 9s."

    row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = validate.validate_row_col_grid(row, "row")
    assert result, "Validation should succeed as no duplicates."


def test_object_for_data_type():
    test_puzzle = [
        ["1", "1", "3", "4", "5", "6", "7", "8", "9"],
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 9]
    ]
    result = validate.validata_data_types(test_puzzle)
    assert not result, "Validation should fail due to string values."

    test_puzzle = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 9]
    ]
    result = validate.validata_data_types(test_puzzle)
    assert result, "Validation should succeed as array is of ints."


def test_validate_puzzle_duplicate_in_row():
    # Puzzle with duplicates in two rows, columns and grids
    test_puzzle = [
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    result = validate.validate_puzzle(test_puzzle)
    assert not result, "Puzzle validation should not succeed as duplicates in row 1."

    test_puzzle2 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 9]
    ]

    result = validate.validate_puzzle(test_puzzle2)
    assert not result, "Puzzle validation should not succeed as duplicates in row 9."


def test_validate_puzzle_duplicate_in_column():
    # Puzzle with duplicates in two rows, columns and grids
    test_puzzle = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    result = validate.validate_puzzle(test_puzzle)
    assert not result, "Puzzle validation should not succeed as duplicates in column 1."

    test_puzzle2 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9]
    ]

    result = validate.validate_puzzle(test_puzzle2)
    assert not result, "Puzzle validation should not succeed as duplicates in column 9."


def test_validate_puzzle_duplicate_in_grid():
    # Puzzle with duplicates in two rows, columns and grids
    test_puzzle = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    result = validate.validate_puzzle(test_puzzle)
    assert not result, "Puzzle validation should not succeed as duplicates in grid 1."

    test_puzzle2 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9]
    ]

    result = validate.validate_puzzle(test_puzzle2)
    assert not result, "Puzzle validation should not succeed as duplicates in grid 9."


def test_validate_puzzle():
    # Puzzle with duplicates in two rows, columns and grids
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

    result = validate.validate_puzzle(test_puzzle)
    assert result, "Puzzle expected to be validated"
