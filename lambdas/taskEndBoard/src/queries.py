import uuid
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from board_type import BoardType
from board_db import connection
db_conn = connection.Connection()

def get_first_expired_board():
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT BIN_TO_UUID(join_code), board_type_id FROM board
						WHERE end_date < NOW()
							AND board_status_id = 1 # ACTIVE
						ORDER BY end_date ASC
						LIMIT 1
						''')

		result = cursor.fetchone()
		db_conn.conn.commit()

		if not result:
			return None
		else:
			join_code, board_type_id = result
			return join_code, BoardType(board_type_id)

def mark_board_completed(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						UPDATE board
						SET board_status_id = 3 # COMPLETED
						WHERE join_code = UUID_TO_BIN(%s)
						''',
						(join_code,))
		db_conn.conn.commit()