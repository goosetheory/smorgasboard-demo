CREATE TABLE IF NOT EXISTS payment_status_lookup (
	payment_status_lookup_id	BIGINT		NOT NULL,
	name						VARCHAR(40)	NOT NULL,

	PRIMARY KEY (payment_status_lookup_id)
);

INSERT INTO payment_status_lookup (payment_status_lookup_id, name)
VALUES	(1, 'INCOMPLETE'),
		(2, 'SUCCEEDED'),
		(3, 'CONSUMED'),
		(4, 'REFUNDED');
