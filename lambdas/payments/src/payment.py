from payment_status import PaymentStatus

class Payment:
	def __init__(self, payment_status, payment_date, stripe_payment_id, amount):
		self.payment_status = PaymentStatus(payment_status)
		self.payment_date = payment_date
		self.stripe_payment_id = stripe_payment_id
		self.amount = amount

	def to_dict(self):
		return {
			'paymentStatus': self.payment_status.value,
			'paymentDateTimestamp': self.payment_date.timestamp() * 1000 if self.payment_date else None,
			'stripePaymentId': self.stripe_payment_id,
			'amount': self.amount
		}
