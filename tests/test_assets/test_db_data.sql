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

COMMIT;
