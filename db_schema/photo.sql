CREATE TABLE IF NOT EXISTS photo (
	photo_id        BIGINT          NOT NULL    AUTO_INCREMENT,
	photo_key		BINARY(16)		NOT NULL	UNIQUE,
	s3_bucket_name  VARCHAR(63)	    NOT NULL,
	s3_object_key	VARCHAR(63)		NOT NULL,
	uploader_id     BIGINT          NULL,
	upload_date		DATETIME        NOT NULL,

	PRIMARY KEY (photo_id),
	FOREIGN KEY (uploader_id) REFERENCES person(person_id)
)