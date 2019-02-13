import json

def handler(event, context):
    data = {
        'output': 'Unsolved puzzle returned.',
        'level': 'easy',
        'puzzle': '[123456789,123456789,123456789,123456789...]'
    }

    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}


# def handler(event, context):
#     inputNumber = event['pathParameters']['number']

#     result = do_function_logic(inputNumber)
#     data = json_output(result)

#     return {'statusCode': 200,
#             'body': json.dumps(data),
#             'headers': {'Content-Type': 'application/json'}}

# def do_function_logic(number):
#     result = 5 + int(number)
    
#     return result

# def json_output(number):
#     data = {
#         'output': 'Numbers added to url were: ' + str(number),
#         'timestamp': datetime.datetime.utcnow().isoformat()
#     }
    
#     return data