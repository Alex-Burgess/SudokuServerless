from apis import unsolved
import json
import re
import os



def test_handler_response(monkeypatch):
    monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'sudoku-unsolved-puzzles')
    response = unsolved.handler(api_gateway_event(), None)
    assert response['statusCode']  == 200

def test_generate_random_key():
    key = unsolved.generate_random_key()
    assert re.match('[1-9].json', key)

def test_get_bucket_name(monkeypatch):
    monkeypatch.setitem(os.environ, 'UNSOLVED_BUCKET_NAME', 'sudoku-unsolved-puzzles')
    name = unsolved.get_bucket_name()
    assert name == 'sudoku-unsolved-puzzles'


# TODO mock s3 call (moto)  Presumably if change name of bucket, the moto call will still work
def test_get_puzzle_from_s3(monkeypatch):
    puzzle_object = unsolved.get_puzzle_from_s3('sudoku-unsolved-puzzles', '1.json')
    test_object = {'level': 'easy','puzzle_rows': ["080064703","720503698","000002410","000007009","096308150","800100000","042800000","978605041","605470080"]}
    
    assert json.loads(puzzle_object) == test_object


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
    

# @pytest.fixture() TODO Maybe use this later
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
    