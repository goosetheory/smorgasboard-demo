import http
import queries
import logging

def handle(event, context):
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
		},
	}

	try:
		connection_id = _parse_args(event)
	except:
		logging.exception('Invalid arguments.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	queries.disconnect_connection(connection_id)
	response['statusCode'] = http.HTTPStatus.OK
	return response


def _parse_args(event):
	connection_id = event['requestContext']['connectionId']
	return connection_id