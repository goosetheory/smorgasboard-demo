import uuid
import logging
from datetime import datetime

from board import Board

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from board_db import connection
db_conn = connection.Connection()

CONNECTED_STATUS = 1
DISCONNECTED_STATUS = 2

def get_board(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
		               	SELECT b.board_id, BIN_TO_UUID(p.cognito_username)
		               	FROM board b
		               	JOIN person p ON b.owner_id = p.person_id
		               	WHERE b.join_code = UUID_TO_BIN(%s)
		               	''',
		               	(str(join_code)))
		board = cursor.fetchone()
		if not board:
			logger.error('No board found for join code: ' + str(join_code))
			return None
		else:
			board_id, cognito_username = board
			return Board(board_id, cognito_username)


def create_connection(board_id, connection_id):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						INSERT INTO board_connection (
							ws_connection_id,
							board_id,
							board_connection_status_id,
							begin_date
						) VALUES (%s, %s, %s, NOW())
						''',
						(connection_id, board_id, CONNECTED_STATUS))
		db_conn.conn.commit()


def disconnect_connection(connection_id):
	with db_conn.get_cursor() as cursor:
		cursor.execute( '''
						UPDATE board_connection
						SET
							board_connection_status_id = %s,
							end_date = NOW()
						WHERE
							ws_connection_id = %s
						''',
						(DISCONNECTED_STATUS, connection_id))
		db_conn.conn.commit()

