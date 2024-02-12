import pytest
from pathlib import Path
from uuid import uuid4

from app.routes import app
from app.data_service.sqlite3 import Sqlite3Driver
from app.models import Survey


@pytest.fixture
def asset_path() -> Path:
    return Path(__file__).parent / "test_assets"


@pytest.fixture
def empty_db_driver(asset_path) -> Sqlite3Driver:
    driver = Sqlite3Driver(Path("/tmp") / f"testing-{uuid4()}.sqlite")

    sql_setup_filename = Path(__file__).parents[1] / "data" / "setup.sql"
    with open(sql_setup_filename) as infile:
        query = infile.read()

    with driver._get_cursor() as cursor:
        cursor.executescript(query)

    return driver


@pytest.fixture
def populated_db_driver(
    empty_db_driver: Sqlite3Driver, asset_path: Path
) -> Sqlite3Driver:
    initial_data_filename = asset_path / "test_db_data.sql"
    with open(initial_data_filename) as infile:
        query = infile.read()

    with empty_db_driver._get_cursor() as cursor:
        cursor.executescript(query)

    return empty_db_driver


@pytest.fixture
def app_client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def new_survey_open():
    # survey with a random UUID
    return Survey(
        name="Test Survey",
        is_open=True,
    )
