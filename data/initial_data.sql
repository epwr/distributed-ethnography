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
  , 'What story would you tell your best friend about this company?'
);

INSERT INTO dimensional_question (
  uid
  , survey_uid
  , question
  , dimension_one
  , dimension_two	
  , dimension_three
) VALUES (
  "4ccfc2b3-c18a-4c86-b918-1f30efdfeea2"
  , "4b5bfb06-2060-4abf-b5fd-3bae5dcf72b9"
  , "How strongly does this story demonstrate the following values?"
  , "Empathy to Colleagues"
  , "Service to Others"
  , "Individual Growth"
),
(
  "a6938e91-e7cc-4048-9b77-8cbba8d735cd"
  , "4b5bfb06-2060-4abf-b5fd-3bae5dcf72b9"
  , "How strongly does this story demonstrate the following values?"
  , "Accountability"
  , "Efficiency"
  , "Individual Growth"
);
