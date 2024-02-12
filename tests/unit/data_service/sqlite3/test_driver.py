import sqlite3
import pytest
from uuid import UUID

from app.models import Survey


def test_sqlite3_driver_enforces_foreign_key_constraints(empty_db_driver):
    with empty_db_driver._get_cursor() as cursor:
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO question (uid, survey_uid, question) VALUES ("
                '    "ed7b2f97-cd9d-4786-9266-a9397172397b", '
                '    "f54e6029-a7bd-4b74-a4a4-e0bbbe1435eb", '
                '    "WHAT AM I???"'
                ");"
            )


def test_sqlite3_driver_can_get_list_open_surveys(populated_db_driver):
    surveys = populated_db_driver.get_open_surveys()

    assert len(surveys) == 1
    for survey in surveys:
        assert isinstance(survey, Survey)


@pytest.mark.parametrize(
    "survey_uid",
    (
        "00000000-9c88-4b81-9de4-bac7444fbb0a",
        "00000000-a087-4fb6-a123-24ff30263530",
    ),
)
def test_driver_get_survey_returns_appropriate_survey(populated_db_driver, survey_uid):
    survey = populated_db_driver.get_survey(survey_uid=survey_uid)
    assert survey is not None
    assert survey.uid == UUID(survey_uid)


@pytest.mark.parametrize(
    "survey_uid",
    (
        "99999999-9c88-4b81-9de4-bac7444fbb0a",
        "99999999-a087-4fb6-a123-24ff30263530",
    ),
)
def test_driver_get_survey_returns_none_when_no_survey_found(
    populated_db_driver, survey_uid
):
    survey = populated_db_driver.get_survey(survey_uid=UUID(survey_uid))
    assert survey is None


def test_sqlite3_driver_throws_error_if_adding_a_survey_that_already_exists(
    populated_db_driver,
):
    surveys = populated_db_driver.get_open_surveys()
    survey = surveys[0]

    with pytest.raises(sqlite3.IntegrityError):
        populated_db_driver.insert_survey(survey)


def test_sqlite3_driver_can_query_an_added_survey(
    empty_db_driver,
    new_survey_open,
):
    empty_db_driver.insert_survey(new_survey_open)

    surveys = empty_db_driver.get_open_surveys()

    assert len(surveys) == 1
    assert surveys[0] == new_survey_open
