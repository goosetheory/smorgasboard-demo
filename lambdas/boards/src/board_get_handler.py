import json
import logging
import http
import uuid

import queries

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle(event, context):
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
	}

	try:
		cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
		logger.info(f'Username: {cognito_username}')
	except:
		logger.info('No username.')
		cognito_username = None

	try:
		join_code = _parse_args(event)
		logger.info(f'Join code: {str(join_code)}')
	except:
		logging.exception('Could not parse args.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	if not join_code:
		if not cognito_username:
			response['statusCode'] = http.HTTPStatus.BAD_REQUEST
			response['body'] = 'Anonymous users must include a board\'s join code.'
			return response
		try:
			boards = queries.get_boards_for_user(cognito_username)
			json_boards = [board.to_dict() for board in boards]
			response['statusCode'] = http.HTTPStatus.OK
			response['body'] = json.dumps(json_boards)
			return response
		except Exception:
			logging.exception('Error getting boards')
			response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
			response['body'] = 'Could not get board info.'
			return response
	else:
		try:
			board = queries.get_board_by_join_code(join_code)
			if board:
				response['body'] = json.dumps(board.to_dict())
				response['statusCode'] = http.HTTPStatus.OK
				return response
			else:
				response['body'] = 'Could not find board with that join code.'
				response['statusCode'] = http.HTTPStatus.BAD_REQUEST
				return response
		except Exception as e:
			logging.exception('Error getting board')
			response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
			response['body'] = 'Could not get board info.'
			return response

def _parse_args(event):
	params = event.get('queryStringParameters')
	if not params or params == 'None':
		return None

	join_code = params.get('joinCode')
	if not join_code:
		return None

	return uuid.UUID(join_code)
