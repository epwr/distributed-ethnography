import sqlite3
from pathlib import Path
from typing import Generator
from contextlib import contextmanager

from .model_factory import fetch_query_results_as_model
from app.models import Survey


class Sqlite3Driver:
    def __init__(self, db_file: Path) -> None:
        self._db_file = db_file

    @contextmanager
    def _get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        connection = sqlite3.connect(self._db_file)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        yield cursor
        connection.commit()

    def get_open_surveys(self) -> list[Survey]:
        query = "SELECT * FROM survey WHERE is_open IS TRUE;"

        with self._get_cursor() as cursor:
            cursor.execute(query)
            result = fetch_query_results_as_model(cursor, Survey)

        return result

    def insert_survey(self, survey: Survey) -> None:
        query = "INSERT INTO survey (uid, name, is_open) VALUES (?, ?, ?)"

        with self._get_cursor() as cursor:
            cursor.execute(query, (str(survey.uid), survey.name, survey.is_open))
