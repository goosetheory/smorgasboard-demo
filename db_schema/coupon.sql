CREATE TABLE IF NOT EXISTS coupon	(
	coupon_id				BIGINT		NOT NULL	AUTO_INCREMENT,
	coupon_code				VARCHAR(40)	NOT NULL,
	coupon_status_id		BIGINT		NOT NULL,
	coupon_price_pennies	INT		NOT NULL,

	PRIMARY KEY (coupon_id),
	FOREIGN Key (coupon_status_id) REFERENCES coupon_status_lookup(coupon_status_lookup_id)
);


INSERT INTO coupon (coupon_code, coupon_status_id, coupon_price_pennies)
VALUES ('TRYFREE', 1, 0);