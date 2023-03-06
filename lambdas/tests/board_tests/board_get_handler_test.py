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
from board_get_handler import handle
from .. import queries_for_testing


class TestBoardGetHandler:
	@classmethod
	def setup_class(cls):
		cls.person = queries_for_testing.create_person()
		cls.board = queries_for_testing.create_board(cls.person['cognito_username'])

	@classmethod
	def teardown_class(cls):
		queries_for_testing.delete_board(cls.board['join_code'])
		queries_for_testing.delete_person(cls.person['cognito_username'])

	def test_get_extant_board_authenticated(self):
		# ARRANGE
		event = {
			'requestContext': {
				'authorizer': {
					'claims': {
						'cognito:username': self.person['cognito_username']
					}
				}
			}
		}

		# ACT
		response = handle(event, None)

		#ASSERT
		assert response['statusCode'] == HTTPStatus.OK
		body = json.loads(response['body'])
		assert len(body) == 1

		returned_board = body[0]
		assert returned_board['boardName'] == self.board['board_name']
		assert returned_board['joinCode'] == self.board['join_code']
		assert returned_board['startDateTimestamp'] == None
		assert returned_board['endDateTimestamp'] == None
		assert returned_board['boardStatus'] is not None


	def test_get_extant_board_unauthenticated(self):
		#ARRANGE
		event = {
			'queryStringParameters': {
				'joinCode': self.board['join_code']
			}
		}

		# ACT
		response = handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.OK
		body = json.loads(response['body'])

		assert body['boardName'] == self.board['board_name']
		assert body['joinCode'] == self.board['join_code']
		assert body['startDateTimestamp'] == None
		assert body['endDateTimestamp'] == None
		assert body['boardStatus'] is not None

	def test_get_board_no_username_no_code_error(self):
		# ARRANGE
		event = {}

		# ACT
		response = handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.BAD_REQUEST


	def test_get_board_nonexistant_code(self):
		# ARRANGE
		event = {
			'queryStringParameters': {
				'joinCode': str(uuid.uuid4()) # Technically nondeterministic but like cmon
			}
		}

		# ACT
		response = handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.BAD_REQUEST
