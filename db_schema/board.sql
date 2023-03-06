CREATE TABLE IF NOT EXISTS board (
    board_id        BIGINT          NOT NULL    AUTO_INCREMENT,
    owner_id        BIGINT          NOT NULL,
    board_name      NVARCHAR(64)    NOT NULL,
    join_code       BINARY(16)      NOT NULL,
    board_status_id BIGINT			NOT NULL DEFAULT 2, -- Default is not_started
    board_type_id	BIGINT			NOT NULL DEFAULT 2,	-- Default is standard
    start_date		DATETIME		NULL,
    end_date		DATETIME		NULL,

    PRIMARY KEY (board_id),
    FOREIGN KEY (owner_id) REFERENCES person(person_id),
    FOREIGN KEY (board_status_id) REFERENCES board_status_lookup(board_status_lookup_id),
    FOREIGN KEY (board_type_id) REFERENCES board_type_lookup(board_type_id)
);
