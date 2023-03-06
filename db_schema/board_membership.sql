CREATE TABLE IF NOT EXISTS board_membership (
	board_membership_id 		BIGINT  	NOT NULL    AUTO_INCREMENT,
	join_date           		DATETIME	NOT NULL,
	person_id           		BIGINT  	NOT NULL,
	board_id            		BIGINT  	NOT NULL,
	board_membership_status_id	BIGINT		NOT NULL,

	PRIMARY KEY (board_membership_id),

	CONSTRAINT UC_board_membership_person_board UNIQUE (person_id, board_id),

	FOREIGN KEY (person_id) REFERENCES  person(person_id),
	FOREIGN KEY (board_id)  REFERENCES  board(board_id),
	FOREIGN KEY (board_membership_status_id) REFERENCES board_membership_status_lookup(board_membership_status_id)
);
