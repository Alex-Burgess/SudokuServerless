import json
import os
import boto3


s3_client = boto3.client('s3')
# TODO - s3 role should least permissions, right now it has all permissons
# TODO - logging


def handler(event, context):
    # puzzle_id = event['pathParameters']['id']
    print("DEBUG: Incomming event: {}".format(event))

    try:
        puzzle_id = event['pathParameters']['id']
    except Exception as e:
        print(e)
        return {'statusCode': 500,
                'body': json.dumps({'error': str(e), 'message': 'Event did not contain pathParameters with puzzle json file.'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}

    try:
        bucket_name = get_bucket_name()
        key = puzzle_id
        puzzle_data = get_puzzle_from_s3(bucket_name, key)

        return {'statusCode': 200,
                'body': puzzle_data,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}
    except Exception as e:
        print(e)
        return {'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}


def get_bucket_name():
    try:
        bucket_name = os.environ['SOLUTIONS_BUCKET_NAME']
    except KeyError:
        raise Exception('SOLUTIONS_BUCKET_NAME environment variable not set correctly')

    return bucket_name


def get_puzzle_from_s3(bucket, key):
    s3 = boto3.resource('s3')
    # logging print("DEBUG: Getting S3 object (" + key + ") from bucket (" + bucket_name +")")

    obj = s3.Object(bucket, key)
    puzzle_data = obj.get()['Body'].read().decode('utf-8')
    # logging print ("DEBUG: Puzzle object: " + puzzle_data)

    return puzzle_data
