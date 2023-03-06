import uuid
import logging
from datetime import datetime

from photo import Photo
from board import Board
from board_status import BoardStatus
from board_type import BoardType
from board_photo_status import BoardPhotoStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from board_db import connection
db_conn = connection.Connection()

def get_board_by_join_code(join_code):
	with db_conn.get_cursor() as cursor:
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
			board_id, owner_id, board_name, join_code, board_status_id, board_type_id, start_date, end_date = board
			return Board(board_id, owner_id, board_name, join_code, BoardStatus(board_status_id), BoardType(board_type_id), start_date, end_date)


def get_board_owner_username(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT BIN_TO_UUID(p.cognito_username) FROM board b
						JOIN person p ON b.owner_id = p.person_id
						WHERE b.join_code = UUID_TO_BIN(%s)
						''',
						(join_code))
		results = cursor.fetchone()
		if not results:
			return None
		else:
			return results[0]

def get_photos_for_board(join_code, page_number=0, page_size=50, before_date=datetime.now(), photo_statuses=[BoardPhotoStatus.ACTIVE]):
	'''page_number is zero-indexed'''
	before_date_string = before_date.strftime('%Y-%m-%d %H:%M:%S')
	offset = page_number * page_size

	format_string = ', '.join(['%s'] * len(photo_statuses))
	tuple_of_status_ids = tuple([status.value for status in photo_statuses])
	args_tuple = (join_code, *tuple_of_status_ids, before_date_string, page_size, offset)

	query = f'''
		SELECT BIN_TO_UUID(ph.photo_key),
			ph.s3_bucket_name,
			ph.s3_object_key,
			bp.add_date,
			BIN_TO_UUID(pe.cognito_username),
			bp.board_photo_map_status_id
		FROM board b
		JOIN board_photo_map bp ON bp.board_id = b.board_id
		JOIN photo ph ON bp.photo_id = ph.photo_id
		LEFT JOIN person pe ON ph.uploader_id = pe.person_id
		WHERE b.join_code = UUID_TO_BIN(%s)
			AND bp.board_photo_map_status_id IN ({format_string})
			AND bp.add_date < %s
		ORDER BY ph.photo_id DESC
		LIMIT %s
		OFFSET %s
		'''


	with db_conn.get_cursor() as cursor:
		cursor.execute(query, args_tuple)
		results = cursor.fetchall()
		db_conn.conn.commit()
		return [Photo(*r) for r in results] # *r isn't magic, it just unpacks the tuple to args

def get_photos_by_key_and_join_code(join_code, photo_keys):
	if not photo_keys:
		return []

	format_string = ','.join(['UUID_TO_BIN(%s)'] * len(photo_keys))
	tuple_of_keys = tuple([str(key) for key in photo_keys])
	args_tuple = (*tuple_of_keys, join_code)

	with db_conn.get_cursor() as cursor:
		cursor.execute(f'''
						SELECT BIN_TO_UUID(ph.photo_key),
							ph.s3_bucket_name,
							ph.s3_object_key,
							bp.add_date,
							BIN_TO_UUID(pe.cognito_username),
							bp.board_photo_map_status_id
						FROM board b
						JOIN board_photo_map bp ON bp.board_id = b.board_id
						JOIN photo ph ON bp.photo_id = ph.photo_id
						LEFT JOIN person pe ON ph.uploader_id = pe.person_id
						WHERE
							ph.photo_key IN ({format_string})
							AND bp.board_photo_map_status_id = {ACTIVE_BOARD_PHOTO_STATUS}
							AND b.join_code = UUID_TO_BIN(%s)
						''',
						args_tuple)
		results = cursor.fetchall()
		db_conn.conn.commit()
		return [Photo(*r) for r in results] # *r isn't magic, it just unpacks the tuple to args

def get_photos_by_key(photo_keys):
	if not photo_keys:
		return []

	format_string = ','.join(['UUID_TO_BIN(%s)'] * len(photo_keys))
	tuple_of_keys = tuple([str(key) for key in photo_keys])

	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT BIN_TO_UUID(ph.photo_key),
							ph.s3_bucket_name,
							ph.s3_object_key,
							bp.add_date,
							BIN_TO_UUID(pe.cognito_username),
							bp.board_photo_map_status_id
						FROM board b
						JOIN board_photo_map bp ON bp.board_id = b.board_id
						JOIN photo ph ON bp.photo_id = ph.photo_id
						LEFT JOIN person pe ON ph.uploader_id = pe.person_id
						WHERE
							ph.photo_key IN (%s)
							AND bp.board_photo_map_status_id = 1 # ACTIVE_BOARD_PHOTO_STATUS
						''' % format_string,
						tuple_of_keys)
		results = cursor.fetchall()
		db_conn.conn.commit()
		return [Photo(*r) for r in results] # *r isn't magic, it just unpacks the tuple to args

def get_board_photos_count(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
		               	SELECT COUNT(board_photo_map_id) FROM board_photo_map m
						JOIN board b ON b.board_id = m.board_id
						WHERE b.join_code = UUID_TO_BIN(%s)
						''',
						(str(join_code)))
		results = cursor.fetchone()
		if not results:
			return 0
		else:
			return results[0]