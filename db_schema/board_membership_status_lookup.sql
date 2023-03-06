CREATE TABLE IF NOT EXISTS board_membership_status_lookup (
	board_membership_status_id	BIGINT			NOT NULL,
	name						VARCHAR(40)		NOT NULL,

	PRIMARY KEY (board_membership_status_id)
);


INSERT INTO board_membership_status_lookup (board_membership_status_id, name)
VALUES 	(1, 'ACTIVE'),
		(2, 'REMOVED'),
		(3, 'LEFT'),
		(4, 'BANNED'),
		(5, 'INACTIVE')
