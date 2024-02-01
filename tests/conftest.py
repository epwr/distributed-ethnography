import pytest
from pathlib import Path

from app.config import settings
from app.data_service.sqlite3_driver import Sqlite3Driver

@pytest.fixture
def test_database_driver():

    driver = Sqlite3Driver(settings.sqlite_file)

    sql_setup_filename = Path(__file__).parents[1] / 'data' / 'setup.sql'
    with open(sql_setup_filename) as infile:
        query = infile.read()
    
    cursor = driver._connection.cursor()
    cursor.execute(query)

    return driver

