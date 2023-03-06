import json
import logging
import http

import queries
from payment_status import PaymentStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle(event, context):
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
	}

	try:
		cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
	except:
		logger.error('Could not find cognito username from event: ' + str(event))
		response['statusCode'] = http.HTTPStatus.UNAUTHORIZED
		return response

	try:
		payment_status = _parse_args(event)
	except:
		logging.exception('No payment status found.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	try:
		payments = queries.get_payments_for_user_and_status(cognito_username, payment_status)
	except:
		logging.exception('Could not execute query.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		return response

	response['body'] = json.dumps([payment.to_dict() for payment in payments])
	response['statusCode'] = http.HTTPStatus.OK
	return response


def _parse_args(event):
	payment_status = PaymentStatus(int(event['queryStringParameters']['paymentStatus']))
	return payment_status

