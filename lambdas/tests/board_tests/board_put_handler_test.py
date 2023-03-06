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
import board_put_handler
import board_get_handler
from .. import queries_for_testing

class TestBoardPutHandler:
	@classmethod
	def setup_class(cls):
		cls.person = queries_for_testing.create_person()
		cls.other_person = queries_for_testing.create_person()
		cls.board = queries_for_testing.create_board(cls.person['cognito_username'])

	@classmethod
	def teardown_class(cls):
		queries_for_testing.delete_all_boards_for_user(cls.person['cognito_username'])
		queries_for_testing.delete_all_boards_for_user(cls.other_person['cognito_username'])
		queries_for_testing.delete_person(cls.person['cognito_username'])
		queries_for_testing.delete_person(cls.other_person['cognito_username'])

	def test_update_board_status_to_active_authenticated_succeeds(self):
		# ARRANGE
		request_body = {
			'boardStatus': 1 # ACTIVE
		}
		event = {
			'body': json.dumps(request_body),
			'path': f'/boards/{self.board["join_code"]}',
			'requestContext': {
				'authorizer': {
					'claims': {
						'cognito:username': self.person['cognito_username']
					}
				}
			}
		}

		# ACT
		response = board_put_handler.handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.OK
		put_body = json.loads(response['body'])
		assert put_body['boardName'] == self.board['board_name']
		assert put_body['joinCode'] == self.board['join_code']
		assert put_body['startDateTimestamp'] is not None
		assert put_body['endDateTimestamp'] is not None
		assert put_body['boardStatus'] == 1 # ACTIVE

		# Verify board updated
		get_handler_request = {
			'queryStringParameters': {
				'joinCode': self.board['join_code']
			}
		}
		get_response = board_get_handler.handle(get_handler_request, None)
		assert get_response['statusCode'] == HTTPStatus.OK

		get_body = json.loads(response['body'])
		assert get_body['boardName'] == self.board['board_name']
		assert get_body['joinCode'] == self.board['join_code']
		assert get_body['startDateTimestamp'] is not None
		assert get_body['endDateTimestamp'] is not None
		assert get_body['boardStatus'] == 1 # ACTIVE

	def test_update_board_status_to_active_not_authorized_fails(self):
		# ARRANGE
		request_body = {
			'boardStatus': 1 # ACTIVE
		}
		event = {
			'body': json.dumps(request_body),
			'path': f'/boards/{self.board["join_code"]}',
			'requestContext': {
				'authorizer': {
					'claims': {
						'cognito:username': self.other_person['cognito_username']
					}
				}
			}
		}

		# ACT
		response = board_put_handler.handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.FORBIDDEN
