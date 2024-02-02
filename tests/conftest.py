import pytest
from pathlib import Path

from app.config import settings
from app.data_service.sqlite3 import Sqlite3Driver
from app.data_service import DataService


@pytest.fixture
def asset_path() -> Path:

    return Path(__file__).parent / "test_assets"


@pytest.fixture
def empty_database_driver(asset_path) -> Sqlite3Driver:

    driver = Sqlite3Driver(settings.sqlite_file)
    cursor = driver._connection.cursor()
    
    sql_setup_filename = Path(__file__).parents[1] / 'data' / 'setup.sql'
    with open(sql_setup_filename) as infile:
        query = infile.read()
    cursor.executescript(query)

    return driver

@pytest.fixture
def populated_database_driver(empty_database_driver: Sqlite3Driver, asset_path: Path) -> Sqlite3Driver:

    cursor = empty_database_driver._connection.cursor()
    
    initial_data_filename = asset_path / "test_db_data.sql"
    with open(initial_data_filename) as infile:
        query = infile.read()
    cursor.executescript(query)

    return empty_database_driver


@pytest.fixture
def patch_data_service(populated_database_driver, monkeypatch):

    patched_data_service = DataService(
        driver=populated_database_driver
    )
    
    with monkeypatch.context() as m:
        print("PATCHING DRIVER")
        m.setattr('app.routes.data_service', patched_data_service)
        yield
    
