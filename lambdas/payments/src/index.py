import http
import re
import copy

import intent_post_handler
import payment_get_handler

payment_intent_regex = re.compile(r'.*/payments/intents/?$')
payment_regex = re.compile(r'.*/payments/?[^/]*$')
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

	if payment_intent_regex.match(event['path']):
		if event['httpMethod'] == 'POST':
			return intent_post_handler.handle(event, context)
		else:
			return unsupported_method_response
	elif payment_regex.match(event['path']):
		if event['httpMethod'] == 'GET':
			return payment_get_handler.handle(event, context)
		else:
			return unsupported_method_response
	else:
		return bad_path_response