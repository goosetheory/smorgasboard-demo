import uuid
import http
import logging

import queries

import email_templates
from email_service import EmailService
from email_type import EmailType
from email_dto import EmailDTO

logger = logging.getLogger()
logger.setLevel(logging.INFO)

email_service = EmailService()


def handle(event, context):
	try:
		email_type = _get_email_type(event)
		logger.info(f'Email type: {str(email_type)}')
	except:
		logging.exception('Email type could not be parsed.')
		return _fail()


	if email_type == EmailType.ON_JOIN:
		return _handle_email_for_signup(event)
	elif email_type == EmailType.ON_BOARD_END:
		return _handle_email_for_board_end(event)
	elif email_type == EmailType.ON_PAY_FOR_BOARD:
		return _handle_email_for_purchase(event)
	elif email_type == EmailType.ON_FREE_TRIAL_END:
		return _handle_email_for_free_trial_end(event)
	else:
		logger.error(f'Email type not found: {str(email_type)}')
		return _fail(http.HTTPStatus.BAD_REQUEST)


def _get_email_type(event):
	email_type = EmailType(int(event['emailType']))
	return email_type

def _handle_email_for_signup(event):
	'''Expected body:
	{
		'emailType': 1,
		'cognitoUsername': <uuid>
	}
	'''
	try:
		cognito_username = uuid.UUID(event['cognitoUsername'])
	except:
		logging.exception('Could not parse cognito username from event.')
		return _fail()

	try:
		person_info = queries.get_person_info(cognito_username)
		if not person_info:
			logger.error(f'Could not find person {str(cognito_username)}')
			return _fail()
	except:
		logging.exception('Could not get person info from db')
		return _fail()

	subject = email_templates.signup_subject()
	body_text = email_templates.signup_body_text()
	body_html = email_templates.signup_body_html()

	email = EmailDTO(person_info['email_address'], subject, body_text, body_html)
	email_service.send(email)
	if not email.sent:
		logger.error('Could not send email.')
		return _fail()

	try:
		queries.record_sent_email(person_info['person_id'], EmailType.ON_JOIN.value, email.message_id, None)
	except:
		logging.exception(f'Could not record signup email for person {str(cognito_username)}')
		return _fail()

	return _succeed()


def _handle_email_for_purchase(event):
	'''Expected body:
	{
		'emailType'': 2,
		'cognitoUsername': <uuid>
	}
	'''
	try:
		cognito_username = uuid.UUID(event['cognitoUsername'])
	except:
		logging.exception('Could not parse cognito username from event.')
		return _fail()

	try:
		person_info = queries.get_person_info(cognito_username)
		if not person_info:
			logger.error(f'Could not find person {str(cognito_username)}')
			return _fail()
	except:
		logging.exception('Could not get person info from db')
		return _fail()
	subject = email_templates.board_purchased_subject()
	body_text = email_templates.board_purchased_body_text(person_info['given_name'])
	body_html = email_templates.board_purchased_body_html(person_info['given_name'])

	email = EmailDTO(person_info['email_address'], subject, body_text, body_html)

	email_service.send(email)
	if not email.sent:
		logger.error('Could not send email.')
		return _fail()

	try:
		queries.record_sent_email(person_info['person_id'], EmailType.ON_PAY_FOR_BOARD.value, email.message_id, None)
	except:
		logging.exception(f'Could not record purchase email for person {str(cognito_username)}')
		return _fail()

	return _succeed()



def _handle_email_for_free_trial_end(event):
	'''Expected body:
		{
			'emailType': 5,
			'joinCode': <uuid>
		}
	'''
	try:
		join_code = uuid.UUID(event['joinCode'])
	except:
		logging.exception('Could not parse join code from event.')
		return _fail()

	try:
		board_info = queries.get_board_info(join_code)
	except:
		logging.exception('Could not get board info from db')
		return _fail()

	subject = email_templates.free_trial_ended_subject()
	body_text = email_templates.free_trial_ended_body_text(board_info['given_name'])
	body_html = email_templates.free_trial_ended_body_html(board_info['given_name'])
	email = EmailDTO(board_info['email_address'], subject, body_text, body_html)

	email_service.send(email)
	if not email.sent:
		logger.error('Could not send email.')
		return _fail()

	try:
		queries.record_sent_email(board_info['person_id'], EmailType.ON_FREE_TRIAL_END.value, email.message_id, board_info['board_id'])
	except:
		logging.exception(f'Could not record board-end email for board {str(join_code)}.')
		return _fail()

	return _succeed()


def _handle_email_for_board_end(event):
	'''Expected body:
		{
			'emailType': 4,
			'joinCode': <uuid>
		}
	'''
	try:
		join_code = uuid.UUID(event['joinCode'])
	except:
		logging.exception('Could not parse join code from event.')
		return _fail()

	try:
		board_info = queries.get_board_info(join_code)
	except:
		logging.exception('Could not get board info from db')
		return _fail()

	subject = email_templates.board_ended_subject()
	body_text = email_templates.board_ended_body_text(
												board_info['given_name'],
												board_info['board_name'],
												str(join_code))
	body_html = email_templates.board_ended_body_html(
												board_info['given_name'],
												board_info['board_name'],
												str(join_code))
	email = EmailDTO(board_info['email_address'], subject, body_text, body_html)

	email_service.send(email)
	if not email.sent:
		logger.error('Could not send email.')
		return _fail()

	try:
		queries.record_sent_email(board_info['person_id'], EmailType.ON_BOARD_END.value, email.message_id, board_info['board_id'])
	except:
		logging.exception(f'Could not record board-end email for board {str(join_code)}.')
		return _fail()

	return _succeed()

def _fail(response_code=http.HTTPStatus.INTERNAL_SERVER_ERROR):
	response = _create_response()
	response['statusCode'] = response_code
	response['body'] = 'Could not send email.'
	return response

def _succeed():
	response = _create_response()
	response['statusCode'] = http.HTTPStatus.OK
	return response

def _create_response():
	return {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
	}
