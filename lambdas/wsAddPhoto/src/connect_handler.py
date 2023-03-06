import http
import queries
import uuid
import logging
import json

def handle(event, context):
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
		},
	}

	try:
		connection_id, join_code, cognito_username = _parse_args(event)
	except:
		logging.exception('Invalid arguments.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	board = queries.get_board(join_code)
	if not board:
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		response['body'] = 'No board with join code: ' + str(join_code)
		return response

	unauthorized_message = _validate_authorization(board, cognito_username)
	if unauthorized_message:
		response['statusCode'] = http.HTTPStatus.FORBIDDEN
		response['body'] = unauthorized_message
		return response

	return _create_connection(board, connection_id, response)


def _parse_args(event):
	connection_id = event['requestContext']['connectionId']
	join_code = uuid.UUID(event['queryStringParameters']['joinCode'])
	cognito_username = uuid.UUID(event['requestContext']['authorizer']['principalId'])
	return connection_id, join_code, cognito_username

def _validate_authorization(board, cognito_username):
	if board.owner_cognito_username != str(cognito_username):
		return 'Only the owner of this board can display it.'
	else:
		return None

def _create_connection(board, connection_id, response):
	queries.create_connection(board.board_id, connection_id)

	body = {
		'connectionId': connection_id
	}
	response['statusCode'] = http.HTTPStatus.OK
	response['body'] = json.dumps(body)
	return response