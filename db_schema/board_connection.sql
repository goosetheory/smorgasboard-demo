CREATE TABLE IF NOT EXISTS board_connection (
	board_connection_id			BIGINT			NOT NULL	AUTO_INCREMENT,
	ws_connection_id			VARCHAR(32)		NOT NULL	UNIQUE,
	board_id					BIGINT			NOT NULL,
	board_connection_status_id	BIGINT			NOT NULL,
	begin_date					DATETIME		NOT NULL,
	end_date					DATETIME		NULL,

	PRIMARY KEY (board_connection_id),
	FOREIGN KEY (board_id) REFERENCES board(board_id),
	FOREIGN KEY (board_connection_status_id) REFERENCES board_connection_status_lookup(board_connection_status_id)
)