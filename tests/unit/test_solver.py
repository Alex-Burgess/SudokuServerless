from puzzle import solver

def test_handler():
    message = solver.handler("", "")
    
    assert message == "Hello World!"


# def test_lambda_handler(apigw_event, mocker):

#     requests_response_mock = namedtuple("response", ["text"])
#     requests_response_mock.text = "1.1.1.1\n"

#     request_mock = mocker.patch.object(
#         app.requests, 'get', side_effect=requests_response_mock)

#     ret = app.lambda_handler(apigw_event, "")
#     assert ret["statusCode"] == 200

#     for key in ("message", "location"):
#         assert key in ret["body"]

#     data = json.loads(ret["body"])
#     assert data["message"] == "hello world"
