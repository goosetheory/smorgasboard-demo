import uuid
import http
import json
import logging
import time

import queries
from s3_client import S3Client

s3_client = S3Client()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

NUM_RETRIES = 5
RETRY_DELAY_SECONDS = 0.5

def handle(event, context):
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
		},
	}

	try:
		photo_keys = _parse_args(event)
	except:
		logging.exception('Could not parse args from adjacent lambda function' + json.dumps(event))
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	return _get_photo_urls(photo_keys, response)

def _parse_args(event):
	return [uuid.UUID(key) for key in event['photoKeys']]

def _get_photo_urls(photo_keys, response):
	try:
		logger.info('Getting photo info...')
		photos = None
		retries_left = NUM_RETRIES
		while retries_left > 0:
			photos = queries.get_photos_by_key(photo_keys)
			if photos:
				break
			else:
				# This sucks. It's due to an issue I haven't been able to figure out
				# where a newly-inserted photo doesn't appear immediately.
				logger.warning('No photos found. Retrying...')
				retries_left -= 1
				time.sleep(RETRY_DELAY_SECONDS)

		if not photos:
			raise Exception('Could not find photos after max retries.')

		logger.info('Got photo info.')
		logger.info(f'Found {str(len(photos))} photos.')
		for photo in photos:
			photo.set_url(s3_client.generate_presigned_url(photo))
	except:
		logging.exception('Could not get photo urls.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		response['body'] = 'Could not get photo urls.'
		return response

	body = {
		'photos': [photo.to_dict() for photo in photos]
	}
	response['statusCode'] = http.HTTPStatus.OK
	response['body'] = json.dumps(body)
	return response
