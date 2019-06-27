import json
import os
import boto3
import random
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logger.handlers[0]
handler.setFormatter(logging.Formatter("[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(module)s:%(funcName)s\t%(message)s\n", "%Y-%m-%dT%H:%M:%S"))

s3_client = boto3.client('s3')


def handler(event, context):
    response = get_unsolved_puzzle_main()
    return response


def get_unsolved_puzzle_main():
    try:
        bucket_name = get_bucket_name()
        key = get_random_key(bucket_name)
        puzzle_data = get_puzzle_from_s3(bucket_name, key)

        # puzzle_data = get_random_key(bucket_name)
    except Exception as e:
        logger.error("Exception: {}".format(e))
        response = create_response(500, json.dumps({'error': str(e)}))
        return response

    return_data = add_id_to_returned_json(puzzle_data, key)
    response = create_response(200, return_data)

    logger.info("Returning response: {}".format(response))
    return response


def add_id_to_returned_json(puzzle_json, id):
    logger.info("Adding id ({}) to puzzle json object ({})".format(id, puzzle_json))
    complete_json = json.loads(puzzle_json)
    complete_json['id'] = id
    return json.dumps(complete_json)


def create_response(code, message):
    logger.info("Creating response with status code ({}) and message ({})".format(code, message))
    response = {'statusCode': code,
                'body': message,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}
    return response


def get_bucket_name():
    try:
        bucket_name = os.environ['UNSOLVED_BUCKET_NAME']
        logger.info("UNSOLVED_BUCKET_NAME environment variable value: " + bucket_name)
    except KeyError:
        logger.error('UNSOLVED_BUCKET_NAME environment variable not set correctly')
        raise Exception('UNSOLVED_BUCKET_NAME environment variable not set correctly')

    return bucket_name


def get_random_key(bucket_name):
    logger.info("Getting s3 bucket object for bucket ({}).".format(bucket_name))
    s3 = boto3.resource('s3')
    try:
        bucket = s3.Bucket(bucket_name)
    except Exception as e:
        logger.error("Could not get bucket object: {}".format(e))
        raise

    number_of_puzzles = 0
    for key in bucket.objects.all():
        number_of_puzzles += 1

    logger.info("Total number of puzzles in bucket ({}): {}".format(bucket_name, number_of_puzzles))

    random_key = str(random.randint(1, number_of_puzzles)) + '.json'

    logger.info("Random puzzle object: {}".format(random_key))
    return random_key


def get_puzzle_from_s3(bucket, key):
    s3 = boto3.resource('s3')
    logger.info("Getting S3 object (" + key + ") from bucket (" + bucket + ")")

    obj = s3.Object(bucket, key)
    puzzle_data = obj.get()['Body'].read().decode('utf-8')
    logger.info("Puzzle object: " + puzzle_data)

    return puzzle_data
