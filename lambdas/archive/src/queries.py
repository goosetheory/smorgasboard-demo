from board_db import connection
db_conn = connection.Connection()

def create_archive(join_code):
	with db_conn.get_cursor() as cursor:
		board_id = _get_board_id(cursor, join_code)
		cursor.execute(	'''
						INSERT INTO archive (board_id, create_date)
						VALUES (%s, NOW())
						''',
						(board_id,))
		db_conn.conn.commit()


def get_photo_retrieval_info(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT s3_bucket_name, s3_object_key
						FROM photo p
						JOIN board_photo_map bpm ON p.photo_id = bpm.photo_id
						JOIN board b ON b.board_id = bpm.board_id
						WHERE b.join_code = UUID_TO_BIN(%s)
						AND bpm.board_photo_map_status_id = 1 # ACTIVE
						''',
						(join_code,))
		results = cursor.fetchall()
		db_conn.conn.commit()
		return results


def create_archive(join_code, bucket_name, shard_filenames):
	with db_conn.get_cursor() as cursor:
		board_id = _get_board_id(cursor, join_code)
		cursor.execute(	'''
						INSERT INTO archive (board_id, create_date)
						VALUES (%s, NOW())
						''',
						(board_id,))

		new_archive_id = cursor.lastrowid

		shard_values = [(new_archive_id, bucket_name, shard_filename) for shard_filename in shard_filenames]

		cursor.executemany(	'''
							INSERT INTO archive_shard (archive_id, s3_bucket_name, s3_object_key)
							VALUES (%s, %s, %s)
							''',
							shard_values)
		db_conn.conn.commit()

def get_archive_info(join_code):
	with db_conn.get_cursor() as cursor:
		board_id = _get_board_id(cursor, join_code)
		cursor.execute(	'''
						SELECT s.s3_bucket_name, s.s3_object_key FROM archive a
						LEFT JOIN archive_shard s ON a.archive_id = s.archive_id
						WHERE a.board_id = %s
						''',
						(board_id,))
		results = cursor.fetchall()
		db_conn.conn.commit()
		return results


def get_board_owner_username(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT BIN_TO_UUID(p.cognito_username) FROM board b
						JOIN person p ON b.owner_id = p.person_id
						WHERE b.join_code = UUID_TO_BIN(%s)
						''',
						(str(join_code)))
		results = cursor.fetchone()
		db_conn.conn.commit()
		if not results:
			return None
		else:
			return results[0]

def does_archive_exist(join_code):
	with db_conn.get_cursor() as cursor:
		board_id = _get_board_id(cursor, join_code)
		cursor.execute(	'''
						SELECT 1 FROM archive
						WHERE board_id = %s
						''',
						(board_id))
		results = cursor.fetchone()
		db_conn.conn.commit()
		if results:
			return True
		else:
			return False

def _get_board_id(cursor, join_code):
	cursor.execute(	'''
					SELECT board_id FROM board
					WHERE join_code = UUID_TO_BIN(%s)
					''',
					(join_code))
	board_id = cursor.fetchone()[0]
	db_conn.conn.commit()
	return board_id