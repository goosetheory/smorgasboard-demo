import uuid
import logging

from board_connection import BoardConnection

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from board_db import connection
db_conn = connection.Connection()

def get_open_connections():
	with db_conn.get_cursor() as cursor:
		cursor.execute( '''
						SELECT board_connection_id, ws_connection_id
						FROM board_connection
						WHERE board_connection_status_id = 1 # CONNECTED
							AND begin_date > NOW() - INTERVAL 2 HOUR
						ORDER BY begin_date ASC
						LIMIT 500
						''')

		results = cursor.fetchall()
		db_conn.conn.commit()

		return [BoardConnection(*r) for r in results]


def mark_connections_closed(connections):
	format_string = ','.join(['%s'] * len(connections))
	tuple_of_connection_ids = tuple([conn.board_connection_id for conn in connections])

	with db_conn.get_cursor() as cursor:
		cursor.execute( '''
						UPDATE board_connection
						SET
							board_connection_status_id = 2, # DISCONNECTED
							end_date = NOW()
						WHERE
							board_connection_status_id = 1 # CONNECTED
							AND board_connection_id IN (%s)
						''' % format_string,
						tuple_of_connection_ids)
		db_conn.conn.commit()