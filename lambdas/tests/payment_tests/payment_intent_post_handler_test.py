test_function_path = '../../payments/src'
common_lambda_layer_path = '../../common2/lib/python/lib/python3.8/site-packages'
stripe_lambda_layer_path = '../../stripelayer/lib/python/lib/python3.8/site-packages'


import pytest
import sys, os
import boto3, moto
from http import HTTPStatus
import json
import uuid

sys.path.append(os.path.abspath('..'))

from .. import utils

sys.path.append(os.path.abspath(test_function_path))
sys.path.append(os.path.abspath(common_lambda_layer_path))
sys.path.append(os.path.abspath(stripe_lambda_layer_path))

utils.init_env()
from intent_post_handler import handle
from .. import queries_for_testing


class TestPaymentIntentPostHandler:
	@classmethod
	def setup_class(cls):
		cls.person = queries_for_testing.create_person()

	@classmethod
	def teardown_class(cls):
		queries_for_testing.delete_all_payments_for_user(cls.person['cognito_username'])
		queries_for_testing.delete_person(cls.person['cognito_username'])


	def test_create_payment_intent_logged_in(self):
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

		# ASSERT
		assert response['statusCode'] == HTTPStatus.OK
		body = json.loads(response['body'])
		print(body)

		assert body['amount'] == 7900
		assert body['currency'] == 'usd'
		assert body.get('client_secret') is not None
