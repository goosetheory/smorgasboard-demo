import uuid
import logging

from board_membership_status import BoardMembershipStatus
from membership_public import MembershipPublic
from membership import Membership

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from board_db import connection
db_conn = connection.Connection()

def create_or_update_membership(cognito_username, join_code, status):
	with db_conn.get_cursor() as cursor:
		try:
			existing_membership = _get_existing_membership(cursor, cognito_username, join_code)
			if existing_membership:
				_update_membership(cursor, existing_membership, status)
			else:
				_create_membership(cursor, cognito_username, join_code, status)
			db_conn.conn.commit()
		except:
			logging.exception('Could not upsert person %s into board %s' % (cognito_username, join_code))
			db_conn.conn.rollback()
			raise Exception('Could not upsert membership.')

def get_boards_for_person_and_status(cognito_username, status):
	with db_conn.get_cursor() as cursor:
		try:
			cursor.execute(	'''
							SELECT b.board_name, BIN_TO_UUID(b.join_code), BIN_TO_UUID(p.cognito_username), p.given_name, bm.board_membership_status_id, bm.join_date
							FROM board b
							JOIN board_membership bm
								ON b.board_id = bm.board_id
							JOIN person p
								ON bm.person_id = p.person_id
							WHERE p.cognito_username = UUID_TO_BIN(%s)
								AND bm.board_membership_status_id = %s
							''',
							(cognito_username, status.value))
			memberships = cursor.fetchall()
			db_conn.conn.commit()
			result = []
			for membership in memberships:
				board_name, join_code, cognito_username, given_name, status, join_date = membership
				new_membership = MembershipPublic(board_name, join_code, cognito_username, given_name, status, join_date)
				result.append(new_membership)
			return result
		except:
			logging.exception('Could not get boards person %s is a member of.', cognito_username)
			db_conn.conn.commit()
			raise Exception('Could not get memberships.')


def deactivate_other_memberships(cognito_username, join_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
		               	UPDATE board b
						JOIN board_membership bm ON b.board_id = bm.board_id
						JOIN person p ON bm.person_id = p.person_id
						SET bm.board_membership_status_id = 5 # INACTIVE
						WHERE p.cognito_username = UUID_TO_BIN(%s)
							AND b.join_code <> UUID_TO_BIN(%s)
						''',
						(cognito_username, join_code))
		db_conn.conn.commit()

def _get_existing_membership(cursor, cognito_username, join_code):
	cursor.execute(	'''
					SELECT board_membership_id, join_date, bm.person_id, bm.board_id, board_membership_status_id
					FROM board_membership bm
					JOIN person p
						ON p.person_id = bm.person_id
					JOIN board b
						ON b.board_id = bm.board_id
					WHERE p.cognito_username = UUID_TO_BIN(%s)
						AND b.join_code = UUID_TO_BIN(%s)
					''',
					(cognito_username, join_code))
	membership = cursor.fetchone()
	if not membership:
		return None
	else:
		board_membership_id, join_date, person_id, board_id, board_membership_status_id = membership
		return Membership(board_membership_id, join_date, person_id, board_id, board_membership_status_id)

def _create_membership(cursor, cognito_username, join_code, status):
	person_id = _get_person_id_for_username(cursor, cognito_username)
	board_id = _get_board_id_by_join_code(cursor, join_code)
	cursor.execute(	'''
				INSERT INTO board_membership (person_id, board_id, join_date, board_membership_status_id)
				VALUES (%s, %s, NOW(), %s)
				''',
				(person_id, board_id, status.value))

def _update_membership(cursor, membership, status):
	cursor.execute(	'''
					UPDATE board_membership
					SET
						board_membership_status_id = %s
					WHERE
						board_membership_id = %s
					''',
					(status.value, membership.board_membership_id))


def _get_board_id_by_join_code(cursor, join_code):
	cursor.execute(	'''
					SELECT board_id
					FROM board
					WHERE join_code=UUID_TO_BIN(%s)
					''',
					(join_code,))
	board_id = cursor.fetchone()
	if not board_id:
		logger.error('No board found for join code: ' + str(join_code))
		return None
	else:
		return board_id

def _get_person_id_for_username(cursor, cognito_username):
	cursor.execute(	'''
					SELECT person_id
					FROM person
					WHERE cognito_username = UUID_TO_BIN(%s)''',
					(cognito_username,))
	person_id = cursor.fetchone()
	if not person_id:
		logger.error('No person found for cognito username: ' + str(cognito_username))
		return None
	else:
		return person_id