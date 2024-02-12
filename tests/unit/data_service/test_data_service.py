import pytest
from unittest.mock import Mock

from app.data_service import DataService
from app.data_service.sqlite3 import Sqlite3Driver
from app.models import Survey


@pytest.fixture
def surveys() -> list[Survey]:
    return [
        Survey(
            name="test survey",
            is_open=True,
        )
    ]


@pytest.fixture
def data_service(surveys) -> DataService:
    mock_driver = Mock(spec=Sqlite3Driver)

    mock_driver.get_open_surveys.return_value = surveys
    mock_driver.insert_survey.return_value = None

    return DataService(driver=mock_driver)


def test_data_service_can_return_all_open_surveys(
    data_service: DataService, surveys: list[Survey]
):
    returned_surveys = data_service.get_open_surveys()

    assert len(surveys) == len(returned_surveys)

    for survey in returned_surveys:
        assert survey in surveys


def test_data_service_can_insert_a_survey(
    data_service: DataService, new_survey_open: Survey
):
    data_service.insert_survey(new_survey_open)
    data_service._driver.insert_survey.assert_called_once_with(new_survey_open)
