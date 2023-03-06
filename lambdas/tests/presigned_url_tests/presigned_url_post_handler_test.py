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

class TestPresignedUrlPostHandler:
	@classmethod
	def setup_class(cls):
		cls.person = queries_for_testing.create_person()
		cls.active_board = queries_for_testing.create_board(cls.person['cognito_username'], board_status_id=1) # Active board
		cls.inactive_board = queries_for_testing.create_board(cls.person['cognito_username'], board_status_id=2) # Inactive board
		cls.free_trial_board = queries_for_testing.create_board(cls.person['cognito_username'], board_status_id=1, board_type_id=1) # Active free trial board
		cls.free_trial_photo = queries_for_testing.create_photo(cls.free_trial_board['join_code'])

	@classmethod
	def teardown_class(cls):
		queries_for_testing.teardown_person(cls.person['cognito_username'])

	@mock_s3
	def test_can_create_upload_link(self):
		# ARRANGE
		import post_handler
		post_handler.s3_client = MP_S3Client()

		request_body = {
			'fileExtension': 'jpg',
			'joinCode': self.active_board['join_code']
		}

		event = {
			'body': json.dumps(request_body)
		}

		# ACT
		response = post_handler.handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.OK

		response_body = json.loads(response['body'])
		assert response_body['url'] == 'testurl'
		assert response_body['fields'] == 'testfields'
		assert response_body['s3BucketName'] == 'testbucketname'
		assert response_body['s3ObjectKey'] is not None
		assert response_body['photoKey'] is not None

	@mock_s3
	def test_upload_to_inactive_board_fails(self):
		# ARRANGE
		import post_handler
		post_handler.s3_client = MP_S3Client()

		request_body = {
			'fileExtension': 'jpg',
			'joinCode': self.inactive_board['join_code']
		}

		event = {
			'body': json.dumps(request_body)
		}

		# ACT
		response = post_handler.handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.CONFLICT

		response_body = json.loads(response['body'])
		assert 'That board is inactive' in response_body['error']


	@mock_s3
	def test_upload_to_full_trial_board_fails(self):
		# ARRANGE
		import post_handler
		post_handler.s3_client = MP_S3Client()
		post_handler.FREE_TRIAL_PHOTO_LIMIT = 1

		request_body = {
			'fileExtension': 'jpg',
			'joinCode': self.free_trial_board['join_code']
		}

		event = {
			'body': json.dumps(request_body)
		}

		# ACT
		response = post_handler.handle(event, None)

		# ASSERT
		assert response['statusCode'] == HTTPStatus.CONFLICT

		response_body = json.loads(response['body'])
		assert 'free trial limit' in response_body['error']


# A monkeypatched s3 client
class MP_S3Client:

	def generate_presigned_post(self, _):
		return {
			'url': 'testurl',
			'fields': 'testfields'
		}

	def get_bucket_name(self):
		return 'testbucketname'