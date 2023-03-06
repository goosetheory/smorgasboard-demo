import http
import logging

import other_lambda_handler

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
	print('received event:')
	print(event)
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
	}

	if 'httpMethod' not in event: # This call comes from another lambda function
		return other_lambda_handler.handle(event, context)
	else:
		logger.info('Cannot handle event type')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		response['body'] = 'Cannot handle event type'
		return response