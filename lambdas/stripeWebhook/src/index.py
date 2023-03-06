import json
import http
import stripe
import logging

import queries
from secrets_client import SecretsClient
from lambda_client import LambdaClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

secrets_client = SecretsClient()
lambda_client = LambdaClient()
stripe.api_key = secrets_client.get_stripe_api_key()

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

	try:
		event_body = json.loads(event['body'])
		stripe_event = stripe.Event.construct_from(event_body, stripe.api_key)
		logger.info(f'Stripe event type: {stripe_event.type}')
	except ValueError as e:
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response


	if stripe_event.type == 'payment_intent.succeeded':
		logger.info(f'Marking payment {stripe_event.data.object.id} succeeded.')
		try:
			queries.mark_payment_successful(stripe_event.data.object.id)
			logger.info(f'Updated payment {stripe_event.data.object.id} successfully.')
		except:
			logging.exception('Could not mark payment successful in db.')
			response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
			return response

		try:
			cognito_username = queries.get_cognito_username_of_payer(stripe_event.data.object.id)
			lambda_client.send_purchase_email(cognito_username)
			logger.info('Sent purchase email')
		except:
			logging.exception('Could not send email to user for purchase.')
			response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
			return response
	else:
		logger.error(f'Unrecognized stripe event type: {stripe_event.type}')

	response['statusCode'] = http.HTTPStatus.OK
	return response
