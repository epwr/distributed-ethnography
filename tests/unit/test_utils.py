import pytest
from typing import Any

from app.utils import validate_survey_data


@pytest.mark.parametrize(
    "data",
    (
        {
            "name": "Survey Name",
            "is_open": "True",
            "question-0": "What's my name again?",
        },
        {
            "name": "Survey Name",
            "question-0": "What's my name again?",
            "question-1": "What's my name again?",
            "question-2": "What's my name again?",
        },
        {
            "name": "Survey Name",
        },
    ),
)
def test_validate_survey_data_returns_no_errors_on_correct_data(data: Any):
    error = validate_survey_data(data)

    assert error is None


@pytest.mark.parametrize(
    "data",
    (
        [],
        "Should be a dict",
        {
            "name": "Survey Name",
            "is_open": "True",
            "question-1": "What's my name again?",  # questions should be 0 indexed.
        },
        {
            "name": "Survey Name",
            "is_open": "bad value",
            "question-0": "What's my name again?",
        },
        {
            "name": "Survey Name",
            "is_open": "True",
            "question-0": "What's my name again?",
            "question-3": "What's my name again?",
        },  # question should have incrementing indices
        {
            "name": [],  # Name should be a string
            "is_open": "True",
            "question-0": "What's my name again?",
        },
        {
            "name": "Survey Name",
            "is_open": 8,  # is_open should be 'true' (or missing)
            "question-0": "What's my name again?",
        },
        {
            "name": "Survey Name",
            "question-0": [],  # questions should be a string
        },
        {
            "name": "Survey Name",
            "question-0": "Hello!",
            "question-1": [],  # questions should be a string
        },
        {
            "name": "Survey Name",
            "question-0": "Hello!",
            123: "Bad key",
        },
    ),
)
def test_validate_survey_data_returns_errors_on_incorrect_data(data: Any):
    error = validate_survey_data(data)

    assert error is not None
