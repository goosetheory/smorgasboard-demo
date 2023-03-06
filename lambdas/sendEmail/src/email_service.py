import logging
import boto3
import os

from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class EmailService:
	def __init__(self):
		region_name = os.environ.get('AWS_REGION')
		self.email_client = boto3.client('ses', region_name=region_name)
		self.charset = 'UTF-8'
		self.sender_address = 'no-reply@smorgasboard.io'

	def send(self, email):
		# Returns true on success
		try:
			response = self.email_client.send_email(
				Destination={
					'ToAddresses': [
						email.recipient,
					],
				},
				Message={
					'Body': {
						'Html': {
							'Charset': self.charset,
							'Data': email.body_html,
						},
						'Text': {
							'Charset': self.charset,
							'Data': email.body_text,
						},
					},
					'Subject': {
						'Charset': self.charset,
						'Data': email.subject,
					},
				},
				Source=self.sender_address,
			)
		except ClientError as e:
			logging.exception('ClientError. Could not send mail.')
			logging.error(e.response['Error']['Message'])
			return
		except:
			logging.exception('Could not send mail.')
			return
		else:
			logging.info(f'Email sent to {str(email.recipient)}. Message ID: {str(response["MessageId"])}')
			email.set_message_id(response["MessageId"])
			email.sent = True
