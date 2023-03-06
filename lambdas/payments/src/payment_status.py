from enum import Enum

class PaymentStatus(Enum):
	INCOMPLETE = 1
	SUCCEEDED = 2
	CONSUMED = 3
	REFUNDED = 4
