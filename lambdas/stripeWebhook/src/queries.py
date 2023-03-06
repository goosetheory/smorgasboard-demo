import uuid

from board_db import connection
from payment_status import PaymentStatus
db_conn = connection.Connection()


def mark_payment_successful(stripe_payment_id):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						UPDATE payment
						SET payment_status_id=%s, payment_date=NOW()
						WHERE stripe_payment_id=%s
						''',
						(PaymentStatus.SUCCEEDED.value, stripe_payment_id))
		db_conn.conn.commit()


def get_cognito_username_of_payer(stripe_payment_id):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
		               	SELECT BIN_TO_UUID(per.cognito_username)
		               	FROM person per
		               	INNER JOIN payment pay ON per.person_id = pay.person_id
		               	WHERE pay.stripe_payment_id=%s
		               	''',
		               	(stripe_payment_id,))
		result = cursor.fetchone()[0]
		db_conn.conn.commit()
		return result