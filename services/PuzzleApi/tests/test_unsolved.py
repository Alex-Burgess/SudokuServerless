import json
import re
import os
import copy
import pytest
import boto3
from moto import mock_s3
from puzzle import unsolved

import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


@pytest.fixture
def s3_bucket_mock(monkeypatch):
    """Uses moto to mock an s3 bucket.  A bucket called test-bucket is created and 3 puzzles are added to it."""
    bucket_name = 'test-bucket'

    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    example_puzzles_path = path + '/../../../data/example_puzzles'

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
                        }

    return input_puzzle_json


@pytest.fixture()
def api_gateway_event():
    """ Generates API GW Event"""

    return {
        "resource": "/puzzle",
        "path": "/puzzle",
        "httpMethod": "GET",
        "headers": "null",
        "multiValueHeaders": "null",
        "queryStringParameters": "null",
        "multiValueQueryStringParameters": "null",
        "pathParameters": "null",
        "stageVariables": "null",
        "requestContext": {
            "path": "/puzzle",
            "accountId": "12345",
            "resourceId": "123456",
            "stage": "local",
            "domainPrefix": "testPrefix",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
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
            "resourcePath": "/puzzle",
            "httpMethod": "GET",
            "apiId": "1234567890"
        },
        "body": "null",
        "isBase64Encoded": "false"
    }


def test_create_response():
    response = unsolved.create_response(200, 'Success message')

    expected_response = {'statusCode': 200,
                         'body': 'Success message',
                         'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                         }}
    assert response == expected_response, "Create_response did not return the expected response value."


def test_add_id_to_returned_json(test_puzzle_json):
    exected_puzzle_json = copy.deepcopy(test_puzzle_json)
    exected_puzzle_json['id'] = "1.json"

    output_data = unsolved.add_id_to_returned_json(json.dumps(test_puzzle_json), '1.json')
    assert output_data == json.dumps(exected_puzzle_json), "ID was not added to puzzle json object."


class TestEnvironmentVariable:
    def test_get_bucket_name(self, monkeypatch):
        monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'test-bucket')
        bucket_name = unsolved.get_bucket_name()
        assert bucket_name == 'test-bucket'

    def test_wrong_variable_name(self, monkeypatch):
        monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAM', 'test-bucket')
        with pytest.raises(Exception) as e:
            unsolved.get_bucket_name()
        assert str(e.value) == "UNSOLVED_BUCKET_NAME environment variable not set correctly"

    def test_no_variable(self):
        with pytest.raises(Exception) as e:
            unsolved.get_bucket_name()
        assert str(e.value) == "UNSOLVED_BUCKET_NAME environment variable not set correctly"


class TestGetRandomKey:
    def test_get_random_key(self, s3_bucket_mock):
        key = unsolved.get_random_key('test-bucket')
        assert re.match('[1-3].json', key)

    def test_bucket_does_not_exist(self, s3_bucket_mock):
        with pytest.raises(Exception) as e:
            unsolved.get_random_key('test-bucket2')
        assert str(e.value) == "An error occurred (NoSuchBucket) when calling the ListObjects operation: The specified bucket does not exist"


class TestGetPuzzleFromS3:
    def test_get_puzzle_from_s3(self, s3_bucket_mock, test_puzzle_json):
        puzzle_object = unsolved.get_puzzle_from_s3('test-bucket', '1.json')
        assert json.loads(puzzle_object) == test_puzzle_json

    def test_key_does_not_exist(self, s3_bucket_mock):
        with pytest.raises(Exception) as e:
            unsolved.get_puzzle_from_s3('test-bucket', '4.json')
        assert str(e.value) == "An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist."

    def test_bucket_does_not_exist(self, monkeypatch, s3_bucket_mock):
        monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'test-bucket2')
        with pytest.raises(Exception) as e:
            unsolved.get_puzzle_from_s3('test-bucket2', '1.json')
        assert str(e.value) == "An error occurred (NoSuchBucket) when calling the GetObject operation: The specified bucket does not exist"


class TestUnsolvedPuzzleMain:
    def test_unsolved_main_returns_response(self, monkeypatch, s3_bucket_mock):
        monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'test-bucket')
        response = unsolved.unsolved_puzzle_main()
        assert response['statusCode'] == 200
        assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert re.match('{"level": .*}', response['body'])

    def test_unsolved_main_exception_response(self, monkeypatch, s3_bucket_mock):
        monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'test-bucke')
        response = unsolved.unsolved_puzzle_main()
        assert response['statusCode'] == 500
        assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert response['body'] == '{"error": "An error occurred (NoSuchBucket) when calling the ListObjects operation: The specified bucket does not exist"}'

    def test_unsolved_main_no_env_variable(self, s3_bucket_mock, api_gateway_event):
        response = unsolved.unsolved_puzzle_main()
        assert response['statusCode'] == 500
        assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert response['body'] == '{"error": "UNSOLVED_BUCKET_NAME environment variable not set correctly"}'

    def test_unsolved_main_bucket_does_not_exist(self, monkeypatch, s3_bucket_mock, api_gateway_event):
        monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'test-bucket2')
        response = unsolved.unsolved_puzzle_main()
        assert response['statusCode'] == 500
        assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        assert response['body'] == '{"error": "An error occurred (NoSuchBucket) when calling the ListObjects operation: The specified bucket does not exist"}'


def test_handler(monkeypatch, api_gateway_event, s3_bucket_mock):
    monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'test-bucket')
    response = unsolved.handler(api_gateway_event, None)
    assert response['statusCode'] == 200
    assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    assert re.match('{"level": .*}', response['body'])
