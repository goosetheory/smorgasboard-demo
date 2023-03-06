import http
import logging
import json

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()

def handle(event, context):
	response = {
		'statusCode': http.HTTPStatus.OK,
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

	logger.info(f'Received ping from {connection_id}')
	return response

def _parse_args(event):
	connection_id = event['requestContext']['connectionId']
	return connection_id