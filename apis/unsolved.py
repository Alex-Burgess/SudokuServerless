import json
import os
import boto3
import random

s3_client = boto3.client('s3')

def handler(event, context):
    key = generate_random_key()
    bucket = get_bucket_name()
    
    puzzle_data = get_puzzle_from_s3(bucket, key)

    return {'statusCode': 200,
            'body': puzzle_data,
            'headers': {'Content-Type': 'application/json'}}


def generate_random_key():
    # TODO - get maximum number of puzzles in bucket
    # TODO - s3 role should least permissions, right now it has all permissons
    random_key = str(random.randint(1, 8)) + '.json'
    return random_key

def get_bucket_name():
    bucket_name = os.environ['UNSOLVED_BUCKET_NAME']
    return bucket_name

def get_puzzle_from_s3(bucket, key):
    s3 = boto3.resource('s3')
    #print("DEBUG: Getting S3 object (" + key + ") from bucket (" + bucket_name +")")
    
    obj = s3.Object(bucket, key)
    puzzle_data = obj.get()['Body'].read().decode('utf-8')
    #print ("DEBUG: Puzzle object: " + puzzle_data)
    
    return puzzle_data

