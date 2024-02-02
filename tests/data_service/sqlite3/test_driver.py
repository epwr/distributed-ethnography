import sqlite3
import pytest

from app.data_service.models import Survey


def test_sqlite3_driver_enforces_foreign_key_constraints(empty_db_driver):

    cursor = empty_db_driver._get_cursor()

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
