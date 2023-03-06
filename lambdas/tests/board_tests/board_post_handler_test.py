test_function_path = '../../boards/src'
lambda_layer_path = '../../common2/lib/python/lib/python3.8/site-packages'

import pytest
import sys, os
import boto3, moto
from http import HTTPStatus
import json
import uuid

sys.path.append(os.getcwd() + '/..')

from .. import utils

sys.path.append(os.path.abspath(test_function_path))
sys.path.append(os.path.abspath(lambda_layer_path))

utils.init_env()
import board_post_handler
import board_get_handler
from .. import queries_for_testing

class TestBoardPostHandler:
	@classmethod
	def setup_class(cls):
		cls.person = queries_for_testing.create_person()
		queries_for_testing.create_payment(cls.person['cognito_username'])

	@classmethod
	def teardown_class(cls):
		queries_for_testing.delete_all_payments_for_user(cls.person['cognito_username'])
		queries_for_testing.delete_all_boards_for_user(cls.person['cognito_username'])
		queries_for_testing.delete_person(cls.person['cognito_username'])

	def test_create_board_authenticated(self):
		# ARRANGE
		test_board_name = 'Test Board Name'
		test_board_type = 2 # Standard
		request_body = {
			'boardName': test_board_name,
			'boardType': test_board_type
		}
		event = {
			'body': json.dumps(request_body),
			'requestContext': {
				'authorizer': {
					'claims': {
						'cognito:username': self.person['cognito_username']
					}
				}
			}
		}

		# ACT
		response = board_post_handler.handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.OK
		post_response_body = json.loads(response['body'])
		assert post_response_body['boardName'] == test_board_name

		# Verify board created
		get_handler_request = {
			'queryStringParameters': {
				'joinCode': post_response_body['joinCode']
			}
		}
		get_response = board_get_handler.handle(get_handler_request, None)
		assert get_response['statusCode'] == HTTPStatus.OK

		get_body = json.loads(response['body'])
		assert get_body['boardName'] == test_board_name
		assert get_body['joinCode'] == post_response_body['joinCode']
		assert get_body['boardType'] == test_board_type
		assert get_body['startDateTimestamp'] == None
		assert get_body['endDateTimestamp'] == None
		assert get_body['boardStatus'] is not None