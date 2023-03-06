from datetime import datetime
from datetime import timedelta
import pymysql
import json
import logging
import http
import re
import uuid

import queries
from board import Board
from board_status import BoardStatus
from board_type import BoardType

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BOARD_DURATION_HOURS = 48
TRIAL_DURATION_HOURS = 2

def handle(event, context):
	'''Expected path: /board/<join_code>
	Expected body:
	{
		boardStatus: <int>
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
		join_code, new_board_status = _parse_args(event)
		logging.info('parsed args')
	except:
		logging.exception('Could not parse args for PUT request.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	try:
		board = queries.get_board_by_join_code(join_code)
		if not board:
			logger.error(f'Board with join code {join_code} does not exist.')
			response['statusCode'] = http.HTTPStatus.BAD_REQUEST
			return response
		logger.info('found board')
	except:
		logging.exception('Get board query failed.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		return response

	try:
		unauthorized_message = _validate_authorization(cognito_username, join_code)
		if unauthorized_message:
			logger.error(f'user {cognito_username} is unauthorized to update board {join_code}')
			response['statusCode'] = http.HTTPStatus.FORBIDDEN
			response['body'] = unauthorized_message
			return response
		else:
			_update_board(board, new_board_status)
			logger.info('updated board')
	except:
		logging.exception('Could not update board.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		return response

	try:
		updated_board = queries.update_board(board)
		response['statusCode'] = http.HTTPStatus.OK
		response['body'] = json.dumps(updated_board.to_dict())
		logger.info('fetched board to return')
	except:
		logging.exception('Could get updated board.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
	return response


def _update_board(board, new_board_status):
	'''Applies limited updates to board. If starting the board, include end date.'''
	if board.board_status == BoardStatus.NOT_STARTED and new_board_status == BoardStatus.ACTIVE:
		board.board_status = BoardStatus.ACTIVE
		board.start_date = datetime.now()
		board_duration = TRIAL_DURATION_HOURS if board.board_type == BoardType.FREE_TRIAL else BOARD_DURATION_HOURS
		board.end_date = board.start_date + timedelta(hours=board_duration)


def _parse_args(event):
	body = json.loads(event['body'])

	if 'boardStatus' in body:
		new_board_status = BoardStatus(int(body['boardStatus']))
	else:
		new_board_status = None

	uuid_regex = re.compile('.*/boards/([^/]*)') # matches '.../boards/<uuid>', capturing <uuid>
	path = event['path']
	uuid_path_component = uuid_regex.match(path).group(1)
	join_code = str(uuid.UUID(uuid_path_component))

	return join_code, new_board_status


def _validate_authorization(cognito_username, join_code):
	board_owner_cognito_username = queries.get_board_owner_username(join_code)
	if not board_owner_cognito_username:
		return 'That board was not found.'
	elif board_owner_cognito_username != str(cognito_username):
		return 'You must be the board owner to update it.'
	else:
		return None
