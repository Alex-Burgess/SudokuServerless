import json
import os
import re
import pytest
import boto3
import copy
from moto import mock_s3
from get_new_puzzle_solution import solution


@pytest.fixture
def s3_bucket_mock(monkeypatch):
    """Uses moto to mock an s3 bucket.  A bucket called test-bucket is created and 3 puzzles are added to it."""
    bucket_name = 'test-bucket'

    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    example_puzzles_path = path + '/../../../data/example_puzzle_solutions'

    monkeypatch.setitem(os.environ, 'AWS_SECRET_ACCESS_KEY', 'foobar_secret')
    monkeypatch.setitem(os.environ, 'AWS_ACCESS_KEY_ID', 'foobar_key')

    # setup: start moto server and create the bucket
    mock = mock_s3()
    mock.start()
    # Create Bucket so that test can run
    s3 = boto3.resource('s3', region_name='eu-west-1')
    s3.create_bucket(Bucket=bucket_name)

    # Add file for testing
    for key in ['1.json', '2.json', '3.json']:
        upload_filename = example_puzzles_path + '/' + key
        s3.meta.client.upload_file(upload_filename, bucket_name, key)

    yield
    # teardown: stop moto server
    mock.stop()


@pytest.fixture
def test_puzzle_json():
    input_puzzle_json = {
                            "level": "easy",
                            "puzzle_rows": [
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
                        }

    return input_puzzle_json


@pytest.fixture()
def api_gateway_event():
    """ Generates API GW Event"""

    return {
      "body": "eyJ0ZXN0IjoiYm9keSJ9",
      "resource": "/getNewPuzzleSolution/{id}",
      "path": "/getNewPuzzleSolution/1.json",
      "httpMethod": "GET",
      "isBase64Encoded": "true",
      "queryStringParameters": {
        "foo": "bar"
      },
      "pathParameters": {
        "id": "1.json"
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
        "path": "/getNewPuzzleSolution/{id}",
        "resourcePath": "/getNewPuzzleSolution/{id}",
        "httpMethod": "GET",
        "apiId": "1234567890",
        "protocol": "HTTP/1.1"
      }
    }


def test_create_response():
    response = solution.create_response(200, 'Success message')

    expected_response = {'statusCode': 200,
                         'body': 'Success message',
                         'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                         }}
    assert response == expected_response, "Create_response did not return the expected response value."


class TestGetPuzzleIdFromPath:
    def test_puzzle_id_present(self, api_gateway_event):
        puzzle_id = solution.get_puzzle_id_from_path(api_gateway_event)
        assert puzzle_id == '1.json'

    def test_puzzle_id_not_present(self, api_gateway_event):
        updated_event_path_parameters = copy.deepcopy(api_gateway_event)
        updated_event_path_parameters['pathParameters'].pop('id', None)

        with pytest.raises(Exception) as e:
            solution.get_puzzle_id_from_path(updated_event_path_parameters)
        assert str(e.value) == "No id path parameter was provided."


class TestEnvironmentVariable:
    def test_get_bucket_name(self, monkeypatch):
        monkeypatch.setitem(os.environ, 'SOLUTIONS_BUCKET_NAME', 'test-bucket')
        bucket_name = solution.get_bucket_name()
        assert bucket_name == 'test-bucket'

    def test_wrong_variable_name(self, monkeypatch):
        monkeypatch.setitem(os.environ, 'SOLUTIONS_BUCKET_NAM', 'test-bucket')
        with pytest.raises(Exception) as e:
            solution.get_bucket_name()
        assert str(e.value) == "SOLUTIONS_BUCKET_NAME environment variable not set correctly"

    def test_no_variable(self, monkeypatch):
        with pytest.raises(Exception) as e:
            solution.get_bucket_name()
        assert str(e.value) == "SOLUTIONS_BUCKET_NAME environment variable not set correctly"


class TestGetPuzzleFromS3:
    def test_get_puzzle_from_s3(self, s3_bucket_mock, test_puzzle_json):
        puzzle_object = solution.get_puzzle_from_s3('test-bucket', '1.json')
        assert json.loads(puzzle_object) == test_puzzle_json

    def test_key_does_not_exist(self, s3_bucket_mock):
        with pytest.raises(Exception) as e:
            solution.get_puzzle_from_s3('test-bucket', '4.json')
        assert str(e.value) == "An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist."

    def test_bucket_does_not_exist(self, monkeypatch, s3_bucket_mock):
        monkeypatch.setitem(os.environ, 'SOLUTIONS_BUCKET_NAME', 'test-bucket2')
        with pytest.raises(Exception) as e:
            solution.get_puzzle_from_s3('test-bucket2', '1.json')
        assert str(e.value) == "An error occurred (NoSuchBucket) when calling the GetObject operation: The specified bucket does not exist"


class TestSolutionMain:
    def test_solution_main_returns_response(self, monkeypatch, s3_bucket_mock, api_gateway_event):
        monkeypatch.setitem(os.environ, 'SOLUTIONS_BUCKET_NAME', 'test-bucket')
        response = solution.solution_main(api_gateway_event)
        assert response['statusCode'] == 200
        assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert re.match('{"level": .*}', response['body'])

    def test_solution_main_exception_response(self, monkeypatch, s3_bucket_mock, api_gateway_event):
        monkeypatch.setitem(os.environ, 'SOLUTIONS_BUCKET_NAME', 'test-bucke')
        response = solution.solution_main(api_gateway_event)
        assert response['statusCode'] == 500
        assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert response['body'] == '{"error": "An error occurred (NoSuchBucket) when calling the GetObject operation: The specified bucket does not exist"}'

    def test_solution_main_no_env_variable(self, s3_bucket_mock, api_gateway_event):
        response = solution.solution_main(api_gateway_event)
        assert response['statusCode'] == 500
        assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert response['body'] == '{"error": "SOLUTIONS_BUCKET_NAME environment variable not set correctly"}'

    def test_solution_main_bucket_does_not_exist(self, monkeypatch, s3_bucket_mock, api_gateway_event):
        monkeypatch.setitem(os.environ, 'SOLUTIONS_BUCKET_NAME', 'test-bucket2')
        response = solution.solution_main(api_gateway_event)
        assert response['statusCode'] == 500
        assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert response['body'] == '{"error": "An error occurred (NoSuchBucket) when calling the GetObject operation: The specified bucket does not exist"}'


def test_handler(monkeypatch, api_gateway_event, s3_bucket_mock):
    monkeypatch.setitem(os.environ, 'SOLUTIONS_BUCKET_NAME', 'test-bucket')
    response = solution.handler(api_gateway_event, None)
    assert response['statusCode'] == 200
    assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    assert re.match('{"level": .*}', response['body'])
