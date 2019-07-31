import pytest
import copy
from solve_puzzle import common
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


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


class TestApiEvent:
    def test_get_puzzle_from_event(self, api_gateway_event, test_puzzle_easy):
        incomplete_puzzle = test_puzzle_easy['incomplete_puzzle']
        result = common.get_puzzle_from_event(api_gateway_event)
        assert result == incomplete_puzzle, "Puzzle returned from event was not as expected."

    def test_get_puzzle_with_empty_event(self, api_gateway_event, test_puzzle_easy):
        with pytest.raises(Exception) as e:
            common.get_puzzle_from_event(None)
        assert str(e.value) == "API Event was empty."

    def test_get_puzzle_with_empty_body(self, api_gateway_event, test_puzzle_easy):
        event_no_body = copy.deepcopy(api_gateway_event)
        event_no_body['body'] = None
        with pytest.raises(Exception) as e:
            common.get_puzzle_from_event(event_no_body)
        assert str(e.value) == "API Event did not contain a valid body."

    def test_get_puzzle_with_no_puzzle(self, api_gateway_event, test_puzzle_easy):
        event_no_body = copy.deepcopy(api_gateway_event)
        event_no_body['body'] = '{}'
        with pytest.raises(Exception) as e:
            common.get_puzzle_from_event(event_no_body)
        assert str(e.value) == "API Event did not contain a valid puzzle."
