import http
import boto3
import logging
import json

import queries
from secrets_client import SecretsClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

secrets_client = SecretsClient()
ws_url = secrets_client.get_websocket_url()
gateway_client = boto3.client('apigatewaymanagementapi', endpoint_url=ws_url)

def handler(event, context):
	print('received event:')
	print(event)
	response = {
		'statusCode': http.HTTPStatus.OK,
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
		},
		'body': 'Success'
	}

	open_connections = queries.get_open_connections()

	logger.info(f'There are currently {str(len(open_connections))} connections.')

	connections_to_close = []
	for connection in open_connections:
		try:
			body = {
				'action': 'ping'
			}
			gateway_client.post_to_connection(Data=json.dumps(body), ConnectionId=connection.ws_connection_id)
		except gateway_client.exceptions.GoneException:
			connections_to_close.append(connection)
		except:
			logging.exception('Could not post to connection.')

	logger.info(f'Closing {str(len(connections_to_close))} connections.')

	if connections_to_close:
		queries.mark_connections_closed(connections_to_close)

	return response
