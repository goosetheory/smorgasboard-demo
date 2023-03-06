import http
import uuid

import post_handler

def handle(event, context):
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
		},
	}

	try:
		join_code = _parse_args(event)
	except:
		logging.exception('Could not get join code from adjacent lambda function'  + json.dumps(event))
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	return post_handler.create_archive(join_code, response)


def _parse_args(event):
	return uuid.UUID(event['joinCode'])