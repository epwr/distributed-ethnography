import sqlite3
from pathlib import Path
import logging

from .model_factory import fetch_query_results_as_model
from app.models import Survey


class Sqlite3Driver:
    def __init__(self, db_file: Path) -> None:
        logging.info(f"Sql3Driver connecting to db_file '{db_file}'")

        self._connection = sqlite3.connect(db_file)
        self._connection.row_factory = sqlite3.Row

        # Ensure foreign key constraints are enforced on every connection
        cursor = self._get_cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

    def _get_cursor(self) -> sqlite3.Cursor:
        return self._connection.cursor()

    def get_open_surveys(self) -> list[Survey]:
        query = "SELECT * FROM survey WHERE is_open IS TRUE;"
        cursor = self._get_cursor()
        cursor.execute(query)
        result = fetch_query_results_as_model(cursor, Survey)

        return result

    def insert_survey(self, survey: Survey) -> None:
        query = "INSERT INTO survey (uid, name, is_open) VALUES (?, ?, ?)"

        cursor = self._get_cursor()
        cursor.execute(query, (str(survey.uid), survey.name, survey.is_open))
