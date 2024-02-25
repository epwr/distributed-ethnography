from uuid import UUID

from .sqlite3 import Sqlite3Driver
from app.models import Survey, TextQuestion, DimensionalQuestion


class DataService:
    def __init__(self, driver: Sqlite3Driver):
        self._driver = driver

    def get_open_surveys(self) -> list[Survey]:
        return self._driver.get_open_surveys()

    def get_survey(self, survey_uid: UUID) -> Survey | None:
        return self._driver.get_survey(survey_uid=survey_uid)

    def get_survey_if_open(self, survey_uid: UUID) -> Survey | None:
        survey = self.get_survey(survey_uid=survey_uid)
        if survey is not None and survey.is_open:
            return survey
        return None

    def insert_survey(self, survey: Survey) -> None:
        return self._driver.insert_survey(survey=survey)

    def get_text_question(self, question_uid: UUID) -> TextQuestion | None:
        return self._driver.get_text_question(question_uid=question_uid)

    def get_text_questions_from_survey(self, survey_uid: UUID) -> list[TextQuestion]:
        return self._driver.get_text_questions_from_survey(survey_uid=survey_uid)

    def insert_text_question(self, text_question: TextQuestion) -> None:
        self._driver.insert_text_question(text_question=text_question)

    def get_dimensional_question(
        self, question_uid: UUID
    ) -> DimensionalQuestion | None:
        return self._driver.get_dimensional_question(question_uid=question_uid)

    def get_dimensional_questions_from_survey(
        self, survey_uid: UUID
    ) -> list[DimensionalQuestion]:
        return self._driver.get_dimensional_questions_from_survey(survey_uid=survey_uid)
