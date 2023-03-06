import http
import boto3
import logging
import json

from secrets_client import SecretsClient
from email_type import EmailType

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class LambdaClient:
	def __init__(self):
		self.secrets_client = SecretsClient()
		self.lambda_client = boto3.client('lambda')

	def send_join_email(self, cognito_username):
		try:
			payload = {
				'emailType': EmailType.ON_JOIN.value,
				'cognitoUsername': str(cognito_username)
			}

			logger.info(f'Sending join email')
			send_email_function_name = self.secrets_client.get_send_email_function_name()
			response = self.lambda_client.invoke(
				FunctionName = send_email_function_name,
				InvocationType = 'RequestResponse',
				Payload = json.dumps(payload)
			)
			response_payload = json.load(response['Payload'])
			logger.info('response from sendEmail lambda: ' + json.dumps(response_payload))

			if (response['ResponseMetadata']['HTTPStatusCode'] != http.HTTPStatus.OK
				or 'statusCode' not in response_payload.keys()
				or response_payload['statusCode'] != http.HTTPStatus.OK):
				logger.error('Absent or non-200 status code from sendEmail lambda.')
				return False

			logger.info('Successfully sent join email.')
			return True

		except:
			logging.exception('Error invoking sendEmail lambda')
			return False