import logging

import queries
from coupon_status import CouponStatus
from payment_status import PaymentStatus


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CouponHandler:
	def __init__(self):
		pass

	def add_coupon(self, coupon_code, cognito_username):
		coupon_info = queries.get_coupon_info(coupon_code)
		logger.info('Coupon info: ' + str(coupon_info))
		if not coupon_info or coupon_info['status'] != CouponStatus.ACTIVE:
			logging.warning('Invalid or nonexistent coupon code.')
			raise InvalidCouponError

		coupon_payments = queries.get_coupon_usage(cognito_username, coupon_info['coupon_id'])
		for payment in coupon_payments:
			if payment['payment_status'] != PaymentStatus.INCOMPLETE:
				# Coupon has already been used by this person, do not allow use again
				logger.warning('Coupon code already used by this user.')
				raise CouponUsedError

		if coupon_info['price'] <= 0:
			# Coupon allows free board; create a complete payment for this user
			logger.info('Creating payment in db for 0-cost coupon')
			queries.create_payment(cognito_username, 0, None, PaymentStatus.SUCCEEDED, coupon_info['coupon_id'])

		return coupon_info['price']


class InvalidCouponError(Exception):
	pass

class CouponUsedError(Exception):
	pass
