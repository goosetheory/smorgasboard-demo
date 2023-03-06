CREATE TABLE IF NOT EXISTS board_status_lookup (
	board_status_lookup_id	BIGINT		NOT NULL,
	name					VARCHAR(40)	NOT NULL,

	PRIMARY KEY (board_status_lookup_id)
);

INSERT INTO board_status_lookup (board_status_lookup_id, name)
VALUES	(1, 'ACTIVE'),
		(2, 'NOT_STARTED'),
		(3, 'COMPLETED');