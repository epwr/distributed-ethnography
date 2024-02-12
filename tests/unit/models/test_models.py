import pytest

from app.models import Survey


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
    ),
)
def test_equality_function_works_on_all_functions(value1, value2, expected):
    result = value1 == value2
    assert result == expected
