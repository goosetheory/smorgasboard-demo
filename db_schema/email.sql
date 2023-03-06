CREATE TABLE IF NOT EXISTS email (
	email_id			BIGINT		NOT NULL	AUTO_INCREMENT,
	email_type_id		BIGINT		NOT NULL,
	recipient_person_id	BIGINT		NOT NULL,
	board_id			BIGINT		NULL,
	sent_date			DATETIME	NOT NULL,
	message_id			VARCHAR(61)	NOT NULL,

	PRIMARY KEY (email_id),

	FOREIGN KEY (email_type_id) REFERENCES email_type_lookup(email_type_id),
	FOREIGN KEY (recipient_person_id) REFERENCES person(person_id),
	FOREIGN KEY (board_id) REFERENCES board(board_id)
);