import pytest

from app.data_service import DataService
from app.data_service.models import Survey


@pytest.fixture
def data_service(populated_db_driver) -> DataService:

    return DataService(
        driver=populated_db_driver
    )

def test_data_service_can_return_all_open_surveys(data_service: DataService):

    surveys = data_service.get_open_surveys()

    assert len(surveys) == len(data_service._driver.get_open_surveys())
    
    for survey in surveys:
        assert isinstance(survey, Survey)

def test_data_service_can_insert_a_survey(data_service: DataService, test_survey_open: Survey):

    data_service.insert_survey(test_survey_open)

    surveys = data_service.get_open_surveys()
    matched_surveys = [
        survey
        for survey in surveys
        if survey.uid == test_survey_open.uid
    ]

    assert len(matched_surveys) == 1
