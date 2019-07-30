import json
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.handlers:
    handler = logger.handlers[0]
    handler.setFormatter(logging.Formatter("[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(module)s:%(funcName)s\t%(message)s\n", "%Y-%m-%dT%H:%M:%S"))


s3_client = boto3.client('s3')


def handler(event, context):
    response = solution_main(event)
    return response


def solution_main(event):
    try:
        bucket_name = get_bucket_name()
        puzzle_id = get_puzzle_id_from_path(event)
        puzzle_data = get_puzzle_from_s3(bucket_name, puzzle_id)
    except Exception as e:
        logger.error("Exception: {}".format(e))
        response = create_response(500, json.dumps({'error': str(e)}))
        logger.info("Returning response: {}".format(response))
        return response

    message = prepare_puzzle_data(puzzle_data)
    response = create_response(200, message)
    logger.info("Returning response: {}".format(response))

    return response


def get_puzzle_id_from_path(event):
    logger.info("Getting puzzle ID from the path in API Gateway event.")

    try:
        puzzle_id = event['pathParameters']['id']
        logger.info("ID path parameter contained value: " + puzzle_id)
    except KeyError:
        logger.error('No id path parameter was provided.')
        raise Exception('No id path parameter was provided.')

    return puzzle_id


def get_bucket_name():
    try:
        bucket_name = os.environ['SOLVED_BUCKET_NAME']
        logger.info("SOLVED_BUCKET_NAME environment variable value: " + bucket_name)
    except KeyError:
        logger.error('SOLVED_BUCKET_NAME environment variable not set correctly')
        raise Exception('SOLVED_BUCKET_NAME environment variable not set correctly')

    return bucket_name


def get_puzzle_from_s3(bucket, key):
    s3 = boto3.resource('s3')
    logger.info("Getting S3 object (" + key + ") from bucket (" + bucket + ")")

    obj = s3.Object(bucket, key)
    puzzle_data = obj.get()['Body'].read().decode('utf-8')
    logger.info("Puzzle object: " + puzzle_data)

    return puzzle_data


def create_response(code, message):
    logger.info("Creating response with status code ({}) and message ({})".format(code, message))
    response = {'statusCode': code,
                'body': message,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }}
    return response


def prepare_puzzle_data(puzzle_data):
    return_data = json.loads(puzzle_data)
    return json.dumps(return_data)
