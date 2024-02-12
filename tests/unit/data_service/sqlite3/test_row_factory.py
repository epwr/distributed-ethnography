import pytest
from uuid import UUID

from app.data_service.sqlite3 import Sqlite3Driver
from app.data_service.sqlite3.model_factory import fetch_query_results_as_model
from app.models import Survey


@pytest.mark.parametrize(
    "records, expected_length",
    [
        ([("test_name 1", False, "42c19f90-2e81-48d9-b194-a1611c999836")], 1),
        ([("garbalaksdc", True, "99c19f90-2e81-48d9-b194-a1611c999836")], 1),
        (
            [
                ("test_name 1", False, "00c19f90-2e81-48d9-b194-a1611c999836"),
                ("garbalaksdc", True, "01c19f90-2e81-48d9-b194-a1611c999836"),
            ],
            2,
        ),
        ([], 0),
    ],
)
def test_convert_sqlite3_row_to_survey_model(
    empty_db_driver: Sqlite3Driver, records: tuple, expected_length: int
):
    with empty_db_driver._get_cursor() as cursor:
        for record in records:
            name = record[0]
            is_open = record[1]
            uid = record[2]

            cursor.execute(
                "INSERT INTO survey (uid, name, is_open) VALUES "
                f'("{uid}", "{name}", {is_open} );'
            )

        cursor.execute("SELECT * FROM survey;")
        surveys = fetch_query_results_as_model(cursor, Survey)

    assert len(surveys) == expected_length

    for survey in surveys:
        assert isinstance(survey, Survey)
        assert isinstance(survey.is_open, bool)
        assert isinstance(survey.uid, UUID)
        assert isinstance(survey.name, str)
