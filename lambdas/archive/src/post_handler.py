import json
import logging
import http
import uuid
import io
import zipfile
import os
import boto3

from botocore.exceptions import ClientError
from botocore.config import Config

import queries
import get_handler
from compression_leader import CompressionLeader
from s3_client import S3Client

s3_client = S3Client()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Number of photos in an archive shard
SHARD_SIZE = 256

def handle(event, context):
	'''Expected body:
	{
		joinCode: string
	}'''
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
	}

	try:
		cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
	except:
		logger.error(f'Could not find cognito username from event {str(event)}')
		response['statusCode'] = http.HTTPStatus.UNAUTHORIZED
		return response

	try:
		join_code = _parse_args(event)
	except:
		logging.exception('No join code found on request.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	unauthorized_message = _validate_authorization(cognito_username, join_code)
	if unauthorized_message:
		response['statusCode'] = http.HTTPStatus.FORBIDDEN
		response['body'] = unauthorized_message
		return response

	try:
		return create_archive(join_code, response)
	except:
		logging.exception('Failed to create archive.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		return response


def create_archive(join_code, response):
	if queries.does_archive_exist(join_code):
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		response['body'] = 'Archive already exists.'
		return response

	logger.info(f'Creating archive for join code {str(join_code)}')

	# Get all photo ids
	photos_to_process = queries.get_photo_retrieval_info(join_code)

	shard_filenames = []

	# Divide into N batches. Foreach:
	leader = CompressionLeader()
	logger.info(f'Starting to zip files. {str(len(photos_to_process))} photos to zip.')
	while photos_to_process:
		photos_in_shard = photos_to_process[:SHARD_SIZE]
		photos_to_process = photos_to_process[SHARD_SIZE:]

		# Compress photos
		shard_filename = leader.compress_shard(photos_in_shard)
		shard_filenames.append(shard_filename)

	# Create archive in DB
	bucket_name = s3_client.get_bucket_name()
	logger.info('Creating archive in DB...')
	queries.create_archive(join_code, bucket_name, shard_filenames)
	logger.info('Archive created.')

	# Get archive and return
	return get_handler.get_archive(join_code, response)


def _parse_args(event):
	body = json.loads(event['body'])
	join_code = uuid.UUID(body['joinCode'])
	return join_code



def _validate_authorization(cognito_username, join_code):
	board_owner_username = queries.get_board_owner_username(join_code)
	if board_owner_username != cognito_username:
		return 'Only the owner of this board can create an archive.'
	else:
		return None


