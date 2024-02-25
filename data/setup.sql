BEGIN;

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS survey (
	   uid TEXT PRIMARY KEY
	   , is_open BOOL
	   , name TEXT
);

CREATE TABLE IF NOT EXISTS text_question (
	   uid TEXT PRIMARY KEY
	   , survey_uid TEXT
	   , question TEXT
	   , FOREIGN KEY(survey_uid) REFERENCES survey(uid)
);

CREATE TABLE IF NOT EXISTS dimensional_question (
	   uid TEXT PRIMARY KEY
	   , survey_uid TEXT
	   , question TEXT
	   , dimension_one TEXT
	   , dimension_two TEXT
	   , dimension_three TEXT
	   , FOREIGN KEY(survey_uid) REFERENCES survey(uid)
);

COMMIT;
