import uuid
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from board_db import connection
db_conn = connection.Connection()

def create_person(user_email, given_name, cognito_username):
	with db_conn.get_cursor() as cursor:
		cursor.execute('''
				INSERT INTO person (email_address, given_name, cognito_username)
				VALUES (%s, %s, UUID_TO_BIN(%s))''',
				(user_email, given_name, cognito_username))
		db_conn.conn.commit()
