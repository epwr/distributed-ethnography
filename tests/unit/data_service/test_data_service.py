import pytest
from unittest.mock import Mock
from uuid import UUID

from app.data_service import DataService
from app.data_service.sqlite3 import Sqlite3Driver
from app.models import Survey, TextQuestion, DimensionalQuestion


@pytest.fixture
def surveys(new_open_survey) -> list[Survey]:
    return [
        new_open_survey,
    ]


@pytest.fixture
def text_questions(new_open_survey) -> list[TextQuestion]:
    return [
        TextQuestion(
            question="What's up?",
            survey_uid=new_open_survey.uid,
        )
    ]


@pytest.fixture
def dimensional_questions(new_open_survey) -> list[DimensionalQuestion]:
    return [
        DimensionalQuestion(
            question="How would you rank?",
            dimension_one="Dim 1",
            dimension_two="Dim 2",
            dimension_three="Dim 3",
            survey_uid=new_open_survey.uid,
        )
    ]


@pytest.fixture
def data_service(
    surveys: list[Survey],
    text_questions: list[TextQuestion],
    dimensional_questions: list[DimensionalQuestion],
) -> DataService:
    mock_driver = Mock(spec=Sqlite3Driver)

    mock_driver.get_open_surveys.return_value = surveys
    mock_driver.insert_survey.return_value = None

    mock_driver.get_text_questions_from_survey.return_value = text_questions
    mock_driver.get_text_question.return_value = text_questions[0]
    mock_driver.insert_text_question.return_value = None

    mock_driver.get_dimensional_questions_from_survey.return_value = (
        dimensional_questions
    )
    mock_driver.get_dimensional_question.return_value = dimensional_questions[0]
    # mock_driver.insert_dimensional_question.return_value = None

    return DataService(driver=mock_driver)


class TestDataServiceSurveyMethods:
    def test_get_open_surveys_returns_all_open_surveys(
        self, data_service: DataService, surveys: list[Survey]
    ):
        returned_surveys = data_service.get_open_surveys()

        assert len(surveys) == len(returned_surveys)

        for survey in returned_surveys:
            assert survey in surveys

    def test_get_survey_returns_one_survey_if_exists(
        self,
        data_service: DataService,
    ):
        survey = Survey(name="test", is_open=True)
        data_service._driver.get_survey.return_value = survey

        returned_survey = data_service.get_survey(survey.uid)
        assert returned_survey == survey

    def test_get_survey_returns_none_if_no_survey(
        self,
        data_service: DataService,
    ):
        data_service._driver.get_survey.return_value = None
        survey = data_service.get_survey(UUID("99999999-9c88-4b81-9de4-bac7444fbb0a"))
        assert survey is None

    def test_get_survey_if_open_returns_one_survey_if_open(
        self,
        data_service: DataService,
    ):
        survey = Survey(name="test", is_open=True)
        data_service._driver.get_survey.return_value = survey

        returned_survey = data_service.get_survey_if_open(survey.uid)
        assert returned_survey == survey

    def test_get_survey_if_open_returns_none_if_survey_closed(
        self,
        data_service: DataService,
    ):
        survey = Survey(name="test", is_open=False)
        data_service._driver.get_survey.return_value = survey

        returned_survey = data_service.get_survey_if_open(survey_uid=survey.uid)
        assert returned_survey is None

    def test_can_insert_a_survey(
        self, data_service: DataService, new_open_survey: Survey
    ):
        data_service.insert_survey(new_open_survey)
        data_service._driver.insert_survey.assert_called_once_with(
            survey=new_open_survey
        )


class TestDataServiceTextQuestionMethods:
    def test_get_questions_from_survey(
        self,
        data_service: DataService,
    ):
        survey_uid = UUID("ee50dd84-86a0-4a9d-a632-ec6670e2cd89")
        questions = data_service.get_text_questions_from_survey(survey_uid=survey_uid)

        assert len(questions) == 1
        assert isinstance(questions[0], TextQuestion)
        data_service._driver.get_text_questions_from_survey.assert_called_once_with(
            survey_uid=survey_uid
        )

    def test_get_question(
        self,
        data_service: DataService,
    ):
        question_uid = UUID("ee50dd84-86a0-4a9d-a632-ec6670e2cd89")
        question = data_service.get_text_question(question_uid=question_uid)

        assert isinstance(question, TextQuestion)
        assert question == data_service._driver.get_text_question.return_value

    def test_insert_text_question(
        self,
        data_service: DataService,
        existing_open_survey: Survey,
        new_text_question: TextQuestion,
    ):
        new_text_question.survey_uid = existing_open_survey.uid

        data_service.insert_text_question(new_text_question)
        data_service._driver.insert_text_question.assert_called_once_with(
            text_question=new_text_question
        )


class TestDataServiceDimensionalQuestionMethods:
    def test_get_questions_from_survey(
        self,
        data_service: DataService,
    ):
        survey_uid = UUID("ee50dd84-86a0-4a9d-a632-ec6670e2cd89")
        questions = data_service.get_dimensional_questions_from_survey(
            survey_uid=survey_uid
        )

        assert len(questions) == 1
        assert isinstance(questions[0], DimensionalQuestion)
        method = data_service._driver.get_dimensional_questions_from_survey
        method.assert_called_once_with(survey_uid=survey_uid)

    def test_get_question(
        self,
        data_service: DataService,
    ):
        question_uid = UUID("ee50dd84-86a0-4a9d-a632-ec6670e2cd89")
        question = data_service.get_dimensional_question(question_uid=question_uid)

        assert isinstance(question, DimensionalQuestion)
        assert question == data_service._driver.get_dimensional_question.return_value


#    def test_insert_dimensional_question(
#        self,
#        data_service: DataService,
#        existing_open_survey: Survey,
#        new_dimensional_question: DimensionalQuestion,
#    ):
#        new_dimensional_question.survey_uid = existing_open_survey.uid
#
#        data_service.insert_dimensional_question(new_dimensional_question)
#        data_service._driver.insert_dimensional_question.assert_called_once_with(
#            dimensional_question=new_dimensional_question
#        )
