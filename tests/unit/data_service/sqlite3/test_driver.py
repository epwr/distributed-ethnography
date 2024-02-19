import sqlite3
import pytest
from uuid import UUID

from app.models import Survey, TextQuestion
from app.data_service.sqlite3 import Sqlite3Driver


class TestDriver:
    def test_sqlite3_driver_enforces_foreign_key_constraints(self, empty_db_driver):
        with empty_db_driver._get_cursor() as cursor:
            with pytest.raises(sqlite3.IntegrityError):
                cursor.execute(
                    "INSERT INTO text_question (uid, survey_uid, question) VALUES ("
                    '    "ed7b2f97-cd9d-4786-9266-a9397172397b", '
                    '    "f54e6029-a7bd-4b74-a4a4-e0bbbe1435eb", '
                    '    "WHAT AM I???"'
                    ");"
                )


class TestDriverSurveyMethods:
    def test_sqlite3_driver_can_get_list_open_surveys(self, populated_db_driver):
        surveys = populated_db_driver.get_open_surveys()

        assert len(surveys) == 2
        for survey in surveys:
            assert isinstance(survey, Survey)

    @pytest.mark.parametrize(
        "survey_uid",
        (
            UUID("00000000-9c88-4b81-9de4-bac7444fbb0a"),
            UUID("00000000-a087-4fb6-a123-24ff30263530"),
        ),
    )
    def test_driver_get_survey_returns_appropriate_survey(
        self, populated_db_driver, survey_uid
    ):
        survey = populated_db_driver.get_survey(survey_uid=survey_uid)
        assert survey is not None
        assert survey.uid == survey_uid

    @pytest.mark.parametrize(
        "survey_uid",
        (
            UUID("99999999-9c88-4b81-9de4-bac7444fbb0a"),
            UUID("99999999-a087-4fb6-a123-24ff30263530"),
        ),
    )
    def test_driver_get_survey_returns_none_when_no_survey_found(
        self, populated_db_driver, survey_uid
    ):
        survey = populated_db_driver.get_survey(survey_uid=survey_uid)
        assert survey is None

    def test_sqlite3_driver_throws_error_if_adding_a_survey_that_already_exists(
        self,
        populated_db_driver,
    ):
        surveys = populated_db_driver.get_open_surveys()
        survey = surveys[0]

        with pytest.raises(sqlite3.IntegrityError):
            populated_db_driver.insert_survey(survey)

    def test_sqlite3_driver_can_query_an_added_survey(
        self,
        empty_db_driver,
        open_survey,
    ):
        empty_db_driver.insert_survey(open_survey)

        surveys = empty_db_driver.get_open_surveys()

        assert len(surveys) == 1
        assert surveys[0] == open_survey


class TestDriverQuestionMethods:
    @pytest.mark.parametrize(
        "text_question_uid",
        (
            UUID("11111111-9c88-4b81-9de4-bac7444fbb0a"),
            UUID("11111111-a087-4fb6-a123-24ff30263530"),
            UUID("11111111-b37a-32b3-19d9-72ec921021e3"),
        ),
    )
    def test_driver_get_test_question(
        self, populated_db_driver: Sqlite3Driver, text_question_uid: UUID
    ):
        question = populated_db_driver.get_text_question(question_uid=text_question_uid)

        assert isinstance(question, TextQuestion)
        assert question.uid == text_question_uid

    def test_get_text_question_returns_none_if_no_question_with_uid_exists(
        self, populated_db_driver: Sqlite3Driver
    ):
        question = populated_db_driver.get_text_question(
            question_uid=UUID("209d67a3-d354-4cd8-afc4-7e6479582086")
        )

        assert question is None

    @pytest.mark.parametrize(
        "survey_uid, expected_tq_uids",
        (
            (
                UUID("00000000-9c88-4b81-9de4-bac7444fbb0a"),
                {UUID("11111111-9c88-4b81-9de4-bac7444fbb0a")},
            ),
            (
                UUID("00000000-a087-4fb6-a123-24ff30263530"),
                {UUID("11111111-a087-4fb6-a123-24ff30263530")},
            ),
            (
                UUID("00000000-b37a-32b3-19d9-72ec921021e3"),
                {
                    UUID("11111111-b37a-44a1-19d9-72ec921021e3"),
                    UUID("11111111-b37a-32b3-19d9-72ec921021e3"),
                },
            ),
            (
                UUID("99999999-a087-4fb6-a123-24ff30263530"),
                {},
            ),
        ),
    )
    def test_driver_can_list_questions_related_to_a_survey_uid(
        self,
        populated_db_driver: Sqlite3Driver,
        survey_uid: UUID,
        expected_tq_uids: set[UUID],
    ):
        text_questions = populated_db_driver.get_text_questions_from_survey(
            survey_uid=survey_uid
        )

        assert len(text_questions) == len(expected_tq_uids)
        for tq in text_questions:
            assert isinstance(tq, TextQuestion)
            assert tq.uid in expected_tq_uids
