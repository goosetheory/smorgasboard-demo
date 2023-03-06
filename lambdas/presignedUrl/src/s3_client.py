import os
import boto3
import logging
import json

from botocore.exceptions import ClientError
from botocore.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class S3Client:
	def __init__(self):
		self.s3_creds_secret_name = os.environ.get('ENV') + '/S3Creds'
		self.s3_bucket_secret_name = os.environ.get('ENV') + '/S3BucketInfo'
		self.region_name = os.environ.get('AWS_REGION')

		self.secrets_client = None
		self.s3_client = None
		self.bucket_name = None


	def generate_presigned_post(self, object_name):
		expiry_seconds = 300
		s3_client = self._get_s3_client()
		bucket_name = self.get_bucket_name()
		return s3_client.generate_presigned_post(Bucket=bucket_name,
												 Key=object_name,
												 ExpiresIn=expiry_seconds)


	def generate_presigned_url(self, photo):
		expiry_seconds = 3600
		s3_client = self._get_s3_client()
		return s3_client.generate_presigned_url('get_object',
										Params={
											'Bucket': photo.s3_bucket_name,
											'Key': photo.s3_object_key},
										ExpiresIn=expiry_seconds)

	def get_bucket_name(self):
		if not self.bucket_name:
			bucket_name_secret = self._get_secret(self.s3_bucket_secret_name)
			self.bucket_name = bucket_name_secret['photo_bucket_name']
		return self.bucket_name


	def _get_secrets_client(self):
		if not self.secrets_client:
			self.secrets_client = boto3.client(
							service_name='secretsmanager',
							region_name=self.region_name
							)
		return self.secrets_client


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


	def _get_s3_client(self):
		if not self.s3_client:
			logger.info('Creating s3 client...')
			s3_creds = self._get_secret(self.s3_creds_secret_name)
			self.s3_client = boto3.client("s3", config=Config(signature_version='s3v4'),
								region_name=self.region_name,
								aws_access_key_id=s3_creds['aws_access_key_id'],
								aws_secret_access_key=s3_creds['aws_secret_access_key'])
			logger.info("s3 client created.")
		return self.s3_client
