CREATE TABLE IF NOT EXISTS payment (
	payment_id			BIGINT		NOT NULL	AUTO_INCREMENT,
	person_id			BIGINT		NOT NULL,
	amount				BIGINT		NOT NULL,
	payment_date		DATETIME	NULL,
	payment_status_id	BIGINT		NOT NULL,
	stripe_payment_id	VARCHAR(32)	NULL,
	coupon_id			BIGINT		NULL,

	PRIMARY KEY (payment_id),

	FOREIGN KEY (person_id)	REFERENCES person(person_id),
	FOREIGN KEY (payment_status_id)	REFERENCES	payment_status_lookup(payment_status_lookup_id),
	FOREIGN KEY (coupon_id) REFERENCES coupon(coupon_id)
);