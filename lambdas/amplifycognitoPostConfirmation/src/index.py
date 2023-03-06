import pymysql
import json
import logging

import queries
from lambda_client import LambdaClient
lambda_client = LambdaClient()

from board_db import connection
conn = connection.Connection()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
	'''
	Adds to person table & sends email
	'''
	cognito_username = event['userName']
	user_email = event['request']['userAttributes']['email']
	given_name = event['request']['userAttributes']['given_name']

	try:
		queries.create_person(user_email, given_name, cognito_username)
	except Exception as err:
		logging.exception('Error while creating user.')
		raise Exception('Unable to create account. Please try again later.')

	logger.info('Inserted user %s successfully.' % user_email)

	try:
		lambda_client.send_join_email(cognito_username)
	except:
		logging.exception('Error invoking send-email lambda.')

	return event

