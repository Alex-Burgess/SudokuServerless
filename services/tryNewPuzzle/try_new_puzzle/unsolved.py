import json
import os
import boto3
import random

s3_client = boto3.client('s3')
# TODO - s3 role should least permissions, right now it has all permissons
# TODO - logging

def handler(event, context):
    try:
        bucket_name = get_bucket_name()
        key = get_random_key(bucket_name)
        puzzle_data = get_puzzle_from_s3(bucket_name, key)

        return {'statusCode': 200,
                'body': puzzle_data,
                'headers': {'Content-Type': 'application/json'}}
    except Exception as e:
        print(e)
        return {'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
                'headers': {'Content-Type': 'application/json'}}

def get_bucket_name():
    try:
        bucket_name = os.environ['UNSOLVED_BUCKET_NAME']
    except:
        raise Exception('UNSOLVED_BUCKET_NAME environment variable not set correctly')

    return bucket_name


def get_random_key(bucket_name):
    print("DEBUG: bucket name " + bucket_name)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    number_of_puzzles = 0
    for key in bucket.objects.all():
        number_of_puzzles += 1

    print("DEBUG: total number of puzzles " + str(number_of_puzzles))

    random_key = str(random.randint(1, number_of_puzzles)) + '.json'
    return random_key


def get_puzzle_from_s3(bucket, key):
    s3 = boto3.resource('s3')
    # print("DEBUG: Getting S3 object (" + key + ") from bucket (" + bucket_name +")")

    obj = s3.Object(bucket, key)
    puzzle_data = obj.get()['Body'].read().decode('utf-8')
    # print ("DEBUG: Puzzle object: " + puzzle_data)

    return puzzle_data
