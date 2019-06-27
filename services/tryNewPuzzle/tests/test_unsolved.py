import json
import re
import os
import pytest
import boto3
from moto import mock_s3
from try_new_puzzle import unsolved

import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


def test_create_response():
    response = unsolved.create_response(200, 'Success message')

    expected_response = {'statusCode': 200,
                         'body': 'Success message',
                         'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                         }}
    assert response == expected_response, "Create_response did not return the expected response value."


def test_add_id_to_returned_json():
    input_puzzle_json = {
                            "level": "easy",
                            "puzzle_rows": [
                              [0, 8, 0, 0, 6, 4, 7, 0, 3],
                              [7, 2, 0, 5, 0, 3, 6, 9, 8],
                              [0, 0, 0, 0, 0, 2, 4, 1, 0],
                              [0, 0, 0, 0, 0, 7, 0, 0, 9],
                              [0, 9, 6, 3, 0, 8, 1, 5, 0],
                              [8, 0, 0, 1, 0, 0, 0, 0, 0],
                              [0, 4, 2, 8, 0, 0, 0, 0, 0],
                              [9, 7, 8, 6, 0, 5, 0, 4, 1],
                              [6, 0, 5, 4, 7, 0, 0, 8, 0]
                            ]
                        }

    exected_puzzle_json = {
                            "level": "easy",
                            "puzzle_rows": [
                              [0, 8, 0, 0, 6, 4, 7, 0, 3],
                              [7, 2, 0, 5, 0, 3, 6, 9, 8],
                              [0, 0, 0, 0, 0, 2, 4, 1, 0],
                              [0, 0, 0, 0, 0, 7, 0, 0, 9],
                              [0, 9, 6, 3, 0, 8, 1, 5, 0],
                              [8, 0, 0, 1, 0, 0, 0, 0, 0],
                              [0, 4, 2, 8, 0, 0, 0, 0, 0],
                              [9, 7, 8, 6, 0, 5, 0, 4, 1],
                              [6, 0, 5, 4, 7, 0, 0, 8, 0]
                            ],
                            "id": "1.json"
                        }

    output_data = unsolved.add_id_to_returned_json(json.dumps(input_puzzle_json), '1.json')
    assert output_data == json.dumps(exected_puzzle_json), "ID was not added to puzzle json object."

# handler

# get_unsolved_puzzle_main

# get_bucket_name
# get_random_key
# get_puzzle_from_s3
