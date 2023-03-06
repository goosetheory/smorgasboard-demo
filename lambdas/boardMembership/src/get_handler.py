import pymysql
import json
import logging
import http

import queries
from board_membership_status import BoardMembershipStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle(event, context):
	logger.info('GET board memberships.')
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
		},
	}

	try:
		cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
	except:
		logger.error('Could not find cognito username from event: ' + str(event))
		response['statusCode'] = http.HTTPStatus.UNAUTHORIZED
		return response
	try:
		memberships = queries.get_boards_for_person_and_status(cognito_username, BoardMembershipStatus.ACTIVE)
		json_memberships = [membership.to_json() for membership in memberships]
		response['statusCode'] = http.HTTPStatus.OK
		response['body'] = json.dumps(json_memberships)
		return response
	except Exception as e:
		logging.exception('Error getting board memberships.')
		response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
		response['body'] = 'Could not get board membership info.'
		return response
