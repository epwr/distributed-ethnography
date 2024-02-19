INSERT INTO survey (
  uid
  , name
  , is_open
) VALUES (
  '4b5bfb06-2060-4abf-b5fd-3bae5dcf72b9'
  , 'Example Survey #1'
  , TRUE
);

INSERT INTO text_question (
  uid
  , survey_uid
  , question
) VALUES (
  '9c9facb5-f360-4155-852a-8e2ac04607ea'
  , '4b5bfb06-2060-4abf-b5fd-3bae5dcf72b9'
  , 'What is your name?'
), (
  'ee947616-3d16-4095-bc8f-603be72022d3'
  , '4b5bfb06-2060-4abf-b5fd-3bae5dcf72b9'
  , 'Are you sure?'
);
