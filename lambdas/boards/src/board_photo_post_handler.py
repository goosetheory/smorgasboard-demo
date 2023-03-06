import json
import logging
import http
import uuid
import re

import queries
from board_membership_status import BoardMembershipStatus
from websocket_service import WebsocketService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

websocket_service = WebsocketService()

def handle(event, context):
	'''Expected body:
	{
		photoKey: string, (a uuid)
		s3BucketName: string,
		s3ObjectKey: string
	}
	'''
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
		'statusCode': http.HTTPStatus.OK
	}

	try:
		cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
	except:
		cognito_username = None

	try:
		photo_key, s3_bucket_name, s3_object_key, join_code = _parse_args(event)
	except:
		logging.exception('Invalid arguments.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	response = _create_board_photo_map(cognito_username,
								   photo_key,
								   s3_bucket_name,
								   s3_object_key,
								   join_code,
								   response)

	if response['statusCode'] == http.HTTPStatus.OK:
		websocket_service.push_photo_to_clients(join_code, photo_key)

	return response


def _parse_args(event):
	body = json.loads(event['body'])
	photo_key = body['photoKey']
	s3_bucket_name = body['s3BucketName']
	s3_object_key = body['s3ObjectKey']

	uuid_regex = re.compile('.*/boards/([^/]*)/photos') # matches '/boards/<uuid>/photos', capturing <uuid>
	path = event['path']
	uuid_path_component = uuid_regex.match(path).group(1)
	join_code = str(uuid.UUID(uuid_path_component))

	return photo_key, s3_bucket_name, s3_object_key, join_code


def _create_board_photo_map(cognito_username,
							photo_key,
							s3_bucket_name,
							s3_object_key,
							join_code,
							response):
	try:
		queries.create_photo_for_board(cognito_username,
									   photo_key,
									   s3_bucket_name,
									   s3_object_key,
									   join_code,
									   BoardMembershipStatus.ACTIVE)
	except:
		logging.exception('Could not create board photo map.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
	finally:
		return response
