from app.data_service.models import Survey


def test_sqlite3_driver_enforces_foreign_key_constraints():

    assert False

    # TODO: mock and ensure that each new connection calls "PRAGMA foreign_keys = ON;".
    # TODO: maybe it's easier to just check if I can insert something that doesn't match FK constraints?


def test_sqlite3_driver_can_get_list_open_surveys(test_database_driver):

    surveys = test_database_driver.get_open_surveys()

    assert len(surveys) == 1
    for survey in surveys:
        assert isinstance(survey, Survey)
