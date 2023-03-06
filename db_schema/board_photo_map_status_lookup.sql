CREATE TABLE IF NOT EXISTS board_photo_map_status_lookup (
	board_photo_map_status_id	BIGINT		NOT NULL,
	name						VARCHAR(40)	NOT NULL,

	PRIMARY KEY (board_photo_map_status_id)
);

INSERT INTO board_photo_map_status_lookup (board_photo_map_status_id, name)
VALUES (1, 'ACTIVE'),
(2, 'REMOVED_BY_HOST')