from .sqlite3 import Sqlite3Driver
from .models import Survey

class DataService:

    def __init__(self, driver: Sqlite3Driver):
        self._driver = driver

    def get_open_surveys(self) -> list[Survey]:
        return self._driver.get_open_surveys()

