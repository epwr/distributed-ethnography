import sqlite3
import pytest
from uuid import UUID

from app.models import Survey, TextQuestion, DimensionalQuestion
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

        assert len(surveys) == 4
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
        new_open_survey,
    ):
        empty_db_driver.insert_survey(new_open_survey)

        surveys = empty_db_driver.get_open_surveys()

        assert len(surveys) == 1
        assert surveys[0] == new_open_survey


class TestDriverTextQuestionMethods:
    @pytest.mark.parametrize(
        "text_question_uid",
        (
            UUID("11111111-9c88-4b81-9de4-bac7444fbb0a"),
            UUID("11111111-a087-4fb6-a123-24ff30263530"),
            UUID("11111111-b37a-32b3-19d9-72ec921021e3"),
        ),
    )
    def test_driver_get_text_question(
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
    def test_driver_can_list_text_questions_related_to_a_survey_uid(
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

    def test_insert_text_question(self, populated_db_driver: Sqlite3Driver):
        question_uid = UUID("9ab25fd1-4c26-47ec-ad67-039ada5c0c7c")
        survey_uid = UUID("00000000-9c88-4b81-9de4-bac7444fbb0a")
        question_text = "What's up?"

        text_question = TextQuestion(
            uid=question_uid, survey_uid=survey_uid, question=question_text
        )

        populated_db_driver.insert_text_question(text_question)

        returned_question = populated_db_driver.get_text_question(
            question_uid=question_uid
        )

        assert text_question == returned_question

    def test_insert_text_question_fails_do_to_survey_foreign_key(
        self, populated_db_driver: Sqlite3Driver
    ):
        question_uid = UUID("9ab25fd1-4c26-47ec-ad67-039ada5c0c7c")
        survey_uid = UUID("022a0def-4417-4d49-9bd2-418604eb9f25")
        question_text = "What's up?"

        text_question = TextQuestion(
            uid=question_uid, survey_uid=survey_uid, question=question_text
        )

        with pytest.raises(sqlite3.IntegrityError):
            populated_db_driver.insert_text_question(text_question)


class TestDriverDimensionalQuestionMethods:
    @pytest.mark.parametrize(
        "dimensional_question_uid",
        (
            UUID("11111111-3e01-4b2c-b396-1b20facf99c2"),
            UUID("11111111-2b47-4d02-8c48-0fa65f0da016"),
            UUID("11111111-041a-490d-a60c-82babc856120"),
            UUID("11111111-b36f-4e80-aba4-9707a10d6acf"),
        ),
    )
    def test_driver_get_dimensional_question(
        self, populated_db_driver: Sqlite3Driver, dimensional_question_uid: UUID
    ):
        question = populated_db_driver.get_dimensional_question(
            question_uid=dimensional_question_uid
        )

        assert isinstance(question, DimensionalQuestion)
        assert question.uid == dimensional_question_uid

    def test_get_dimensional_question_returns_none_if_no_question_with_uid_exists(
        self, populated_db_driver: Sqlite3Driver
    ):
        question = populated_db_driver.get_dimensional_question(
            question_uid=UUID("209d67a3-d354-4cd8-afc4-7e6479582086")
        )

        assert question is None

    @pytest.mark.parametrize(
        "survey_uid, expected_dq_uids",
        (
            (
                UUID("00000000-9c88-4b81-9de4-bac7444fbb0a"),
                {UUID("11111111-3e01-4b2c-b396-1b20facf99c2")},
            ),
            (
                UUID("00000000-0762-4fd1-b927-65ddb494e04f"),
                {UUID("11111111-2b47-4d02-8c48-0fa65f0da016")},
            ),
            (
                UUID("00000000-e253-4c39-b32b-eeb4f8e8711d"),
                {
                    UUID("11111111-041a-490d-a60c-82babc856120"),
                    UUID("11111111-b36f-4e80-aba4-9707a10d6acf"),
                },
            ),
            (
                UUID("99999999-a087-4fb6-a123-24ff30263530"),
                {},
            ),
        ),
    )
    def test_driver_can_list_dimensional_questions_related_to_a_survey_uid(
        self,
        populated_db_driver: Sqlite3Driver,
        survey_uid: UUID,
        expected_dq_uids: set[UUID],
    ):
        dimensional_questions = (
            populated_db_driver.get_dimensional_questions_from_survey(
                survey_uid=survey_uid
            )
        )

        assert len(dimensional_questions) == len(expected_dq_uids)
        for tq in dimensional_questions:
            assert isinstance(tq, DimensionalQuestion)
            assert tq.uid in expected_dq_uids
