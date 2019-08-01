import pytest
import copy
import json
import re
from solve_puzzle import solve
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


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
def test_puzzle_easy():
    incomplete_puzzle = [
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

    complete_puzzle = [
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

    return {'incomplete_puzzle': incomplete_puzzle, 'complete_puzzle': complete_puzzle}


@pytest.fixture
def test_puzzle_medium():
    incomplete_puzzle = [
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

    complete_puzzle = [
        [7, 4, 2, 3, 5, 6, 9, 1, 8],
        [3, 1, 9, 2, 8, 7, 5, 4, 6],
        [6, 5, 8, 9, 1, 4, 7, 2, 3],
        [4, 9, 5, 8, 6, 1, 2, 3, 7],
        [2, 6, 3, 7, 9, 5, 1, 8, 4],
        [8, 7, 1, 4, 2, 3, 6, 5, 9],
        [1, 2, 7, 6, 4, 8, 3, 9, 5],
        [9, 3, 4, 5, 7, 2, 8, 6, 1],
        [5, 8, 6, 1, 3, 9, 4, 7, 2]
    ]

    return {'incomplete_puzzle': incomplete_puzzle, 'complete_puzzle': complete_puzzle}


@pytest.fixture
def test_puzzle_hard():
    incomplete_puzzle = [
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

    complete_puzzle = [
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

    return {'incomplete_puzzle': incomplete_puzzle, 'complete_puzzle': complete_puzzle}


@pytest.fixture
def test_puzzle_extreme():
    incomplete_puzzle = [
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

    complete_puzzle = [
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

    return {'incomplete_puzzle': incomplete_puzzle, 'complete_puzzle': complete_puzzle}


@pytest.fixture
def test_puzzle_worlds_hardest():
    incomplete_puzzle = [
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

    complete_puzzle = [
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

    return {'incomplete_puzzle': incomplete_puzzle, 'complete_puzzle': complete_puzzle}


@pytest.fixture
def test_puzzle_extreme_after_methods_1_to_4():
    incomplete_puzzle = [
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

    complete_puzzle = [
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

    return {'incomplete_puzzle': incomplete_puzzle, 'complete_puzzle': complete_puzzle}


@pytest.fixture()
def api_gateway_event():
    """ Generates API GW Event"""

    return {
      "body": "{\"puzzle_rows\":[[0,8,0,0,6,4,7,0,3],[7,2,0,5,0,3,6,9,8],[0,0,0,0,0,2,4,1,0],[0,0,0,0,0,7,0,0,9],[0,9,6,3,0,8,1,5,0],[8,0,0,1,0,0,0,0,0],[0,4,2,8,0,0,0,0,0],[9,7,8,6,0,5,0,4,1],[6,0,5,4,7,0,0,8,0]]}",
      "resource": "/solve",
      "path": "/solve",
      "httpMethod": "POST",
      "isBase64Encoded": "false",
      "queryStringParameters": {
        "foo": "bar"
      },
      "pathParameters": {
        "proxy": "/path/to/resource"
      },
      "stageVariables": {
        "baz": "qux"
      },
      "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "max-age=0",
        "CloudFront-Forwarded-Proto": "https",
        "CloudFront-Is-Desktop-Viewer": "true",
        "CloudFront-Is-Mobile-Viewer": "false",
        "CloudFront-Is-SmartTV-Viewer": "false",
        "CloudFront-Is-Tablet-Viewer": "false",
        "CloudFront-Viewer-Country": "US",
        "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Custom User Agent String",
        "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
        "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https"
      },
      "requestContext": {
        "accountId": "123456789012",
        "resourceId": "123456",
        "stage": "prod",
        "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
        "requestTime": "09/Apr/2015:12:34:56 +0000",
        "requestTimeEpoch": 1428582896000,
        "identity": {
          "cognitoIdentityPoolId": "null",
          "accountId": "null",
          "cognitoIdentityId": "null",
          "caller": "null",
          "accessKey": "null",
          "sourceIp": "127.0.0.1",
          "cognitoAuthenticationType": "null",
          "cognitoAuthenticationProvider": "null",
          "userArn": "null",
          "userAgent": "Custom User Agent String",
          "user": "null"
        },
        "path": "/solve",
        "resourcePath": "/solve",
        "httpMethod": "POST",
        "apiId": "1234567890",
        "protocol": "HTTP/1.1"
      }
    }


class TestSolveCompletePuzzles:
    def test_solve_puzzle_easy(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        complete_puzzle = test_puzzle_easy['complete_puzzle']

        result = solve.solve_puzzle(incomplete_puzzle)
        assert result['status'], "Puzzle should be solved."
        assert result['puzzle'] == complete_puzzle, "Solution should match solution provided."

    def test_solve_puzzle5(self, test_puzzle_hard):
        incomplete_puzzle = test_puzzle_hard['incomplete_puzzle']
        complete_puzzle = test_puzzle_hard['complete_puzzle']

        result = solve.solve_puzzle(incomplete_puzzle)
        assert result['status'], "Puzzle should be solved."
        assert result['puzzle'] == complete_puzzle, "Solution should match solution provided."

    def test_solve_puzzle7(self, test_puzzle_extreme):
        incomplete_puzzle = test_puzzle_extreme['incomplete_puzzle']
        complete_puzzle = test_puzzle_extreme['complete_puzzle']

        result = solve.solve_puzzle(incomplete_puzzle)
        assert result['status'], "Puzzle should be solved."
        assert result['puzzle'] == complete_puzzle, "Solution should match solution provided."

    def test_solve_puzzle_worlds_hardest(self, test_puzzle_worlds_hardest):
        incomplete_puzzle = test_puzzle_worlds_hardest['incomplete_puzzle']
        complete_puzzle = test_puzzle_worlds_hardest['complete_puzzle']

        result = solve.solve_puzzle(incomplete_puzzle)
        assert result['status'], "Puzzle should be solved."
        assert result['puzzle'] == complete_puzzle, "Solution should match solution provided."


class TestSolveByMethod5:
    def test_solve_by_rows(self, test_puzzle_extreme_after_methods_1_to_4):
        incomplete_puzzle = test_puzzle_extreme_after_methods_1_to_4['incomplete_puzzle']
        complete_puzzle = test_puzzle_extreme_after_methods_1_to_4['complete_puzzle']

        result = solve.solve_with_method_5(incomplete_puzzle, 'rows')
        assert result['status'], "Puzzle should be solved."
        assert result['puzzle'] == complete_puzzle, "Solution should match solution provided."

    def test_solve_by_cols(self, test_puzzle_extreme_after_methods_1_to_4):
        incomplete_puzzle = test_puzzle_extreme_after_methods_1_to_4['incomplete_puzzle']
        complete_puzzle = test_puzzle_extreme_after_methods_1_to_4['complete_puzzle']

        result = solve.solve_with_method_5(incomplete_puzzle, 'cols')
        assert result['status'], "Puzzle should be solved."
        assert result['puzzle'] == complete_puzzle, "Solution should match solution provided."

    def test_solve_with_method_5_grids(self, test_puzzle_extreme_after_methods_1_to_4):
        incomplete_puzzle = test_puzzle_extreme_after_methods_1_to_4['incomplete_puzzle']
        incomplete_puzzle[7][6] = 6
        incomplete_puzzle[8][7] = 2

        complete_puzzle = test_puzzle_extreme_after_methods_1_to_4['complete_puzzle']

        result = solve.solve_with_method_5(incomplete_puzzle, 'grids')
        assert result['status'], "Puzzle should be solved."
        assert result['puzzle'] == complete_puzzle, "Solution should match solution provided."


class TestCheckComplete:
    def test_puzzle_for_completeness_fail(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        result = solve.puzzle_complete(incomplete_puzzle)
        assert not result, "Puzzle should not be complete."

    def test_puzzle_for_completeness(self, test_puzzle_easy):
        complete_puzzle = test_puzzle_easy['complete_puzzle']
        result = solve.puzzle_complete(complete_puzzle)
        assert result, "Puzzle should be complete."

    def test_row_not_complete(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        result = solve.row_col_grid_complete(incomplete_puzzle, "rows")
        assert not result, "Rows should not be complete."

    def test_col_not_complete(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        result = solve.row_col_grid_complete(incomplete_puzzle, "cols")
        assert not result, "Cols should not be complete."

    def test_grid_not_complete(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        result = solve.row_col_grid_complete(incomplete_puzzle, "grids")
        assert not result, "Grids should not be complete."

    def test_row_complete(self, test_puzzle_easy):
        complete_puzzle = test_puzzle_easy['complete_puzzle']
        result = solve.row_col_grid_complete(complete_puzzle, "rows")
        assert result, "Rows should be complete."

    def test_col_complete(self, test_puzzle_easy):
        complete_puzzle = test_puzzle_easy['complete_puzzle']
        result = solve.row_col_grid_complete(complete_puzzle, "cols")
        assert result, "Cols should be complete."

    def test_grid_complete(self, test_puzzle_easy):
        complete_puzzle = test_puzzle_easy['complete_puzzle']
        result = solve.row_col_grid_complete(complete_puzzle, "grids")
        assert result, "Grids should be complete."


class TestEliminationMethods:
    def test_eliminate_values_with_1_missing(self):
        remaining_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        row = [0, 2, 3, 4, 5, 6, 7, 8, 9]
        result = solve.elimate_list_values(remaining_values, row)
        assert result == [1], "All values except the number 1 should have been eliminated."

    def test_eliminate_values_with_9_missing(self):
        remaining_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        row = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        result = solve.elimate_list_values(remaining_values, row)
        assert result == [9], "All values except the number 9 should have been eliminated."

    def test_eliminate_values_with_8_and_9_missing(self):
        remaining_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        row = [1, 2, 3, 4, 5, 6, 7, 0, 0]
        result = solve.elimate_list_values(remaining_values, row)
        assert result == [8, 9], "All values except the numbers 8 & 9 should have been eliminated."

    def test_eliminate_values_for_cell_0_7(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        result = solve.eliminate_cell_values(incomplete_puzzle, 0, 7)
        assert result['status'], "Cell should be solved as row 0 and col 7 eliminate all values except 2."
        assert result['values'] == [2], "Value for cell should be 2."

    def test_eliminate_values_for_cell_1_4(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        result = solve.eliminate_cell_values(incomplete_puzzle, 1, 4)
        assert result['values'] == [1], "Value for cell should be 1."

    def test_eliminate_values_for_cell_1_2(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        result = solve.eliminate_cell_values(incomplete_puzzle, 1, 2)
        assert not result['status'], "Cell is not solved as row 1 and col 2 leave a number of values."
        assert result['values'] == [1, 4], "List of values for cell should be [1, 4]."

    def test_eliminate_values_for_cell_8_6(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        result = solve.eliminate_cell_values(incomplete_puzzle, 8, 6)
        assert not result['status'], "Cell is not solved as row 8 and col 6 leave a number of values."
        assert result['values'] == [2, 3, 9], "List of values for cell should be [2, 3, 9]."

    def test_row_elimination(self, test_puzzle_medium):
        incomplete_puzzle = test_puzzle_medium['incomplete_puzzle']
        puzzle_result = copy.deepcopy(incomplete_puzzle)
        puzzle_result[3][6] = 2

        result = solve.row_elimination(incomplete_puzzle, 3)
        assert result == puzzle_result, "Row 3, col 6, should have had the value 2 added."

    def test_col_elimination(self, test_puzzle_medium):
        incomplete_puzzle = test_puzzle_medium['incomplete_puzzle']
        puzzle_result = copy.deepcopy(incomplete_puzzle)
        puzzle_result[1][6] = 5
        puzzle_result[6][6] = 3

        result = solve.col_elimination(incomplete_puzzle, 6)
        assert result == puzzle_result, "Col 6 should have had values 3 and 5 added."

    def test_grid_elimination(self, test_puzzle_medium):
        incomplete_puzzle = test_puzzle_medium['incomplete_puzzle']
        puzzle_result = copy.deepcopy(incomplete_puzzle)
        puzzle_result[6][6] = 3
        puzzle_result[7][8] = 1
        puzzle_result[8][7] = 7

        result = solve.grid_elimination(incomplete_puzzle, 8)
        assert result == puzzle_result, "Grid 8 should have had values 1, 3 and 7 added."


class TestFindPairs:
    def test_find_pairs_by_type_rows(self, test_puzzle_extreme_after_methods_1_to_4):
        incomplete_puzzle = test_puzzle_extreme_after_methods_1_to_4['incomplete_puzzle']

        result = solve.find_pairs_by_type(incomplete_puzzle, 'rows')
        keys = list(result['rows'].keys())
        assert keys[0] == 1, "Row number should be 1"
        assert result['rows'][1] == [6, 9], "List of values for row pairs should be [6, 9]."

        assert keys[1] == 2, "Row number should be 2"
        assert result['rows'][2] == [5, 7], "List of values for row pairs should be [5, 7]."

    def test_find_pairs_by_type_none(self, test_puzzle_extreme_after_methods_1_to_4):
        incomplete_puzzle = test_puzzle_extreme_after_methods_1_to_4['incomplete_puzzle']

        result = solve.find_pairs_by_type(incomplete_puzzle, 'grids')
        keys = result['grids'].keys()
        assert not keys, "There should be no grids with pairs"

    def test_find_pairs_by_type_cols(self, test_puzzle_extreme_after_methods_1_to_4):
        incomplete_puzzle = test_puzzle_extreme_after_methods_1_to_4['incomplete_puzzle']

        result = solve.find_pairs_by_type(incomplete_puzzle, 'cols')
        keys = list(result['cols'].keys())
        assert keys[0] == 1, "Col number should be 1"
        assert result['cols'][1] == [5, 9], "List of values for col pairs should be [5, 9]."

    def test_find_pairs_by_type_grids(self, test_puzzle_extreme_after_methods_1_to_4):
        incomplete_puzzle = test_puzzle_extreme_after_methods_1_to_4['incomplete_puzzle']
        incomplete_puzzle[7][6] = 6
        incomplete_puzzle[8][7] = 2

        result = solve.find_pairs_by_type(incomplete_puzzle, 'grids')
        keys = list(result['grids'].keys())
        assert keys[0] == 8, "Grid number should be 8"
        assert result['grids'][8] == [5, 7], "List of values for grid pairs should be [5, 7]."


class TestUpdate:
    def test_update_cell(self, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        complete_puzzle = copy.deepcopy(incomplete_puzzle)
        complete_puzzle[0][0] = 5

        puzzle_result = solve.update_cell(incomplete_puzzle, 0, 0, 5)
        assert puzzle_result == complete_puzzle, "Cell was not updated."


def test_create_response():
    response = solve.create_response(200, 'Success message')

    expected_response = {'statusCode': 200,
                         'body': 'Success message',
                         'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': 'https://staging.sudokuless.com'
                         }}
    assert response == expected_response, "Create_response did not return the expected response value."


class TestSolveMain:
    def test_solve_main_returns_response(self, api_gateway_event):
        response = solve.solve_main(api_gateway_event)
        assert response['statusCode'] == 200
        # assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert re.match('{"status": .*}', response['body'])

    def test_solve_main_no_body(self, api_gateway_event):
        event_no_body = copy.deepcopy(api_gateway_event)
        event_no_body['body'] = '{}'
        response = solve.solve_main(event_no_body)
        assert response['statusCode'] == 500
        # assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert response['body'] == '{"error": "API Event did not contain a valid puzzle."}'

    def test_solve_main_data_validation_fail(self, api_gateway_event, empty_puzzle):
        event_no_body = copy.deepcopy(api_gateway_event)
        empty_puzzle[0][1] = "1"
        event_no_body['body'] = "{\"puzzle_rows\": " + json.dumps(empty_puzzle) + "}"

        response = solve.solve_main(event_no_body)
        assert response['statusCode'] == 500
        # assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert response['body'] == '{"error": "Puzzle was not validated due to wrong data types."}'

    def test_solve_main_puzzle_validation_fail(self, api_gateway_event, empty_puzzle):
        event_no_body = copy.deepcopy(api_gateway_event)
        empty_puzzle[0][1] = 1
        empty_puzzle[0][8] = 1
        event_no_body['body'] = "{\"puzzle_rows\": " + json.dumps(empty_puzzle) + "}"

        response = solve.solve_main(event_no_body)
        assert response['statusCode'] == 500
        # assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert response['body'] == '{"error": "Puzzle was not validated due to invalid row, column or grid."}'


def test_handler(api_gateway_event):
    response = solve.handler(api_gateway_event, None)
    assert response['statusCode'] == 200
    # assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    assert re.match('{"status": .*}', response['body'])
