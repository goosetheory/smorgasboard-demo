import uuid
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from board_db import connection
db_conn = connection.Connection()

def get_board_info(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT b.board_name, b.board_id, p.given_name, p.email_address, p.person_id
						FROM board b
						JOIN person p ON b.owner_id = p.person_id
						WHERE b.join_code = UUID_TO_BIN(%s)
						''',
						(join_code,))
		results = cursor.fetchone()
		db_conn.conn.commit()
		if not results:
			return None

		board_name, board_id, given_name, email_address, person_id = results
		return {
			'board_name': board_name,
			'board_id': board_id,
			'given_name': given_name,
			'email_address': email_address,
			'person_id': person_id
		}

def get_person_info(cognito_username):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT person_id, given_name, email_address
						FROM person
						WHERE cognito_username=UUID_TO_BIN(%s)
						''',
						(str(cognito_username),))
		results = cursor.fetchone()
		db_conn.conn.commit()
		if not results:
			return None

		person_id, given_name, email_address = results
		return {
			'person_id': person_id,
			'given_name': given_name,
			'email_address': email_address
		}

def record_sent_email(recipient_person_id, email_type_id, message_id, board_id=None):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						INSERT INTO email (recipient_person_id, email_type_id, sent_date, message_id, board_id)
						VALUES (%s, %s, NOW(), %s, %s)
						''',
						(recipient_person_id, email_type_id, message_id, board_id))
		db_conn.conn.commit()


