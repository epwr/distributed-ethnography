from uuid import UUID

from app.data_service.sqlite3.model_factory import convert_row_to_model
from app.data_service.models import Survey


def test_convert_sqlite3_row_to_survey_model(test_database_driver):

    cursor = test_database_driver._connection.cursor()
    survey_results = cursor.execute("SELECT * FROM survey;").fetchall()

    for row in survey_results:

        survey = convert_row_to_model(Survey, row)

        assert isinstance(survey, Survey)
        assert survey.is_open == row['is_open']
        assert survey.uid == UUID(row['uid'])
        assert survey.name == row['name']
