CREATE TABLE IF NOT EXISTS archive (
	archive_id		BIGINT		NOT NULL	AUTO_INCREMENT,
	board_id 		BIGINT		NOT NULL,
	create_date		DATETIME	NOT NULL,

	PRIMARY KEY (archive_id),

	CONSTRAINT UC_archive_board UNIQUE (board_id),
	FOREIGN KEY	(board_id) REFERENCES board(board_id)
);