import pytest
from unittest.mock import Mock
from uuid import UUID

from app.data_service import DataService
from app.data_service.sqlite3 import Sqlite3Driver
from app.models import Survey, TextQuestion


@pytest.fixture
def surveys() -> list[Survey]:
    return [
        Survey(
            uid=UUID("74bce4cf-0875-471b-a7c4-f25c7ef42864"),
            name="test survey",
            is_open=True,
        )
    ]


@pytest.fixture
def questions() -> list[TextQuestion]:
    return [
        TextQuestion(
            question="What's up?",
            survey_uid=UUID("74bce4cf-0875-471b-a7c4-f25c7ef42864"),
        )
    ]


@pytest.fixture
def data_service(surveys) -> DataService:
    mock_driver = Mock(spec=Sqlite3Driver)

    mock_driver.get_open_surveys.return_value = surveys
    mock_driver.insert_survey.return_value = None

    return DataService(driver=mock_driver)


class TestDataServiceSurveyMethods:
    def test_get_open_surveys_returns_all_open_surveys(
        self, data_service: DataService, surveys: list[Survey]
    ):
        returned_surveys = data_service.get_open_surveys()

        assert len(surveys) == len(returned_surveys)

        for survey in returned_surveys:
            assert survey in surveys

    def test_get_survey_returns_one_survey_if_exists(
        self,
        data_service: DataService,
    ):
        survey = Survey(name="test", is_open=True)
        data_service._driver.get_survey.return_value = survey

        returned_survey = data_service.get_survey(survey.uid)
        assert returned_survey == survey

    def test_get_survey_returns_none_if_no_survey(
        self,
        data_service: DataService,
    ):
        data_service._driver.get_survey.return_value = None
        survey = data_service.get_survey(UUID("99999999-9c88-4b81-9de4-bac7444fbb0a"))
        assert survey is None

    def test_get_survey_if_open_returns_one_survey_if_open(
        self,
        data_service: DataService,
    ):
        survey = Survey(name="test", is_open=True)
        data_service._driver.get_survey.return_value = survey

        returned_survey = data_service.get_survey_if_open(survey.uid)
        assert returned_survey == survey

    def test_get_survey_if_open_returns_none_if_survey_closed(
        self,
        data_service: DataService,
    ):
        survey = Survey(name="test", is_open=False)
        data_service._driver.get_survey.return_value = survey

        returned_survey = data_service.get_survey_if_open(survey.uid)
        assert returned_survey is None

    def test_can_insert_a_survey(
        self, data_service: DataService, new_survey_open: Survey
    ):
        data_service.insert_survey(new_survey_open)
        data_service._driver.insert_survey.assert_called_once_with(new_survey_open)
