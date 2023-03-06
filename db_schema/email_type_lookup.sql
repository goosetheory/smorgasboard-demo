CREATE TABLE IF NOT EXISTS email_type_lookup(
	email_type_id		BIGINT		NOT NULL,
	name				VARCHAR(40)	NOT NULL,

	PRIMARY KEY	(email_type_id)
);

INSERT INTO email_type_lookup(email_type_id, name)
VALUES
	(1, 'ON_JOIN'),
	(2, 'ON_PAY_FOR_BOARD'),
	(3, 'ON_BOARD_START'),
	(4, 'ON_BOARD_END'),
	(5, 'ON_FREE_TRIAL_END');
