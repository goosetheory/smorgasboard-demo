import json
import logging
import http
import uuid
import re

import queries
from board_photo_status import BoardPhotoStatus
from websocket_service import WebsocketService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

websocket_service = WebsocketService()

def handle(event, context):
	'''Expected body:
	{
		photoKey: string, (a uuid)
		boardPhotoStatus: int
	}
	'''
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
		photo_key, join_code, board_photo_status = _parse_args(event)
	except:
		logging.exception('Invalid arguments.')
		json.dumps({'error': 'Invalid arguments.'})
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	try:
		unauthorized_message = _validate_authorization(cognito_username, join_code)
		if unauthorized_message:
			response['statusCode'] = http.HTTPStatus.FORBIDDEN
			response['body'] = json.dumps({'error': unauthorized_message})
			return response
	except:
		logging.exception('Could not verify user was board owner.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		response['body'] = json.dumps({'error': 'Could not verify user was board owner.'})
		return response

	try:
		queries.set_board_photo_status(photo_key, join_code, board_photo_status)
	except:
		logging.exception('Failed to update photo.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		response['body'] = json.dumps({'error': 'Could not apply update.'})
		return response

	try:
		_send_websocket_messages(join_code, photo_key, board_photo_status)
	except:
		logging.exception('Could not send message to websocket clients.')

	response['statusCode'] = http.HTTPStatus.OK
	return response



def _parse_args(event):
	body = json.loads(event['body'])
	photo_key = uuid.UUID(body['photoKey'])
	board_photo_status = BoardPhotoStatus(int(body['boardPhotoStatus']))

	uuid_regex = re.compile('.*/boards/([^/]*)/photos') # matches '/boards/<uuid>/photos', capturing <uuid>
	path = event['path']
	uuid_path_component = uuid_regex.match(path).group(1)
	join_code = str(uuid.UUID(uuid_path_component))

	return photo_key, join_code, board_photo_status


def _validate_authorization(cognito_username, join_code):
	board_owner_cognito_username = queries.get_board_owner_username(join_code)
	if not board_owner_cognito_username:
		return 'That board was not found.'
	elif board_owner_cognito_username != str(cognito_username):
		return 'You must be the board owner to manage its photos.'
	else:
		return None

def _send_websocket_messages(join_code, photo_key, board_photo_status):
	if board_photo_status == BoardPhotoStatus.ACTIVE:
		logger.info(f'Pushing out photo with key {str(photo_key)} to clients')
		websocket_service.push_photo_to_clients(join_code, photo_key)
	elif board_photo_status == BoardPhotoStatus.REMOVED_BY_HOST:
		logger.info(f'Removing photo with key {str(photo_key)} from clients')
		websocket_service.remove_photo_from_clients(join_code, photo_key)
	else:
		raise Exception('Unrecognized board photo status.')
