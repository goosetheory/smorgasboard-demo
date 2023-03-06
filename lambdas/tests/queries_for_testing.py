import uuid

from board_db import connection
db_conn = connection.Connection()

def create_person():
	cognito_username = str(uuid.uuid4())
	given_name = 'Test'
	user_email = f'test_{cognito_username}@test.com'
	with db_conn.get_cursor() as cursor:
		cursor.execute('''
				INSERT INTO person (email_address, given_name, cognito_username)
				VALUES (%s, %s, UUID_TO_BIN(%s))''',
				(user_email, given_name, cognito_username))
		db_conn.conn.commit()
	return {
		'cognito_username': cognito_username,
		'given_name': given_name,
		'user_email': user_email
	}

def create_payment(cognito_username, payment_status_id=2):
	# Default payment status is 2, which is SUCCEEDED
	with db_conn.get_cursor() as cursor:
		person_id = _get_person_id(cursor, cognito_username)
		cursor.execute(	'''
						INSERT INTO payment (person_id, amount, payment_status_id, stripe_payment_id, coupon_id)
						VALUES (%s, 10, %s, %s, %s)
						''',
						(person_id, payment_status_id, 'stripe_payment_id', None))
		db_conn.conn.commit()

def delete_person(cognito_username):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						DELETE FROM person
						WHERE UUID_TO_BIN(%s) = cognito_username;
						''',
						(cognito_username,))
		db_conn.conn.commit()


def create_board(owner_cognito_username, board_status_id=2, board_type_id=2):
	# Default board status id is 2, NOT_STARTED
	# Default board type id is 2, STANDARD
	board_name = 'Test Board'
	join_code = str(uuid.uuid4())
	with db_conn.get_cursor() as cursor:
		person_id = _get_person_id(cursor, owner_cognito_username)

		cursor.execute(	'''
						INSERT INTO board (owner_id, board_name, join_code, board_status_id, board_type_id)
						VALUES (%s, %s, UUID_TO_BIN(%s), %s, %s)
						''',
						(person_id, board_name, join_code, board_status_id, board_type_id))


		db_conn.conn.commit()
	return {
		'join_code': join_code,
		'board_name': board_name
	}

def create_photo(board_join_code, photo_status_id=1):
	photo_key = str(uuid.uuid4())
	s3_object_key = photo_key + '.jpg'
	s3_bucket_name = 'testbucket'
	with db_conn.get_cursor() as cursor:
		board_id = _get_board_id(cursor, board_join_code)

		cursor.execute(	'''
						INSERT INTO photo (uploader_id, photo_key, s3_bucket_name, s3_object_key, upload_date)
						VALUES (%s, UUID_TO_BIN(%s), %s, %s, NOW())
						''',
						(None, photo_key, s3_bucket_name, s3_object_key))
		photo_id = cursor.lastrowid
		cursor.execute(	'''
						INSERT INTO board_photo_map (board_id, photo_id, board_photo_map_status_id, add_date)
						VALUES (%s, %s, %s, NOW())
						''',
						(board_id, photo_id, photo_status_id))
		db_conn.conn.commit()
		return {
			'photo_key': photo_key,
			's3_bucket_name': s3_bucket_name,
			's3_object_key': s3_object_key,
		}

def get_board_photo_map(join_code, photo_key):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
		               	SELECT photo_key, board_photo_map_status_id FROM board_photo_map m
		               	JOIN photo p ON m.photo_id = p.photo_id
		               	JOIN board b ON m.board_id = b.board_id
		               	WHERE b.join_code = UUID_TO_BIN(%s)
		               		AND p.photo_key = UUID_TO_BIN(%s)
		               	''',
						(join_code, photo_key))
		result = cursor.fetchone()
		db_conn.conn.commit()
		return {
			'photo_key': result[0],
			'status_id': result[1]
		}

def delete_board(join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
				DELETE FROM board
				WHERE UUID_TO_BIN(%s) = join_code
				''',
				(join_code,))
		db_conn.conn.commit()

def teardown_person(cognito_username):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						DELETE board_photo_map, photo
						FROM person
						LEFT JOIN board ON person.person_id = board.owner_id
						LEFT JOIN board_photo_map ON board_photo_map.board_id = board.board_id
						LEFT JOIN photo ON board_photo_map.photo_id = photo.photo_id
						WHERE person.cognito_username = UUID_TO_BIN(%s)
						''',
						(cognito_username,))

		cursor.execute(	'''
						DELETE payment
						FROM person
						LEFT JOIN payment ON payment.person_id = person.person_id
						WHERE person.cognito_username = UUID_TO_BIN(%s);
						''',
						(cognito_username,))

		cursor.execute(	'''
						DELETE board
						FROM person
						LEFT JOIN board ON person.person_id = board.owner_id
						WHERE person.cognito_username = UUID_TO_BIN(%s);
						''',
						(cognito_username,))

		cursor.execute(	'''
						DELETE person
						FROM person
						WHERE person.cognito_username = UUID_TO_BIN(%s);
						''',
						(cognito_username,))
		db_conn.conn.commit()


def delete_all_boards_for_user(owner_cognito_username):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						DELETE board FROM board
						INNER JOIN person ON owner_id = person_id
						WHERE cognito_username = UUID_TO_BIN(%s);
						''',
						(owner_cognito_username,))
		db_conn.conn.commit()

def delete_all_payments_for_user(cognito_username):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						DELETE payment FROM payment
						INNER JOIN person ON person.person_id = payment.person_id
						WHERE cognito_username = UUID_TO_BIN(%s);
						''',
						(cognito_username,))
		db_conn.conn.commit()

def _get_board_id(cursor, join_code):
	cursor.execute(	'''
					SELECT board_id
					FROM board
					WHERE UUID_TO_BIN(%s) = join_code
					''',
					(join_code,))
	return cursor.fetchone()

def _get_person_id(cursor, cognito_username):
		cursor.execute(	'''
						SELECT person_id
						FROM person
						WHERE UUID_TO_BIN(%s) = cognito_username
						''',
						(cognito_username,))
		person_id = cursor.fetchone()
		return person_id