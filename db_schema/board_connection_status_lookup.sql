CREATE TABLE IF NOT EXISTS board_connection_status_lookup (
	board_connection_status_id		BIGINT		NOT NULL,
	name							VARCHAR(40)	NOT NULL,

	PRIMARY KEY (board_connection_status_id)
);

INSERT INTO board_connection_status_lookup (board_connection_status_id, name)
VALUES	(1, 'CONNECTED'),
		(2, 'DISCONNECTED');