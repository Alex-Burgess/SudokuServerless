import pytest
from solve_puzzle import solve


def test_validate_row():
    row = [1, 1, 0, 0, 0, 0, 0, 0, 0]
    result = solve.validate_row(row)
    assert not result, "Row validation should fail due to duplicate 1s."

    row = [0, 0, 0, 0, 0, 0, 0, 9, 9]
    result = solve.validate_row(row)
    assert not result, "Row validation should fail due to duplicate 9s."

    row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = solve.validate_row(row)
    assert result, "Row validation should succeed as no duplicates."
