CREATE TABLE IF NOT EXISTS person (
  person_id         BIGINT          NOT NULL    AUTO_INCREMENT,
  email_address     NVARCHAR(320)   NOT NULL    UNIQUE,
  cognito_username  BINARY(16)      NOT NULL    UNIQUE,
  given_name        NVARCHAR(40)    NOT NULL,
PRIMARY KEY (person_id));