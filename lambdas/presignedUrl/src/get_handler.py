import pymysql
import json
import logging
import http
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from datetime import datetime
import uuid
import dateutil.parser

import queries
from s3_client import S3Client
from board_photo_status import BoardPhotoStatus

s3_client = S3Client()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle(event, context):
	''' possible inputs:
		/presigned-urls?join-code=<uuid>&page-number=<int>&page-size=<int>&before-date=<date>&photo-status=1&photo-status=2
		/presigned-urls?join-code=<uuid>&photo-key=<uuid>
	'''
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
		},
	}

	try:
		cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
	except:
		logger.error('Could not find cognito username from event: ' + str(event))
		response['statusCode'] = http.HTTPStatus.UNAUTHORIZED
		return response

	try:
		logger.info('Parsing args')
		args = _parse_args(event)
	except:
		logging.exception('Invalid arguments.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	try:
		unauthorized_message = _validate_authorization(cognito_username, args.join_code)
		if unauthorized_message:
			logger.error('Unauthorized: ' + unauthorized_message)
			response['statusCode'] = http.HTTPStatus.FORBIDDEN
			response['body'] = json.dumps({'error': unauthorized_message})
			return response
	except:
		logging.exception('Could not verify user was board owner.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	if args.photo_keys:
		return _get_photo_urls_for_photo_keys(args, response)
	else:
		return _get_photo_urls_for_page(args, response)

def _get_photo_urls_for_page(args, response):
	try:
		photos = queries.get_photos_for_board(args.join_code, args.page_number, args.page_size, args.before_date, args.photo_statuses)
		return _get_photo_urls_from_s3(photos, response)
	except:
		logging.exception('Could not get photo urls.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		response['body'] = 'Could not get photo urls.'
		return response

def _get_photo_urls_for_photo_keys(args, response):
	try:
		photos = queries.get_photos_by_key_and_join_code(args.join_code, args.photo_keys)
		return _get_photo_urls_from_s3(photos, response)
	except:
		logging.exception('Could not get photo urls.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		response['body'] = 'Could not get photo urls.'
		return response

def _get_photo_urls_from_s3(photos, response):
	for photo in photos:
		photo.set_url(s3_client.generate_presigned_url(photo))
	body = {
		'photos': [photo.to_dict() for photo in photos]
	}
	response['statusCode'] = http.HTTPStatus.OK
	response['body'] = json.dumps(body)
	return response

def _parse_args(event):
	'''If there are any photo codes, use those; otherwise, use pagination'''

	join_code = uuid.UUID(event['queryStringParameters']['join-code'])
	if event.get('multiValueQueryStringParameters', {}).get('photo-key'):
		photo_keys = event.get('multiValueQueryStringParameters', {}).get('photo-key')
		return Args.from_photo_keys(join_code, photo_keys)
	else:
		page_number = int(event['queryStringParameters']['page-number'])
		page_size = int(event['queryStringParameters']['page-size'])
		before_date = dateutil.parser.isoparse(event['queryStringParameters']['before-date'])
		photo_status_ids = event.get('multiValueQueryStringParameters', {}).get('photo-status')
		if photo_status_ids:
			photo_statuses = [BoardPhotoStatus(int(status)) for status in photo_status_ids]
		else:
			photo_statuses = [BoardPhotoStatus.ACTIVE]
		return Args.from_page(join_code, page_number, page_size, before_date, photo_statuses)


def _validate_authorization(cognito_username, join_code):
	board_owner_cognito_username = queries.get_board_owner_username(join_code)
	if not board_owner_cognito_username:
		return 'That board was not found.'
	elif board_owner_cognito_username != str(cognito_username):
		return 'You must be the board owner to view its photos.'
	else:
		return None

class Args:
	def __init__(self, join_code=None, page_number=None, page_size=None, before_date=None, photo_keys=None, photo_statuses=[]):
		self.join_code = join_code
		self.page_number = page_number
		self.page_size = page_size
		self.before_date = before_date
		self.photo_keys = photo_keys
		self.photo_statuses = photo_statuses

	@classmethod
	def from_page(cls, join_code, page_number, page_size, before_date, photo_statuses):
		return cls(join_code=join_code, page_number=page_number, page_size=page_size, before_date=before_date, photo_statuses=photo_statuses)

	@classmethod
	def from_photo_keys(cls, join_code, photo_keys):
		return cls(join_code=join_code, photo_keys=photo_keys)


