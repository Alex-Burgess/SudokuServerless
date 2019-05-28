import json

def handler(event, context):
    msg = 'Hello World!'
    
    return msg


# Take in json object and load into dictionary
# https://stackoverflow.com/questions/42640163/json-into-a-list-of-lists-python
# import json
# with open('test.json') as f:
#     d = json.load(f)
#     print [row.values() for row in d]