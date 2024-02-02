import pytest
from uuid import UUID

from app.data_service.sqlite3.model_factory import fetch_query_results_as_model
from app.data_service.models import Survey


@pytest.mark.parametrize("name, is_open, uid", [
    ('test_name 1', False, '48c19f90-2e81-48d9-b194-a1611c999836'),
    ('garbalaksdc', True,  '48c19f90-2e81-48d9-b194-a1611c999836'),
])
def test_convert_sqlite3_row_to_survey_model(empty_db_driver, uid, name, is_open):

    cursor = empty_db_driver._connection.cursor()
    cursor.execute(
        "INSERT INTO survey (uid, name, is_open) VALUES "
        f'("{uid}", "{name}", {is_open} );'
    )
    cursor.execute("SELECT * FROM survey;")
    
    surveys = fetch_query_results_as_model(cursor, Survey)

    assert len(surveys) == 1

    survey = surveys[0]
    assert isinstance(survey, Survey)
    assert isinstance(survey.is_open, bool)
    assert survey.is_open == is_open
    assert isinstance(survey.uid, UUID)
    assert survey.uid == UUID(uid)
    assert isinstance(survey.name, str)
    assert survey.name == name
