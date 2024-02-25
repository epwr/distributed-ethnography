BEGIN;

INSERT INTO survey (
	   uid
	   , is_open
	   , name
) VALUES (
  "00000000-9c88-4b81-9de4-bac7444fbb0a"
  , false
  , "Closed Test Survey"
),
(
  "00000000-a087-4fb6-a123-24ff30263530"
  , true
  , "Open Test Survey - 1Q"
),
(
  "00000000-b37a-32b3-19d9-72ec921021e3"
  , true
  , "Open Test Survey - 2Qs"
),
(
  "00000000-0762-4fd1-b927-65ddb494e04f"
  , true
  , "Open Test Survey - 1DQ"
),
(
  "00000000-e253-4c39-b32b-eeb4f8e8711d"
  , true
  , "Open Test Survey - 2DQ"
);

INSERT INTO text_question (
	   uid
	   , survey_uid
	   , question
) VALUES (
  "11111111-9c88-4b81-9de4-bac7444fbb0a"
  , "00000000-9c88-4b81-9de4-bac7444fbb0a"
  , "What story would you tell your best friend about this company?"
),
(
  "11111111-a087-4fb6-a123-24ff30263530"
  , "00000000-a087-4fb6-a123-24ff30263530"
  , "What stands out to you about current quarterly plan?"
),
(
  "11111111-b37a-32b3-19d9-72ec921021e3"
  , "00000000-b37a-32b3-19d9-72ec921021e3"
  , "What story?"
),
(
  "11111111-b37a-44a1-19d9-72ec921021e3"
  , "00000000-b37a-32b3-19d9-72ec921021e3"
  , "What story?"
);

INSERT INTO dimensional_question (
	   uid
	   , survey_uid
	   , question
	   , dimension_one
	   , dimension_two
	   , dimension_three
) VALUES (
  "11111111-3e01-4b2c-b396-1b20facf99c2"
  , "00000000-9c88-4b81-9de4-bac7444fbb0a"
  , "How would you describe your manager on the following dimensions?"
  , "Empathetic"
  , "Motivational"
  , "Knowledgable"
),
(
  "11111111-2b47-4d02-8c48-0fa65f0da016"
  , "00000000-0762-4fd1-b927-65ddb494e04f"
  , "What came across in your last interaction with the CEO?"
  , "Purpose"
  , "Audacity"
  , "Clarity of Direction"
),
(
  "11111111-041a-490d-a60c-82babc856120"
  , "00000000-e253-4c39-b32b-eeb4f8e8711d"
  , "How would you describe your manager on the following dimensions?"
  , "Empathetic"
  , "Motivational"
  , "Knowledgable"
),
(
  "11111111-b36f-4e80-aba4-9707a10d6acf"
  , "00000000-e253-4c39-b32b-eeb4f8e8711d"
  , "What came across in your last interaction with the CEO?"
  , "Purpose"
  , "Audacity"
  , "Clarity of Direction"
);

COMMIT;
