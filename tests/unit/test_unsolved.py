import json
import re
import os
import pytest
import boto3
from moto import mock_s3
from apis import unsolved

bucket_name = 'mytestbucket'
example_puzzles_path = '/home/ec2-user/environment/SudokuServerless/example_puzzles'

@pytest.fixture()
def api_gateway_event():
    return {
        "resource": "/unsolvedPuzzle",
        "path": "/unsolvedPuzzle",
        "httpMethod": "GET",
        "headers": "null",
        "multiValueHeaders": "null",
        "queryStringParameters": "null",
        "multiValueQueryStringParameters": "null",
        "pathParameters": "null",
        "stageVariables": "null",
        "requestContext": {
            "path": "/unsolvedPuzzle",
            "accountId": "123456789012",
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
            "resourcePath": "/unsolvedPuzzle",
            "httpMethod": "GET",
            "apiId": "1234567890"
        },
        "body": "null",
        "isBase64Encoded": "false"
    }


@pytest.fixture
def s3_bucket_mock(monkeypatch):
    monkeypatch.setitem(os.environ, 'AWS_SECRET_ACCESS_KEY', 'foobar_secret')
    monkeypatch.setitem(os.environ, 'AWS_ACCESS_KEY_ID', 'foobar_key')
    
    # setup: start moto server and create the bucket
    mock = mock_s3()
    mock.start()
    # Create Bucket so that test can run
    s3 = boto3.resource('s3', region_name='eu-west-1')
    s3.create_bucket(Bucket=bucket_name)
    
    # Add file for testing
    upload_filename = example_puzzles_path + '/1.json' 
    key = '1.json'
    s3.meta.client.upload_file(upload_filename, bucket_name, key)
    
    upload_filename = example_puzzles_path + '/2.json' 
    key = '2.json'
    s3.meta.client.upload_file(upload_filename, bucket_name, key)
    
    upload_filename = example_puzzles_path + '/3.json' 
    key = '3.json'
    s3.meta.client.upload_file(upload_filename, bucket_name, key)
    
    yield
    # teardown: stop moto server
    mock.stop()


def test_get_bucket_name(monkeypatch):
    monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', bucket_name)
    name = unsolved.get_bucket_name()
    assert name == bucket_name


def test_get_random_key2(s3_bucket_mock):
    key = unsolved.get_random_key(bucket_name)
    assert re.match('[1-9].json', key)
    

def test_get_puzzle_from_s3(s3_bucket_mock):
    puzzle_object = unsolved.get_puzzle_from_s3(bucket_name, '1.json')
    test_object = {'level': 'easy','puzzle_rows': ["080064703","720503698","000002410","000007009","096308150","800100000","042800000","978605041","605470080"]}
    assert json.loads(puzzle_object) == test_object


# TODO Assert that the get puzzle method returns a not found error.  handle exceptions.
# def test_get_puzzle_from_s3_not_found(s3_bucket_with_one_file):
#     puzzle_object = unsolved.get_puzzle_from_s3('sudoku-test-bucket', '2.json')
#     test_object = {'level': 'easy','puzzle_rows': ["080064703","720503698","000002410","000007009","096308150","800100000","042800000","978605041","605470080"]}
#     assert json.loads(puzzle_object) == test_object


# # TODO - this fails now, because we don't have any logic to limit the random number generation to the number of puzzles in the bucket
# def test_handler_response(s3_bucket_with_one_file, bucket_name, api_gateway_event, monkeypatch):
#     monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', bucket_name)
#     response = unsolved.handler(api_gateway_event, None)
#     print (json.dumps(response))
#     assert response['statusCode']  == 200

# TODO mock s3 call for bucket and key
# def test_handler_response_body():  Needs to be mocked
#     response = unsolved.handler(api_gateway_event(), None)
    
#     {
#     "level": "easy",
#     "puzzle_rows": [
#         "000010820",
#         "008700000"
#     ]
# }
    
#     assert response['body'] == 'Puzzle data'



# TODO - Integration test calling the API, which calls the lambda function.
    