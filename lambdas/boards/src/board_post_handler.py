from datetime import datetime
import pymysql
import json
import logging
import http

import queries
from board_status import BoardStatus
from payment_status import PaymentStatus
from board_type import BoardType

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle(event, context):
	'''Expected body:
	{
		boardName: string,
		boardType: int
	}
	'''

	try:
		cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
	except:
		logging.exception('Could not find cognito username from event: ' + str(event))
		response = _get_response()
		response['statusCode'] = http.HTTPStatus.UNAUTHORIZED
		return response

	try:
		board_name, board_type = _parse_args(event)
	except:
		logging.exception('Could not parse args to to create board.')
		response = _get_response()
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	if board_type == BoardType.STANDARD:
		return _handle_create_standard_board(cognito_username, board_name)
	elif board_type == BoardType.FREE_TRIAL:
		return _handle_create_free_trial_board(cognito_username, board_name)
	else:
		logger.error(f'No such board type: {str(board_type)}')
		response = _get_response()
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response


def _handle_create_free_trial_board(cognito_username, board_name):
	logger.info(f'Creating free trial board for user (username: {str(cognito_username)}, board_name: {board_name})')
	return _create_board(cognito_username, board_name, BoardType.FREE_TRIAL)


def _handle_create_standard_board(cognito_username, board_name):
	response = _get_response()
	logger.info(f'Creating standard board for user (username: {str(cognito_username)}, board_name: {board_name})')
	try:
		payment_id = queries.get_first_succeeded_payment_id_for_user(cognito_username)
		if not payment_id:
			logger.error(f'Could not create board for {str(cognito_username)}. No available payment.')
			response['body'] = 'Unable to create board - your payment has not been processed.'
			response['statusCode'] = http.HTTPStatus.PAYMENT_REQUIRED
			return response
		else:
			queries.update_payment_status(payment_id, PaymentStatus.CONSUMED)
	except:
		logging.exception('Could not find or update payment info.')
		response = _get_response()
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		return response

	return _create_board(cognito_username, board_name, BoardType.STANDARD)


def _create_board(cognito_username, board_name, board_type):
	response = _get_response()
	try:
		created_board = queries.create_board(cognito_username, board_name, BoardStatus.NOT_STARTED, board_type)

		if created_board:
			response['body'] = json.dumps(created_board.to_dict())
			response['statusCode'] = http.HTTPStatus.OK
			return response
		else:
			raise Exception('Create board failed.')

	except Exception as e:
		logging.exception('Error creating board')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		response['body'] = 'Could not create board.'
	finally:
		return response


def _get_response():
	return {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
	}

def _parse_args(event):
	body = json.loads(event['body'])
	board_name = body['boardName']
	board_type = BoardType(int(body['boardType']))
	return board_name, board_type



