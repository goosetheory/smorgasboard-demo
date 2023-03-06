import os
import boto3
import logging
import json

from botocore.exceptions import ClientError
from botocore.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SecretsClient:
	def __init__(self):
		self.stripe_info_secret_name = os.environ.get('ENV') + '/StripeInfo'
		self.region_name = os.environ.get('AWS_REGION')
		self.secrets_client = None

		self.stripe_info = None


	def get_stripe_api_key(self):
		return self._get_stripe_info()['stripe_api_key']


	def _get_stripe_info(self):
		if not self.stripe_info:
			self.stripe_info = self._get_secret(self.stripe_info_secret_name)
		return self.stripe_info

	def _get_secret(self, secret_name):
		logger.info(f'Attempting to get secret {secret_name}')
		client = self._get_secrets_client()
		try:
			get_secret_value_response = client.get_secret_value(SecretId=secret_name)
		except ClientError as e:
			logging.exception(f'Error getting secret {secret_name}.')
			raise e
		else:
			secret = get_secret_value_response['SecretString']
			logger.info(f'Successfully retrieved secret {secret_name}.')
			return json.loads(secret)


	def _get_secrets_client(self):
		if not self.secrets_client:
			self.secrets_client = boto3.client(
							service_name='secretsmanager',
							region_name=self.region_name
							)
		return self.secrets_client
