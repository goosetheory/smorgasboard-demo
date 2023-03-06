CREATE TABLE IF NOT EXISTS coupon_status_lookup (
	coupon_status_lookup_id	BIGINT		NOT NULL,
	name					VARCHAR(40)	NOT NULL,

	PRIMARY KEY (coupon_status_lookup_id)
);

INSERT INTO coupon_status_lookup	(coupon_status_lookup_id, name)
VALUES	(1, 'ACTIVE'),
		(2, 'DISABLED');