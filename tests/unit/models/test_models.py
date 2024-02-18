import pytest

from app.models import Survey, Question


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
        [Question, {"question": "How are you today?"}],  # .uid should be optional
        [
            Question,
            {
                "uid": "bb92a5f5-7d62-4e77-9cbb-c8c903c4e65f",
                "question": "How are you today?",
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
            Question(question="What is?"),
            Question(question="What is?"),
            False,
        ),  # UIDs should be different
        (
            Question(question="What is?", uid="aa11a5f5-7d42-4e77-9cbb-c8c903c4e65f"),
            Question(question="What is?", uid="aa11a5f5-7d42-4e77-9cbb-c8c903c4e65f"),
            True,
        ),
        (
            Question(
                uid="aa11a5f5-7d42-4e77-9cbb-c8c903c4e65f",
                question="What is?",
            ),
            Survey(
                uid="aa11a5f5-7d42-4e77-9cbb-c8c903c4e65f", name="Test", is_open=True
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
