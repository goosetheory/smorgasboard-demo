CREATE TABLE IF NOT EXISTS board_type_lookup (
	board_type_id	BIGINT		NOT NULL,
	name			VARCHAR(40)	NOT NULL,

	PRIMARY KEY (board_type_id)
);

INSERT INTO board_type_lookup (board_type_id, name)
VALUES 	(1, 'FREE_TRIAL'),
		(2, 'STANDARD');