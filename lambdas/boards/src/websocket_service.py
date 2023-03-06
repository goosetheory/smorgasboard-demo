import http
import uuid
import boto3
import json
import botocore.exceptions
import logging
from collections import defaultdict

import queries
from secrets_client import SecretsClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class WebsocketService:
	def __init__(self):
		self.secrets_client = SecretsClient()
		self.lambda_client = boto3.client('lambda')
		self.gateway_client = None

	def remove_photo_from_clients(self, join_code, photo_key):
		try:
			logger.info(f'WS: pushing removal of photo {photo_key} from board {join_code} to clients')
			active_connection_ids = queries.get_connections_for_board(join_code)
			self._send_removed_photo_websocket_message_to_clients(photo_key, active_connection_ids)
		except:
			logging.exception(f'Error removing photo key {str(photo_key)} from clients of {str(join_code)}.')


	def push_photo_to_clients(self, join_code, photo_key):
		try:
			logger.info(f'WS: pushing new photo {str(photo_key)} to clients')
			active_connection_ids = queries.get_connections_for_board(join_code)
			self._send_new_photo_websocket_message_to_clients(photo_key, active_connection_ids)
		except:
			logging.exception(f'Error pushing photo key {str(photo_key)} to clients of {str(join_code)}.')


	def _send_new_photo_websocket_message_to_clients(self, photo_key, connection_ids):
		photo = self._get_photo_with_presigned_urls(photo_key)
		if not photo:
			return

		for connection_id in connection_ids:
			body = {
				'action': 'newPhotos',
				'photos': [photo]
			}
			self._send_websocket_message_to_client(body, connection_id)


	def _send_removed_photo_websocket_message_to_clients(self, photo_key, connection_ids):
		body = {
			'action': 'removePhotos',
			'photoKeys': [str(photo_key)]
		}

		for connection_id in connection_ids:
			self._send_websocket_message_to_client(body, connection_id)


	def _send_websocket_message_to_client(self, body, connection_id):
		body_str = json.dumps(body)
		try:
			gateway_client = self._get_gateway_client()
			gateway_client.post_to_connection(ConnectionId=connection_id, Data=body_str.encode('utf-8'))
			logger.info('sent websocket message to ' + str(connection_id) + ': ' + body_str)
		except gateway_client.exceptions.GoneException:
			logging.exception('GoneException trying to callback to client')
		except Exception:
			logging.exception('Non-GoneException error when trying to callback to client')


	def _get_gateway_client(self):
		if not self.gateway_client:
			ws_url = self.secrets_client.get_websocket_url()
			self.gateway_client = boto3.client('apigatewaymanagementapi', endpoint_url=ws_url)
		return self.gateway_client


	def _get_photo_with_presigned_urls(self, photo_key):
		try:
			payload = {
				'photoKeys': [str(photo_key)]
			}
			presigned_url_function_name = self.secrets_client.get_presigned_url_function_name()
			response = self.lambda_client.invoke(
				FunctionName = presigned_url_function_name,
				InvocationType = 'RequestResponse',
				Payload = json.dumps(payload)
			)

			response_payload = json.load(response['Payload'])
			logger.info('response from presignedUrl lambda: ' + json.dumps(response_payload))
			if (response['ResponseMetadata']['HTTPStatusCode'] != http.HTTPStatus.OK
				or 'statusCode' not in response_payload.keys()
				or response_payload['statusCode'] != http.HTTPStatus.OK):
				logger.error('Absent or non-200 status code from presignedUrl lambda.')
				return None

			photos = json.loads(response_payload['body'])['photos']
			if not photos:
				logger.warning('No photos returned by presignedUrl lambda.')
				return None

			return photos[0]
		except:
			logging.exception('Error invoking presignedUrl lambda.')
			return None