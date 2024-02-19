import pytest

from app.models import Survey, TextQuestion


@pytest.mark.parametrize(
    "model_class, arguments",
    [
        [
            Survey,
            {
                "uid": "bb92a5f5-7d62-4e77-9cbb-c8c903c4e65f",  # type uuid.UUID
                "is_open": True,
                "name": "Test Survey",
            },
        ],
        [Survey, {"is_open": True, "name": "Test Survey"}],  # .uid should be optional
        [
            TextQuestion,
            {
                "question": "How are you today?",
                "survey_uid": "63163031-ce99-46c3-a70b-c3df75a51258",
            },
        ],  # .uid should be optional
        [
            TextQuestion,
            {
                "uid": "bb92a5f5-7d62-4e77-9cbb-c8c903c4e65f",
                "question": "How are you today?",
                "survey_uid": "63163031-ce99-46c3-a70b-c3df75a51258",
            },
        ],  # type cast uid
    ],
)
def test_all_models_enforce_type_hints(model_class, arguments):
    model = model_class(**arguments)
    for key in arguments.keys():
        # Check that the value in model object is of the correct type
        value_type = model.__annotations__[key]
        assert model.__getattribute__(key) == value_type(arguments[key])

    # Check that all models fields are set
    for key in model.__annotations__.keys():
        assert model.__getattribute__(key) is not None


@pytest.mark.parametrize(
    "value1, value2, expected",
    (
        (Survey(name="Test", is_open=True), 5, False),
        (Survey(name="Test", is_open=True), Survey(name="Test", is_open=True), False),
        (
            Survey(
                uid="bb92a5f5-7d62-4e77-9cbb-c8c903c4e65f", name="Test", is_open=True
            ),
            Survey(
                uid="bb92a5f5-7d62-4e77-9cbb-c8c903c4e65f", name="Test", is_open=True
            ),
            True,
        ),
        (
            TextQuestion(
                question="What is?",
                survey_uid="63163031-ce99-46c3-a70b-c3df75a51258",
            ),
            TextQuestion(
                question="What is?",
                survey_uid="63163031-ce99-46c3-a70b-c3df75a51258",
            ),
            False,
        ),  # UIDs should be different
        (
            TextQuestion(
                question="What is?",
                uid="aa11a5f5-7d42-4e77-9cbb-c8c903c4e65f",
                survey_uid="63163031-ce99-46c3-a70b-c3df75a51258",
            ),
            TextQuestion(
                question="What is?",
                uid="aa11a5f5-7d42-4e77-9cbb-c8c903c4e65f",
                survey_uid="63163031-ce99-46c3-a70b-c3df75a51258",
            ),
            True,
        ),
        (
            TextQuestion(
                uid="aa11a5f5-7d42-4e77-9cbb-c8c903c4e65f",
                question="What is?",
                survey_uid="63163031-ce99-46c3-a70b-c3df75a51258",
            ),
            Survey(
                uid="63163031-ce99-46c3-a70b-c3df75a51258", name="Test", is_open=True
            ),
            False,
        ),
    ),
)
def test_equality_function_works_on_all_functions(value1, value2, expected):
    """
    Equality of these models means that all fields have the same values.
    """
    result = value1 == value2
    assert result == expected
