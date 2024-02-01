import pytest
from pathlib import Path

from app.config import settings
from app.data_service.sqlite3 import Sqlite3Driver


@pytest.fixture
def asset_path():

    return Path(__file__).parent / "test_assets"


@pytest.fixture
def test_database_driver(asset_path):

    driver = Sqlite3Driver(settings.sqlite_file)
    cursor = driver._connection.cursor()
    
    sql_setup_filename = Path(__file__).parents[1] / 'data' / 'setup.sql'
    with open(sql_setup_filename) as infile:
        query = infile.read()
    cursor.executescript(query)

    initial_data_filename = asset_path / "test_db_data.sql"
    with open(initial_data_filename) as infile:
        query = infile.read()
    cursor.executescript(query)

    return driver

