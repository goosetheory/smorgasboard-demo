import json
import logging
import http
import uuid
import re

import queries

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle(event, context):
	'''Returns photo info for all photos on board, but no presigned urls.
		Call: /boards/<join-code>/photos'''
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
		logging.exception('Could not find cognito username from event: ' + str(event))
		response['statusCode'] = http.HTTPStatus.UNAUTHORIZED
		return response

	try:
		join_code = _parse_args(event)
	except:
		logging.exception('Invalid arguments.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	try:
		unauthorized_message = _validate_authorization(cognito_username, join_code)
		if unauthorized_message:
			response['statusCode'] = http.HTTPStatus.FORBIDDEN
			response['body'] = unauthorized_message
			return response
	except:
		logging.exception('Could not verify user was board owner.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	try:
		photo_keys = queries.get_photos_for_board(join_code)
	except:
		logging.exception('Failed to retrieve photo keys.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		response['body'] = 'Could not retrieve photo keys for board.'
		return response

	body = {
		'photoKeys': photo_keys
	}
	response['statusCode'] = http.HTTPStatus.OK
	response['body'] = json.dumps(body)
	return response


def _parse_args(event):
	uuid_regex = re.compile('.*/boards/([^/]*)/photos') # matches '/boards/<uuid>/photos', capturing <uuid>
	path = event['path']
	uuid_path_component = uuid_regex.match(path).group(1)
	join_code = uuid.UUID(uuid_path_component)
	return join_code

def _validate_authorization(cognito_username, join_code):
	board_owner_cognito_username = queries.get_board_owner_username(join_code)
	if not board_owner_cognito_username:
		return 'That board was not found.'
	elif board_owner_cognito_username != str(cognito_username):
		return 'You must be the board owner to view its photos.'
	else:
		return None
