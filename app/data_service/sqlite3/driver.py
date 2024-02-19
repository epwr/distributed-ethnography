import sqlite3
from pathlib import Path
from typing import Generator
from contextlib import contextmanager
from uuid import UUID

from .model_factory import fetch_query_results_as_model
from app.models import Survey, TextQuestion


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

    def get_survey(self, survey_uid: UUID) -> Survey | None:
        query = "SELECT * FROM survey WHERE uid = ? LIMIT 1;"

        with self._get_cursor() as cursor:
            cursor.execute(query, (str(survey_uid),))
            result = fetch_query_results_as_model(cursor, Survey)

        if len(result) > 0:
            return result[0]
        return None

    def insert_survey(self, survey: Survey) -> None:
        query = "INSERT INTO survey (uid, name, is_open) VALUES (?, ?, ?)"

        with self._get_cursor() as cursor:
            cursor.execute(query, (str(survey.uid), survey.name, survey.is_open))

    def get_text_question(self, question_uid: UUID) -> TextQuestion | None:
        query = "SELECT * FROM text_question WHERE uid = ? LIMIT 1;"

        with self._get_cursor() as cursor:
            cursor.execute(query, (str(question_uid),))
            result = fetch_query_results_as_model(cursor, TextQuestion)

        if len(result) > 0:
            return result[0]
        return None

    def get_text_questions_from_survey(self, survey_uid: UUID) -> list[TextQuestion]:
        query = "SELECT * FROM text_question WHERE survey_uid = ?;"

        with self._get_cursor() as cursor:
            cursor.execute(query, (str(survey_uid),))
            results = fetch_query_results_as_model(cursor, TextQuestion)

        return results
