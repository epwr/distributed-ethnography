import pytest
from pathlib import Path
from uuid import uuid4, UUID

from app.routes import app
from app.data_service.sqlite3 import Sqlite3Driver
from app.models import Survey, TextQuestion


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
def new_open_survey() -> Survey:
    return Survey(
        uid=UUID("f21ccd82-83d6-40bc-8e60-703382f73860"),
        name="Test Survey",
        is_open=True,
    )


@pytest.fixture
def existing_open_survey() -> Survey:
    return Survey(
        uid=UUID("00000000-a087-4fb6-a123-24ff30263530"),
        name="Open Test Survey - 1Q",
        is_open=True,
    )


@pytest.fixture
def new_text_question() -> TextQuestion:
    return TextQuestion(
        uid=UUID("fd3d76f5-96a0-42a6-92d6-cbc55ef1d79f"),
        survey_uid=UUID("f21ccd82-83d6-40bc-8e60-703382f73860"),
        question="When is it time?",
    )
