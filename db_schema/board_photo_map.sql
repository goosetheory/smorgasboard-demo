CREATE TABLE IF NOT EXISTS board_photo_map (
	board_photo_map_id  		BIGINT      NOT NULL    AUTO_INCREMENT,
	board_id            		BIGINT      NOT NULL,
	photo_id            		BIGINT      NOT NULL,
	board_photo_map_status_id	BIGINT		NOT NULL,
	add_date            		DATETIME    NOT NULL,

	PRIMARY KEY (board_photo_map_id),

	CONSTRAINT UC_board_photo_map_board_photo UNIQUE (board_id, photo_id),

	FOREIGN KEY (photo_id) REFERENCES  photo(photo_id),
	FOREIGN KEY (board_id)  REFERENCES  board(board_id),
	FOREIGN KEY	(board_photo_map_status_id) REFERENCES board_photo_map_status_lookup(board_photo_map_status_id)
);