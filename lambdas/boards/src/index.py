import board_get_handler
import board_post_handler
import board_put_handler
import board_photo_post_handler
import board_photo_get_handler
import board_photo_put_handler
import http
import re
import copy

board_photo_regex = re.compile(r'.*/boards/[^/]*/photos/?$')
board_regex = re.compile(r'.*/boards/?[^/]*$')
def handler(event, context):
	print('received event:')
	print(event)
	base_response = {
			'headers': {
				'Access-Control-Allow-Headers': '*',
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
			},
			'body': "This method is not supported."
		}
	unsupported_method_response = copy.deepcopy(base_response)
	unsupported_method_response['statusCode'] = http.HTTPStatus.METHOD_NOT_ALLOWED

	bad_path_response = copy.deepcopy(base_response)
	bad_path_response['statusCode'] = http.HTTPStatus.BAD_REQUEST

	if board_photo_regex.match(event['path']):
		if event['httpMethod'] == 'POST':
			return board_photo_post_handler.handle(event, context)
		elif event['httpMethod'] == 'GET':
			return board_photo_get_handler.handle(event, context)
		elif event['httpMethod'] == 'PUT':
			return board_photo_put_handler.handle(event, context)
		else:
			return unsupported_method_response
	elif board_regex.match(event['path']):
		if event['httpMethod'] == 'GET':
			return board_get_handler.handle(event, context)
		elif event['httpMethod'] == 'POST':
			return board_post_handler.handle(event, context)
		elif event['httpMethod'] == 'PUT':
			return board_put_handler.handle(event, context)
		else:
			return unsupported_method_response
	else:
		return bad_path_response
