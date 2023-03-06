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
		self.email_info_secret_name = os.environ.get('ENV') + '/SendEmailInfo'
		self.region_name = os.environ.get('AWS_REGION')
		self.secrets_client = None

		self.stripe_info = None
		self.send_email_function_name = None


	def get_send_email_function_name(self):
		if not self.send_email_function_name:
			secret = self._get_secret(self.email_info_secret_name)
			self.send_email_function_name = secret['send_email_function_name']
		return self.send_email_function_name

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
