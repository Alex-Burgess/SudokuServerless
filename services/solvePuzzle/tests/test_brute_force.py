import pytest
from solve_puzzle import brute_force


@pytest.fixture
def test_puzzle():
    incomplete_puzzle = [
        [0, 9, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 5, 0],
        [6, 7, 5, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 2, 0, 8],
        [0, 0, 9, 0, 5, 0, 6, 0, 0],
        [2, 0, 4, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 8, 6, 4],
        [0, 2, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 9, 0]
    ]

    complete_puzzle = [
        [1, 9, 3, 2, 7, 5, 4, 8, 6],
        [8, 4, 2, 9, 1, 6, 3, 5, 7],
        [6, 7, 5, 3, 8, 4, 1, 2, 9],
        [5, 6, 7, 1, 4, 9, 2, 3, 8],
        [3, 8, 9, 7, 5, 2, 6, 4, 1],
        [2, 1, 4, 8, 6, 3, 9, 7, 5],
        [9, 3, 1, 5, 2, 7, 8, 6, 4],
        [7, 2, 6, 4, 9, 8, 5, 1, 3],
        [4, 5, 8, 6, 3, 1, 7, 9, 2]
    ]

    return {'incomplete_puzzle': incomplete_puzzle, 'complete_puzzle': complete_puzzle}


def test_solve_puzzle(test_puzzle):
    incomplete_puzzle = test_puzzle['incomplete_puzzle']
    complete_puzzle = test_puzzle['complete_puzzle']

    result = brute_force.solve_wrapper(incomplete_puzzle)
    assert result['status'], "Puzzle should be solved."
    assert result['puzzle'] == complete_puzzle, "Solution should match solution provided."


def test_convert_for_brute_force(test_puzzle):
    incomplete_puzzle = test_puzzle['incomplete_puzzle']

    test_result = [
        0, 9, 0, 2, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 3, 5, 0,
        6, 7, 5, 0, 0, 4, 0, 0, 0,
        0, 0, 0, 0, 4, 0, 2, 0, 8,
        0, 0, 9, 0, 5, 0, 6, 0, 0,
        2, 0, 4, 0, 6, 0, 0, 0, 0,
        0, 0, 0, 5, 0, 0, 8, 6, 4,
        0, 2, 6, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 9, 0
    ]

    result = brute_force.convert_to_bf(incomplete_puzzle)
    assert result == test_result


def test_convert_from_brute_force(test_puzzle):
    puzzle = [
         1, 9, 3, 2, 7, 5, 4, 8, 6,
         8, 4, 2, 9, 1, 6, 3, 5, 7,
         6, 7, 5, 3, 8, 4, 1, 2, 9,
         5, 6, 7, 1, 4, 9, 2, 3, 8,
         3, 8, 9, 7, 5, 2, 6, 4, 1,
         2, 1, 4, 8, 6, 3, 9, 7, 5,
         9, 3, 1, 5, 2, 7, 8, 6, 4,
         7, 2, 6, 4, 9, 8, 5, 1, 3,
         4, 5, 8, 6, 3, 1, 7, 9, 2
    ]

    complete_puzzle = test_puzzle['complete_puzzle']

    result = brute_force.convert_from_bf(puzzle)
    assert result == complete_puzzle
