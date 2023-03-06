import stripe
import logging
import http
import json

import queries
from secrets_client import SecretsClient
from coupon_handler import CouponHandler, InvalidCouponError, CouponUsedError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BOARD_COST_PENNIES = 7900 # Stripe expects pennies

coupon_handler = CouponHandler()
secrets_client = SecretsClient()
stripe.api_key = secrets_client.get_stripe_api_key()

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
		logger.error(f'Could not find cognito username from event {str(event)}')
		response['statusCode'] = http.HTTPStatus.UNAUTHORIZED
		return response

	coupon_code = _parse_args(event)
	price = BOARD_COST_PENNIES
	if coupon_code:
		try:
			logger.info(f'Handling coupon code {coupon_code}')
			price = coupon_handler.add_coupon(coupon_code, cognito_username)
		except InvalidCouponError:
			response['body'] = json.dumps({'error': 'That coupon does not exist or has expired.'})
			response['statusCode'] = http.HTTPStatus.BAD_REQUEST
			return response
		except CouponUsedError:
			response['body'] = json.dumps({'error': 'You have already used that coupon.'})
			response['statusCode'] = http.HTTPStatus.BAD_REQUEST
			return response
		except:
			logging.exception('Exception applying coupon.')
			response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
			return response

	logger.info('price: ' + str(price))
	if price > 0:	# Creating a payment is handled by coupon_handler if not
		try:
			intent = stripe.PaymentIntent.create(
				amount=price,
				currency='usd'
			)
			logger.info('intent from stripe: ' + str(intent))
		except:
			logging.exception('Could not get response from stripe')
			response['body'] = json.dumps({'error': 'Unable to get intent from stripe server.'})
			response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
			return response
		try:
			logger.info('Recording intent in db.')
			queries.create_payment(cognito_username, price, intent['id'])
			body = intent
			response['body'] = json.dumps(body)
			response['statusCode'] = http.HTTPStatus.OK
			return response
		except:
			logging.exception('Could not record intent in db.')
			response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
			return response
	else:
		body = {
			'amount': 0,
			'currency': 'usd'
		}
		response['body'] = json.dumps(body)
		response['statusCode'] = http.HTTPStatus.OK
		return response



def _parse_args(event):
	'''Optional arg: couponCode'''
	if not event.get('body'):
		return None

	body = json.loads(event['body'])
	coupon_code = body.get('couponCode', None)
	if coupon_code:
		coupon_code = coupon_code.upper()
	return coupon_code

