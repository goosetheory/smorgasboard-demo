import uuid
import logging

from board import Board
from board_status import BoardStatus
from board_type import BoardType

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from board_db import connection
db_conn = connection.Connection()

def get_boards_for_user(cognito_username):
	with db_conn.get_cursor() as cursor:
		cursor.execute('''
						SELECT b.board_id, b.owner_id, b.board_name, BIN_TO_UUID(b.join_code), b.board_status_id, b.board_type_id, b.start_date, b.end_date
						FROM board b
						JOIN person p ON b.owner_id = p.person_id
						WHERE p.cognito_username = UUID_TO_BIN(%s)''',
						(cognito_username,))
		results = cursor.fetchall()
		db_conn.conn.commit()
		return [_board_tuple_to_board(board) for board in results]


def get_board_by_join_code(join_code):
	with db_conn.get_cursor() as cursor:
		board = _get_board_by_join_code(cursor, join_code)
		db_conn.conn.commit()
		return board


def create_board(cognito_username, board_name, board_status, board_type):
	with db_conn.get_cursor() as cursor:
		owner_id = _get_person_id_for_username(cursor, cognito_username)
		new_uuid = uuid.uuid4()
		cursor.execute(	'''
						INSERT INTO board (owner_id, board_name, join_code, board_status_id, board_type_id)
						VALUES (%s, %s, UUID_TO_BIN(%s), %s, %s);
						''',
						(owner_id, board_name, new_uuid, board_status.value, board_type.value))
		db_conn.conn.commit()
		return _get_board_by_join_code(cursor, new_uuid)


def update_board(board):
	start_date = board.start_date.strftime('%Y-%m-%d %H:%M:%S') if board.start_date else None
	end_date = board.end_date.strftime('%Y-%m-%d %H:%M:%S') if board.end_date else None
	with db_conn.get_cursor() as cursor:
		cursor.execute( '''
						UPDATE board
						SET
							board_status_id = %s,
							start_date = %s,
							end_date = %s
						WHERE
							join_code=UUID_TO_BIN(%s)
						''',
						(board.board_status.value, start_date, end_date, board.join_code))
		updated_board = _get_board_by_join_code(cursor, board.join_code)
		db_conn.conn.commit()
		return updated_board


def create_photo_for_board(cognito_username,
						   photo_key,
						   s3_bucket_name,
						   s3_object_key,
						   join_code,
						   board_photo_status):
	with db_conn.get_cursor() as cursor:
		try:
			person_id = _get_person_id_for_username(cursor, cognito_username)
			board = _get_board_by_join_code(cursor, join_code)
			new_photo_id = _create_photo(cursor, person_id, photo_key, s3_bucket_name, s3_object_key)
			_create_mapping(cursor, board, new_photo_id, board_photo_status)
			db_conn.conn.commit()
			cursor.close()
		except:
			logging.exception(f'Could not insert photo {url} for user {cognito_username}')
			db_conn.conn.rollback()
			raise Exception('Could not insert photo.')


def set_board_photo_status(photo_key, join_code, board_photo_status):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						UPDATE board_photo_map m
						JOIN photo p ON p.photo_id = m.photo_id
						JOIN board b ON b.board_id = m.board_id
						SET m.board_photo_map_status_id = %s
						WHERE p.photo_key = UUID_TO_BIN(%s)
							AND b.join_code = UUID_TO_BIN(%s)
						''',
						(board_photo_status.value, str(photo_key), str(join_code)))
		db_conn.conn.commit()


def get_photos_for_board(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT BIN_TO_UUID(p.photo_key) FROM board b
						JOIN board_photo_map bp ON b.board_id = bp.board_id
						JOIN photo p ON bp.photo_id = p.photo_id
						WHERE b.join_code=UUID_TO_BIN(%s)
						''',
						str(join_code))
		results = cursor.fetchall()
		detupled_results = [photo_key for photo_key, in results]
		db_conn.conn.commit()
		return detupled_results


def get_board_owner_username(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT BIN_TO_UUID(p.cognito_username) FROM board b
						JOIN person p ON b.owner_id = p.person_id
						WHERE b.join_code = UUID_TO_BIN(%s)
						''',
						(join_code))
		results = cursor.fetchone()
		db_conn.conn.commit()
		if not results:
			return None
		else:
			return results[0]


def get_connections_for_board(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
			SELECT bc.ws_connection_id FROM board b
			JOIN board_connection bc ON bc.board_id = b.board_id
			WHERE
				b.join_code = UUID_TO_BIN(%s)
				AND bc.board_connection_status_id = 1 # CONNECTED
			''',
			join_code)

		results = cursor.fetchall()
		detupled_results = [photo_key for photo_key, in results]
		db_conn.conn.commit()
		return detupled_results


def get_first_succeeded_payment_id_for_user(cognito_username):
	with db_conn.get_cursor() as cursor:
		person_id = _get_person_id_for_username(cursor, cognito_username)
		cursor.execute(	'''
						SELECT payment_id FROM payment
						WHERE person_id=%s
							AND payment_status_id=2 -- SUCCEEDED
						LIMIT 1
						''',
						(person_id))
		results = cursor.fetchone()
		db_conn.conn.commit()
		if not results:
			return None
		else:
			return results[0]


def update_payment_status(payment_id, new_status):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						UPDATE payment
						SET payment_status_id=%s
						WHERE payment_id=%s
						''',
						(new_status.value, payment_id))
		db_conn.conn.commit()


def _create_photo(cursor, person_id, photo_key, s3_bucket_name, s3_object_key):
	cursor.execute(	'''
					INSERT INTO photo (uploader_id, photo_key, s3_bucket_name, s3_object_key, upload_date)
					VALUES (%s, UUID_TO_BIN(%s), %s, %s, NOW());
					''',
					(person_id, photo_key, s3_bucket_name, s3_object_key))
	return cursor.lastrowid


def _create_mapping(cursor, board, photo_id, board_photo_status):
	cursor.execute(	'''
					INSERT INTO board_photo_map (board_id, photo_id, board_photo_map_status_id, add_date)
					VALUES (%s, %s, %s, NOW())
					''',
					(board.board_id, photo_id, board_photo_status.value))


def _get_board_by_join_code(cursor, join_code):
	cursor.execute(	'''
					SELECT board_id, owner_id, board_name, BIN_TO_UUID(join_code), board_status_id, board_type_id, start_date, end_date
					FROM board
					WHERE join_code=UUID_TO_BIN(%s)
					''',
					(join_code,))
	board = cursor.fetchone()
	if not board:
		logger.error('No board found for join code: ' + str(join_code))
		return None
	else:
		return _board_tuple_to_board(board)


def _get_person_id_for_username(cursor, cognito_username):
	if not cognito_username:
		return None

	cursor.execute(	'''
					SELECT person_id
					FROM person
					WHERE person.cognito_username = UUID_TO_BIN(%s)''',
					(cognito_username,))
	person_id = cursor.fetchone()
	return person_id


def _board_tuple_to_board(board_tuple):
	board_id, owner_id, board_name, join_code, board_status_id, board_type_id, start_date, end_date = board_tuple
	return Board(board_id, owner_id, board_name, join_code, BoardStatus(board_status_id), BoardType(board_type_id), start_date, end_date)
