import uuid

from board_db import connection
from payment_status import PaymentStatus
from coupon_status import CouponStatus
from payment import Payment

db_conn = connection.Connection()


def create_payment(cognito_username, amount, stripe_payment_id, payment_status=PaymentStatus.INCOMPLETE, coupon_id=None):
	with db_conn.get_cursor() as cursor:
		person_id = _get_person_id_for_username(cursor, cognito_username)

		cursor.execute(	'''
						INSERT INTO payment (person_id, amount, payment_status_id, stripe_payment_id, coupon_id)
						VALUES (%s, %s, %s, %s, %s)
						''',
						(person_id, amount, payment_status.value, stripe_payment_id, coupon_id))
		db_conn.conn.commit()


def get_payments_for_user_and_status(cognito_username, payment_status):
	with db_conn.get_cursor() as cursor:
		person_id = _get_person_id_for_username(cursor, cognito_username)

		cursor.execute(	'''
						SELECT payment_status_id, payment_date, stripe_payment_id, amount
						FROM payment
						WHERE person_id=%s AND payment_status_id=%s
						''',
						(person_id, payment_status.value))
		results = cursor.fetchall()
		db_conn.conn.commit()
		payments = []
		for payment_status_id, payment_date, stripe_payment_id, amount in results:
			payment = Payment(PaymentStatus(payment_status_id), payment_date, stripe_payment_id, amount)
			payments.append(payment)
		return payments


def get_coupon_info(coupon_code):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT coupon_id, coupon_price_pennies, coupon_status_id
						FROM coupon
						WHERE coupon_code=%s
						''',
						(coupon_code,))
		result = cursor.fetchone()
		db_conn.conn.commit()
		if not result:
			return None
		coupon_id, coupon_price_pennies, coupon_status_id = result
		return {
			'status': CouponStatus(coupon_status_id),
			'coupon_id': coupon_id,
			'price': coupon_price_pennies
		}


def get_coupon_usage(cognito_username, coupon_id):
	with db_conn.get_cursor() as cursor:
		cursor.execute(	'''
						SELECT pt.payment_status_id FROM payment pt
						JOIN person p ON pt.person_id = p.person_id
						JOIN coupon c ON pt.coupon_id = c.coupon_id
						WHERE
							p.cognito_username=UUID_TO_BIN(%s) AND
							c.coupon_id=%s
						''',
						(cognito_username, coupon_id))
		results = cursor.fetchall()
		db_conn.conn.commit()
		result_dicts = []
		for payment_status_id, in results:
			result_dicts.append({
								'payment_status': PaymentStatus(payment_status_id)
							 })
		return result_dicts


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