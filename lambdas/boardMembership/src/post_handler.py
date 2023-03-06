import pymysql
import json
import logging
import http

import queries
from board_membership_status import BoardMembershipStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle(event, context):
	'''Expected body:
	{
		cognitoUsername: string (optional),
		joinCode: string,
		boardMembershipStatus: int,
	}

	If cognitoUsername absent, assume self
	'''
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
		},
	}

	try:
		caller_cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
	except:
		logger.exception('Could not find cognito username from event: ' + str(event))
		response['statusCode'] = http.HTTPStatus.UNAUTHORIZED
		return response

	try:
		body = json.loads(event['body'])
		join_code = body['joinCode']
		target_status = BoardMembershipStatus(int(body['boardMembershipStatus']))
	except:
		logging.exception('Invalid arguments.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	if 'cognitoUsername' in body:
		target_cognito_username = body['cognitoUsername']
	else:
		target_cognito_username = caller_cognito_username

	queries.create_or_update_membership(target_cognito_username, join_code, target_status)
	queries.deactivate_other_memberships(target_cognito_username, join_code)
	response['statusCode'] = http.HTTPStatus.OK

	return response
