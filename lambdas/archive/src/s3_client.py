import os
import boto3
import logging
import json

from botocore.exceptions import ClientError
from botocore.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SECONDS_IN_A_WEEK = 604800

class S3Client:
	def __init__(self):
		self.s3_creds_secret_name = os.environ.get('ENV') + '/S3Creds'
		self.s3_bucket_secret_name = os.environ.get('ENV') + '/S3BucketInfo'
		self.region_name = os.environ.get('AWS_REGION')

		self.secrets_client = None
		self.s3_client = None
		self.s3_creds = None
		self.bucket_name = None

	def eager_init(self):
		self._get_secrets_client()
		self._get_s3_client()

	def get_object(self, s3_bucket_name, s3_photo_key):
		s3_client = self._get_s3_client()
		photo = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_photo_key)
		result = photo['Body'].read()
		return result

	def put_file(self, filename, file_content):
		logger.info(f'Uploading file {filename} to s3')
		s3_client = self._get_s3_client()
		s3_client.put_object(Bucket=self.get_bucket_name(), Key=filename, Body=file_content)

	def get_presigned_url(self, s3_bucket_name, s3_object_key, expiry_seconds=SECONDS_IN_A_WEEK):
		s3_client = self._get_s3_client()
		return s3_client.generate_presigned_url('get_object',
										Params={
											'Bucket': s3_bucket_name,
											'Key': s3_object_key},
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
			self.s3_client = self._create_s3_client()
			logger.info('s3 client created.')
		return self.s3_client

	def _create_s3_client(self):
		if not self.s3_creds:
			self.s3_creds = self._get_secret(self.s3_creds_secret_name)
		config = Config(signature_version='s3v4', connect_timeout=5, retries={'max_attempts': 0})
		session = boto3.session.Session()
		s3_client = session.client("s3", config=config,
							region_name=self.region_name,
							aws_access_key_id=self.s3_creds['aws_access_key_id'],
							aws_secret_access_key=self.s3_creds['aws_secret_access_key'])
		return s3_client
