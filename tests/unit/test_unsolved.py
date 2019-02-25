from apis import unsolved
import json
import re
import os

def api_gateway_event():
    return {
        'resource': '',
        'path': '',
        'httpMethod': '',
        'headers': {},
        'requestContext': {
            'resourcePath': '',
            'httpMethod': ''
        },
        "body": '{ "test": "body"}'
    }

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



# def test_handler_response_body():
#     response = unsolved.handler(api_gateway_event(), None)
    
#     {
#     "level": "hard",
#     "puzzle_rows": [
#         "000009300",
#         "074030000",
#         "300008079",
#         "000050200",
#         "710000096",
#         "006040000",
#         "630200005",
#         "000010820",
#         "008700000"
#     ]
# }
    
#     assert response['body'] == 'Puzzle data'
    




# TODO Maybe use this later
# @pytest.fixture()
# def api_gateway_event2():
#     """ Generates API GW Event"""

#     return {
#         "body": '{ "test": "body"}',
#         "resource": "/{proxy+}",
#         "requestContext": {
#             "resourceId": "123456",
#             "apiId": "1234567890",
#             "resourcePath": "/{proxy+}",
#             "httpMethod": "POST",
#             "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
#             "accountId": "123456789012",
#             "identity": {
#                 "apiKey": "",
#                 "userArn": "",
#                 "cognitoAuthenticationType": "",
#                 "caller": "",
#                 "userAgent": "Custom User Agent String",
#                 "user": "",
#                 "cognitoIdentityPoolId": "",
#                 "cognitoIdentityId": "",
#                 "cognitoAuthenticationProvider": "",
#                 "sourceIp": "127.0.0.1",
#                 "accountId": "",
#             },
#             "stage": "prod",
#         },
#         "queryStringParameters": {"foo": "bar"},
#         "headers": {
#             "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
#             "Accept-Language": "en-US,en;q=0.8",
#             "CloudFront-Is-Desktop-Viewer": "true",
#             "CloudFront-Is-SmartTV-Viewer": "false",
#             "CloudFront-Is-Mobile-Viewer": "false",
#             "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
#             "CloudFront-Viewer-Country": "US",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#             "Upgrade-Insecure-Requests": "1",
#             "X-Forwarded-Port": "443",
#             "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
#             "X-Forwarded-Proto": "https",
#             "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
#             "CloudFront-Is-Tablet-Viewer": "false",
#             "Cache-Control": "max-age=0",
#             "User-Agent": "Custom User Agent String",
#             "CloudFront-Forwarded-Proto": "https",
#             "Accept-Encoding": "gzip, deflate, sdch",
#         },
#         "pathParameters": {"proxy": "/examplepath"},
#         "httpMethod": "POST",
#         "stageVariables": {"baz": "qux"},
#         "path": "/examplepath",
#     }

    