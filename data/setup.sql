PRAGMA foreign_keys = ON;

CREATE TABLE survey (
	   uid TEXT PRIMARY KEY
	   , is_open BOOL
	   , name TEXT
);

CREATE TABLE survey_question (
	   uid TEXT PRIMARY KEY
	   , survey_uid TEXT
	   , question TEXT
);

CREATE TABLE survey_question (
	   uid TEXT PRIMARY KEY
	   , question_uid TEXT
	   , first_dimension TEXT
	   , second_dimension TEXT
	   , third_dimension TEXT
);
