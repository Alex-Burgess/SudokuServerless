import json
import os
import boto3
import random

s3_client = boto3.client('s3')

def handler(event, context):
	response = {
		'statusCode': 200,
		'body': json.dumps('Hello Python')
	}
	return response

# def handler(event, context):
#     puzzle_data = get_puzzle_from_s3()

#     return {'statusCode': 200,
#             'body': puzzle_data,
#             'headers': {'Content-Type': 'application/json'}}



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

