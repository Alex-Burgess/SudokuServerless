from apis import unsolved
import json
import re
import os
import pytest
import boto3
from moto import mock_s3

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
@mock_s3
def setup_moto_s3_bucket():
    '''Creates an s3 bucket, with 1 puzzle in it and returns the bucket.  Tearsdown the moto s3 bucket as well'''
    
    bucketName = 'sudoku-test-bucket'
    upload_filename = '../../example_puzzles/1.json' 
    key = '1.json'
    
    s3 = boto3.resource('s3')
    
    s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    s3.meta.client.upload_file(upload_filename, bucketName, key)

    yield "setup_moto_s3_bucket"
    
    bucket = s3.Bucket(bucketName)
    for key in bucket.objects.all():
            key.delete()
    bucket.delete()


# TODO - this fails now, because we don't have any logic to limit the random number generation to the number of puzzles in the bucket
def test_handler_response(setup_moto_s3_bucket, api_gateway_event, monkeypatch):
    monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'sudoku-test-bucket')
    response = unsolved.handler(api_gateway_event, None)
    print (json.dumps(response))
    assert response['statusCode']  == 200

def test_generate_random_key():
    key = unsolved.generate_random_key()
    assert re.match('[1-9].json', key)

def test_get_bucket_name(monkeypatch):
    monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'sudoku-unsolved-puzzles')
    name = unsolved.get_bucket_name()
    assert name == 'sudoku-unsolved-puzzles'


def test_get_puzzle_from_s3(setup_moto_s3_bucket):
    puzzle_object = unsolved.get_puzzle_from_s3('sudoku-test-bucket', '1.json')
    test_object = {'level': 'easy','puzzle_rows': ["080064703","720503698","000002410","000007009","096308150","800100000","042800000","978605041","605470080"]}
    assert json.loads(puzzle_object) == test_object


# TODO Assert that the get puzzle method returns a not found error.  handle exceptions.
# def test_get_puzzle_from_s3_not_found(setup_moto_s3_bucket):
#     puzzle_object = unsolved.get_puzzle_from_s3('sudoku-test-bucket', '2.json')
#     test_object = {'level': 'easy','puzzle_rows': ["080064703","720503698","000002410","000007009","096308150","800100000","042800000","978605041","605470080"]}
#     assert json.loads(puzzle_object) == test_object

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
    