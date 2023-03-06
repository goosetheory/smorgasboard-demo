import pymysql
import json
import logging
import http
import boto3
import uuid

import queries
from board import Board
from board_status import BoardStatus
from board_type import BoardType
from s3_client import S3Client

s3_client = S3Client()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

FREE_TRIAL_PHOTO_LIMIT = 20

def handle(event, context):
	'''Expected body:
	{
		fileExtension: string,
		joinCode: string
	}
	'''
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
		},
	}

	try:
		file_extension, join_code = _parse_args(event)
	except:
		logging.exception('Invalid arguments.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	try:
		cannot_upload_to_board_message = _validate_can_upload_to_board(join_code)
		if cannot_upload_to_board_message:
			logger.error(f'Cannot upload to board: {cannot_upload_to_board_message}')
			response['statusCode'] = http.HTTPStatus.CONFLICT
			response['body'] = json.dumps({'error': cannot_upload_to_board_message})
			return response
	except:
		logging.exception('Exception checking whether board could be uploaded to.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		return response


	new_photo_key = uuid.uuid4()
	new_filename = _generate_new_filename(new_photo_key, file_extension)
	try:
		logger.info(f'Creating upload link for new filename: {new_filename}')
		body = _create_presigned_post(new_filename, response)
		body['s3BucketName'] = s3_client.get_bucket_name()
		body['s3ObjectKey'] = new_filename
		body['photoKey'] = str(new_photo_key)
		response['statusCode'] = http.HTTPStatus.OK
		response['body'] = json.dumps(body)
		return response
	except:
		logging.exception('Could not generate presigned post.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		response['body'] = 'Unable to generate upload url.'
		return response

def _parse_args(event):
	body = json.loads(event['body'])
	file_extension = body['fileExtension']
	join_code = uuid.UUID(body['joinCode'])
	return file_extension, join_code


def _validate_can_upload_to_board(join_code):
	board = queries.get_board_by_join_code(join_code)
	if not board:
		return 'That board could not be found.'
	if board.board_status is not BoardStatus.ACTIVE:
		return 'That board is inactive.'
	if board.board_type == BoardType.FREE_TRIAL:
		board_photo_count = queries.get_board_photos_count(join_code)
		if board_photo_count >= FREE_TRIAL_PHOTO_LIMIT:
			return 'You have reached the free trial limit on photo uploads.'
	return None


def _generate_new_filename(new_uuid, file_extension):
	if file_extension:
		new_filename = f'{new_uuid}.{file_extension}'
	else:
		new_filename = str(new_uuid)
	return new_filename


def _create_presigned_post(new_filename, response):
	presigned_post = s3_client.generate_presigned_post(new_filename)
	presigned_post_body = {
		'url': presigned_post['url'],
		'fields': presigned_post['fields']
	}
	return presigned_post_body
