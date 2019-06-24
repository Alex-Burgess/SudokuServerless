import pytest
from solve_puzzle import common


@pytest.fixture
def test_puzzle():
    test_puzzle = [
        [1, 2, 3, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 7, 8, 9]
    ]
    return test_puzzle


class TestGetLists:
    def test_get_row(sef, test_puzzle):
        first_row = common.get_row(test_puzzle, 0)
        assert first_row == [1, 2, 3, 0, 0, 0, 0, 0, 0], "First row did not match expected values."

        last_row = common.get_row(test_puzzle, 8)
        assert last_row == [0, 0, 0, 0, 0, 0, 7, 8, 9], "Last row did not match expected values."

    def test_get_column(self, test_puzzle):
        first_column = common.get_column(test_puzzle, 0)
        assert first_column == [1, 4, 5, 6, 7, 0, 0, 0, 0], "First column did not match expected values."

        last_column = common.get_column(test_puzzle, 8)
        assert last_column == [0, 0, 0, 0, 0, 0, 1, 2, 9], "Last column did not match expected values."

    def test_get_grid(self, test_puzzle):
        first_grid = common.get_grid(test_puzzle, 0)
        assert first_grid == [1, 2, 3, 4, 0, 0, 5, 0, 0], "First grid did not match expected values."

        last_grid = common.get_grid(test_puzzle, 8)
        assert last_grid == [0, 0, 1, 0, 0, 2, 7, 8, 9], "Last grid did not match expected values."


class TestGridInteractions:
    def test_grid_top_left_cell_number(self):
        grid1 = common.grid_top_left_cell_number(0)
        assert grid1 == [0, 0], "Grid 1 coordinates did not match expected values."

        grid9 = common.grid_top_left_cell_number(8)
        assert grid9 == [6, 6], "Grid 9 coordinates did not match expected values."

    def test_get_grid_number(self, test_puzzle):
        grid_num = common.get_grid_number(test_puzzle, 0, 0)
        assert grid_num == 0, "Grid number for row 0, col 0 should be 0."

        grid_num = common.get_grid_number(test_puzzle, 1, 1)
        assert grid_num == 0, "Grid number for row 1, col 1 should be 0."

        grid_num = common.get_grid_number(test_puzzle, 2, 2)
        assert grid_num == 0, "Grid number for row 2, col 2 should be 0."

        grid_num = common.get_grid_number(test_puzzle, 3, 3)
        assert grid_num == 4, "Grid number for row 3, col 3 should be 4."

        grid_num = common.get_grid_number(test_puzzle, 8, 8)
        assert grid_num == 8, "Grid number for row 8, col 8 should be 8."

    def test_get_row_numbers_from_grid(self, test_puzzle):
        result = common.get_row_numbers_from_grid(test_puzzle, 0)
        assert result == [0, 1, 2], "Row numbers from grid 0 should be 0, 1, 2"

        result = common.get_row_numbers_from_grid(test_puzzle, 3)
        assert result == [3, 4, 5], "Row numbers from grid 3 should be 3, 4, 5"

        result = common.get_row_numbers_from_grid(test_puzzle, 8)
        assert result == [6, 7, 8], "Row numbers from grid 8 should be 6, 7, 8"

    def test_get_row_number_from_grid(self, test_puzzle):
        result = common.get_row_number_from_grid(test_puzzle, 0, 0)
        assert result == 0, "Row number should be 0."

        result = common.get_row_number_from_grid(test_puzzle, 0, 1)
        assert result == 0, "Row number should be 0."

        result = common.get_row_number_from_grid(test_puzzle, 0, 3)
        assert result == 1, "Row number should be 2."

        result = common.get_row_number_from_grid(test_puzzle, 8, 8)
        assert result == 8, "Row number should be 8."

    def test_get_col_numbers_from_grid(self, test_puzzle):
        result = common.get_col_numbers_from_grid(test_puzzle, 0)
        assert result == [0, 1, 2], "Row numbers from grid 0 should be 0, 1, 2"

        result = common.get_col_numbers_from_grid(test_puzzle, 3)
        assert result == [0, 1, 2], "Row numbers from grid 3 should be 0, 1, 2"

        result = common.get_col_numbers_from_grid(test_puzzle, 4)
        assert result == [3, 4, 5], "Row numbers from grid 4 should be 3, 4, 5"

        result = common.get_col_numbers_from_grid(test_puzzle, 8)
        assert result == [6, 7, 8], "Row numbers from grid should be 6, 7, 8"

    def test_get_col_number_from_grid(self, test_puzzle):
        result = common.get_col_number_from_grid(test_puzzle, 0, 0)
        assert result == 0, "Col number should be 0."

        result = common.get_col_number_from_grid(test_puzzle, 0, 1)
        assert result == 1, "Col number should be 1."

        result = common.get_col_number_from_grid(test_puzzle, 0, 3)
        assert result == 0, "Col number should be 0."

        result = common.get_col_number_from_grid(test_puzzle, 8, 0)
        assert result == 6, "Col number should be 6."

        result = common.get_col_number_from_grid(test_puzzle, 8, 8)
        assert result == 8, "Col number should be 8."


def test_cell_contains_number(test_puzzle):
    result = common.cell_contains_number(test_puzzle, 0, 0)
    assert result, "Cell in row 0, col 0 countains a value."

    result = common.cell_contains_number(test_puzzle, 0, 3)
    assert not result, "Cell in row 0, col 1 does not countain a value."

    result = common.cell_contains_number(test_puzzle, 8, 8)
    assert result, "Cell in row 8, col 8 countains a value."


def test_get_empty_cell_refs():
    row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = common.get_empty_cell_refs(row)
    assert result == [], "row should return empty array as no empty cells."

    row = [0, 2, 3, 4, 5, 6, 7, 8, 9]
    result = common.get_empty_cell_refs(row)
    assert result == [0], "row should return cell ref 0."

    row = [0, 2, 3, 4, 5, 6, 7, 0, 0]
    result = common.get_empty_cell_refs(row)
    assert result == [0, 7, 8], "row should return cell refs 0, 7 and 8."
