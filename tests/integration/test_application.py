import pytest
from uuid import uuid4
from multiprocessing import Pool
from pathlib import Path

from app.data_service import DataService, Sqlite3Driver
from app.models import Survey


@pytest.fixture
def setup_data_service(monkeypatch, populated_db_driver):
    def patched_init(self, driver):
        self._driver = populated_db_driver

    monkeypatch.setattr("app.routes.DataService.__init__", patched_init)

    yield

    monkeypatch.undo()


class TestMutationEndpoints:
    test_cases = [
        (
            "post",
            "/surveys/new",
            {
                "name": "test mutable endpoints 1",
                "is_open": True,
                "questions": [],
            },
            "/surveys",
        ),
        (
            "post",
            "/surveys/new",
            {
                "name": "test mutable endpoints 2",
                "is_open": True,
                "question-0": "What's my name again?",
                "question-1": "What's you name again?",
                "question-2": "Why are we here again?",
            },
            "/surveys",
        ),
    ]

    @pytest.mark.parametrize("http_method, slug, data, read_endpoint", test_cases)
    def test_endpoint_changes_response_of_other_endpoint(
        self,
        app_client,
        setup_data_service,
        http_method: str,
        slug: str,
        data: dict[str, str],
        read_endpoint: str,
    ):
        initial_response = app_client.get(read_endpoint)
        mutation_response = app_client.__getattribute__(http_method)(slug, data=data)
        updated_response = app_client.get(read_endpoint)

        assert initial_response.status_code == 200
        assert mutation_response.status_code == 200
        assert updated_response.status_code == 200

        assert initial_response.data != updated_response.data


class TestDataPersistency:
    test_cases = [
        (
            "post",
            "/surveys/new",
            {"name": "test", "is_open": True, "question-0": "Hello there!"},
            "/surveys",
        ),
    ]

    @staticmethod
    def create_new_data_service(database_file: Path) -> DataService:
        return DataService(Sqlite3Driver(db_file=database_file))

    @staticmethod
    def create_survey_in_database(database_file: Path) -> None:
        data_service = TestDataPersistency.create_new_data_service(database_file)
        survey = Survey(name="Test Survey", is_open=True)
        data_service.insert_survey(survey)

    def test_different_data_services_interact_with_the_same_database(
        self,
    ):
        temp_file = Path("/tmp") / f"testing-{str(uuid4())}.sqlite"
        data_service = TestDataPersistency.create_new_data_service(temp_file)

        sql_setup_filename = Path(__file__).parents[2] / "data" / "setup.sql"
        with open(sql_setup_filename) as infile:
            query = infile.read()

        with data_service._driver._get_cursor() as cursor:
            cursor.executescript(query)

        with Pool(processes=5) as pool:
            pool.map(TestDataPersistency.create_survey_in_database, [temp_file] * 5)

        surveys = data_service.get_open_surveys()
        assert len(surveys) == 5
