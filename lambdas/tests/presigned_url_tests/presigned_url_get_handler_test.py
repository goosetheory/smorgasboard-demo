test_function_path = '../../presignedUrl/src'
lambda_layer_path = '../../common2/lib/python/lib/python3.8/site-packages'

import pytest
import sys, os
from moto import mock_s3
import boto3
from http import HTTPStatus
import json
import uuid

sys.path.append(os.getcwd() + '/..')

from .. import utils

sys.path.append(os.path.abspath(test_function_path))
sys.path.append(os.path.abspath(lambda_layer_path))

utils.init_env()
from .. import queries_for_testing


class TestPresignedUrlGetHandler:
	@classmethod
	def setup_class(cls):
		cls.person = queries_for_testing.create_person()
		cls.board = queries_for_testing.create_board(cls.person['cognito_username'])
		cls.active_photo = queries_for_testing.create_photo(cls.board['join_code'], photo_status_id=1)
		cls.inactive_photo = queries_for_testing.create_photo(cls.board['join_code'], photo_status_id=2)

	@classmethod
	def teardown_class(cls):
		queries_for_testing.teardown_person(cls.person['cognito_username'])

	@mock_s3
	def test_get_presigned_url_all_statuses_returns_all(self):
		import get_handler
		get_handler.s3_client = MP_S3Client()

		# ARRANGE
		event = {
			'requestContext': {
				'authorizer': {
					'claims': {
						'cognito:username': self.person['cognito_username']
					}
				}
			},
			'queryStringParameters': {
				'before-date': '2100-12-19T19:05:51.383Z', # Estimated heat death of universe
				'join-code': self.board['join_code'],
				'page-number': '0',
				'page-size': '2'
			},
			'multiValueQueryStringParameters': {
				'photo-status': [1, 2]
			}
		}

		# ACT
		response = get_handler.handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.OK
		body = json.loads(response['body'])
		photos = body['photos']
		assert len(photos) == 2


	@mock_s3
	def test_get_presigned_url_unspecified_status_returns_active_only(self):
		import get_handler
		get_handler.s3_client = MP_S3Client()

		# ARRANGE
		event = {
			'requestContext': {
				'authorizer': {
					'claims': {
						'cognito:username': self.person['cognito_username']
					}
				}
			},
			'queryStringParameters': {
				'before-date': '2100-12-19T19:05:51.383Z', # Estimated heat death of universe
				'join-code': self.board['join_code'],
				'page-number': '0',
				'page-size': '2'
			}
		}

		# ACT
		response = get_handler.handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.OK
		body = json.loads(response['body'])
		photos = body['photos']
		assert len(photos) == 1
		assert photos[0]['photoKey'] == self.active_photo['photo_key']




# A monkeypatched s3 client
class MP_S3Client:

	def generate_presigned_url(self, _):
		return 'testurl'


