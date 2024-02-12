BEGIN;

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS survey (
	   uid TEXT PRIMARY KEY
	   , is_open BOOL
	   , name TEXT
);

CREATE TABLE IF NOT EXISTS question (
	   uid TEXT PRIMARY KEY
	   , survey_uid TEXT
	   , question TEXT
	   , FOREIGN KEY(survey_uid) REFERENCES survey(uid)
);

CREATE TABLE IF NOT EXISTS ranking (
	   uid TEXT PRIMARY KEY
	   , question_uid TEXT
	   , first_dimension TEXT
	   , second_dimension TEXT
	   , third_dimension TEXT
	   , FOREIGN KEY(question_uid) REFERENCES question(uid)
);

COMMIT;
