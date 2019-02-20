import json
import os
import boto3
import random

s3_client = boto3.client('s3')

def handler(event, context):
    # TODO Add checks to validate that was a json object and was a sudoku puzzle
    unsolved_puzzle = json.dumps(event, indent=2)

    solved_puzzle = get_solved_puzzle(unsolved_puzzle)
    
    data = {
        'output': 'Puzzle successfully solved.',
        'Solved Puzzle': solved_puzzle
    }
    
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
            

def get_solved_puzzle(puzzle_input):
    print("DEBUG: Unsolved puzzle: " + puzzle_input)
    
    # TODO: Solved puzzle logic goes here. Lambda layer?  Main logic doesn't need to be here.
    
    solved_puzzle = {
        'puzzle_rows': [
            "581964723",
            "724513698",
            "369782415",
            "413257869",
            "296348157",
            "857196234",
            "142839576",
            "978625341",
            "635471982"
        ]
    }
    
    print("DEBUG: Solved puzzle: " + json.dumps(solved_puzzle))
    
    return solved_puzzle


# def get_puzzle_from_s3():
#     s3 = boto3.resource('s3')
#     bucket_name = os.environ['UNSOLVED_BUCKET_NAME']

#     # TODO - get maximum number of puzzles in bucket
#     # TODO - s3 role should least permissions, right now it has all permissons
#     random_key = str(random.randint(1, 8)) + '.json'
#     print ('DEBUG: Puzzle Key: ' + str(random_key))
    
#     print("DEBUG: Getting S3 object (" + random_key + ") from bucket (" + bucket_name +")")
#     obj = s3.Object(bucket_name, random_key)
#     puzzle_data = obj.get()['Body'].read().decode('utf-8')
#     print ("DEBUG: Puzzle object: " + puzzle_data)
    
#     return puzzle_data

