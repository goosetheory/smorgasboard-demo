import http
import logging

import connect_handler
import disconnect_handler
import ping_handler

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def handler(event, context):
	print('received event:')
	print(event)

	response = {
			'headers': {
				'Access-Control-Allow-Headers': '*',
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
			}
		}

	route_key = event.get('requestContext', {}).get('routeKey')
	if not route_key:
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		response['body'] = 'Expected event.requestContext.routeKey but none found'
		return response

	if route_key == '$connect':
		return connect_handler.handle(event, context)
	elif route_key == '$disconnect':
		return disconnect_handler.handle(event, context)
	elif route_key == 'ping':
		return ping_handler.handle(event, context)
	else:
		logger.error('Route key not recognized: ' + str(route_key))
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		response['body'] = 'Unrecognized route key'
		return response