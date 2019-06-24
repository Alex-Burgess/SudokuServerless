import pytest
from solve_puzzle import validate


@pytest.fixture
def empty_puzzle():
    test_puzzle = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    return test_puzzle


@pytest.fixture
def valid_incomplete_puzzle():
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
    return test_puzzle


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


def test_object_for_data_type(valid_incomplete_puzzle):
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

    result = validate.validata_data_types(valid_incomplete_puzzle)
    assert result, "Validation should succeed as array is of ints."


def test_validate_puzzle(valid_incomplete_puzzle):
    result = validate.validate_puzzle(valid_incomplete_puzzle)
    assert result, "Puzzle expected to be validated"


class TestDuplicates:
    def test_validate_puzzle_duplicate_in_row0(self, empty_puzzle):
        empty_puzzle[0][1] = 1
        empty_puzzle[0][8] = 1

        result = validate.validate_puzzle(empty_puzzle)
        assert not result, "Puzzle validation should not succeed as duplicates in row 1."

    def test_validate_puzzle_duplicate_in_row8(self, empty_puzzle):
        empty_puzzle[8][1] = 9
        empty_puzzle[8][8] = 9

        result = validate.validate_puzzle(empty_puzzle)
        assert not result, "Puzzle validation should not succeed as duplicates in row 9."

    def test_validate_puzzle_duplicate_in_column0(self, empty_puzzle):
        empty_puzzle[0][0] = 1
        empty_puzzle[8][0] = 1

        result = validate.validate_puzzle(empty_puzzle)
        assert not result, "Puzzle validation should not succeed as duplicates in column 1."

    def test_validate_puzzle_duplicate_in_column8(self, empty_puzzle):
        empty_puzzle[0][8] = 9
        empty_puzzle[8][8] = 9

        result = validate.validate_puzzle(empty_puzzle)
        assert not result, "Puzzle validation should not succeed as duplicates in column 9."

    def test_validate_puzzle_duplicate_in_grid0(self, empty_puzzle):
        empty_puzzle[0][0] = 1
        empty_puzzle[2][2] = 1

        result = validate.validate_puzzle(empty_puzzle)
        assert not result, "Puzzle validation should not succeed as duplicates in grid 1."

    def test_validate_puzzle_duplicate_in_grid8(self, empty_puzzle):
        empty_puzzle[6][6] = 9
        empty_puzzle[8][8] = 9

        result = validate.validate_puzzle(empty_puzzle)
        assert not result, "Puzzle validation should not succeed as duplicates in grid 9."
