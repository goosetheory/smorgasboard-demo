CREATE TABLE IF NOT EXISTS archive_shard (
    archive_shard_id		BIGINT		NOT NULL	AUTO_INCREMENT,
    archive_id    			BIGINT		NOT NULL,
    s3_bucket_name			VARCHAR(63)	NOT NULL,
    s3_object_key			VARCHAR(63)	NOT NULL,

    PRIMARY KEY (archive_shard_id),

    FOREIGN KEY (archive_id) REFERENCES archive(archive_id)
);