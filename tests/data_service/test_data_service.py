import pytest

from app.data_service import DataService
from app.data_service.models import Survey


@pytest.fixture
def data_service(populated_database_driver) -> DataService:

    return DataService(
        driver=populated_database_driver
    )

def test_data_service(data_service):

    surveys = data_service.get_open_surveys()

    for survey in surveys:
        assert isinstance(survey, Survey)
