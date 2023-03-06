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
from board_photo_put_handler import handle
from .. import queries_for_testing


class TestBoardPhotoPutHandler:
	@classmethod
	def setup_class(cls):
		cls.person = queries_for_testing.create_person()
		cls.board = queries_for_testing.create_board(cls.person['cognito_username'])
		cls.photo = queries_for_testing.create_photo(cls.board['join_code'], photo_status_id=1)


	@classmethod
	def teardown_class(cls):
		queries_for_testing.teardown_person(cls.person['cognito_username'])


	def test_update_photo_status(self):
		# ARRANGE
		request_body = {
			'photoKey': self.photo['photo_key'],
			'boardPhotoStatus': '2'
		}
		event = {
			'path': f'/boards/{self.board["join_code"]}/photos',
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
		response = handle(event, None)

		#ASSERT
		assert response['statusCode'] == HTTPStatus.OK

		found_bpm = queries_for_testing.get_board_photo_map(self.board['join_code'], self.photo['photo_key'])
		assert found_bpm['status_id'] == 2