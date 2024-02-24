import pytest
from unittest.mock import MagicMock

from app.data_service import DataService
from app.models import Survey, TextQuestion

from tests.unit.test_routes_helpers import (
    assert_response_is_valid_htmx,
    assert_response_is_valid_html,
    assert_response_is_valid,
    assert_mocked_class_has_method_call_on_object,
)


@pytest.fixture
def mock_data_service(
    monkeypatch, new_open_survey: Survey, new_text_question: TextQuestion
):
    data_service = MagicMock()
    monkeypatch.setattr("app.routes.DataService", data_service)

    data_service.return_value.get_survey_if_open.return_value = new_open_survey
    data_service.return_value.get_text_questions_from_survey.return_value = (
        new_text_question
    )

    yield data_service

    monkeypatch.undo()


class TestGetHTMLEndpoints:

    """
    Test basic GET endpoints.
    """

    @pytest.mark.parametrize(
        "endpoint",
        (
            "/",
            "/admin",
            "/surveys/new",
            "/surveys/00000000-a087-4fb6-a123-24ff30263530",  # Open Test Survey
        ),
    )
    def test_get_requests_provide_an_html_page(
        self,
        app_client,
        mock_data_service,
        endpoint: str,
    ):
        response = app_client.get(endpoint)
        assert_response_is_valid_html(response)

    @pytest.mark.parametrize(
        "endpoint",
        ("/surveys/00000000-9c88-4b81-9de4-bac7444fbb0a",),  # Closed Test Survey
    )
    def test_get_request_returns_404(
        self,
        app_client,
        mock_data_service,
        endpoint: str,
    ):
        mock_data_service.return_value.get_survey_if_open.return_value = None
        response = app_client.get(endpoint)
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "slug, expected_data_service_calls",
        (
            (
                "/surveys/00000000-a087-4fb6-a123-24ff30263530",
                ("get_survey_if_open", "get_text_questions_from_survey"),
            ),
        ),
    )
    def test_get_requests_make_expected_data_service_calls(
        self,
        app_client,
        mock_data_service,
        slug: str,
        expected_data_service_calls: str,
    ):
        response = app_client.get(slug)

        for method in expected_data_service_calls:
            assert_mocked_class_has_method_call_on_object(
                mock_class=mock_data_service,
                method_call=method,
            )
        assert_response_is_valid_html(response)


class TestGetHTMXEndpoints:

    """
    Test endpoints that respond to GET requests that include HTMX headers with
    HTMX responses, and to GET requests without HTMX headers with HTML responses.
    """

    test_cases = (
        (
            "/surveys",
            ("get_open_surveys",),
        ),
    )

    @pytest.mark.parametrize(
        "slug, expected_data_service_calls",
        test_cases,
    )
    def test_get_requests_return_partial_html_if_htmx_headers_are_present(
        self,
        app_client,
        mock_data_service,
        slug: str,
        expected_data_service_calls: str,
    ):
        response = app_client.get(slug, headers={"Hx-Request": "true"})

        for method in expected_data_service_calls:
            assert_mocked_class_has_method_call_on_object(
                mock_class=mock_data_service,
                method_call=method,
            )
        assert_response_is_valid_htmx(response)

    @pytest.mark.parametrize(
        "slug, expected_data_service_calls",
        test_cases,
    )
    def test_htmx_endpoints_returns_html_page_if_htmx_headers_are_not_present(
        self,
        app_client,
        mock_data_service,
        slug: str,
        expected_data_service_calls: str,
    ):
        response = app_client.get(slug)

        for method in expected_data_service_calls:
            assert_mocked_class_has_method_call_on_object(
                mock_class=mock_data_service,
                method_call=method,
            )
        assert_response_is_valid_html(response)


class TestGetStaticFileEndpoints:

    """
    Test endpoints that respond to GET requests with static files.
    """

    @pytest.mark.parametrize("slug, mime_type", (("/static/style.css", "text/css"),))
    def test_static_files_can_be_served(self, app_client, slug, mime_type):
        response = app_client.get(slug)
        assert_response_is_valid(response, mime_type=mime_type)


class TestCreateSurveyEndpoint:
    test_cases = (
        (
            {
                "name": "test survey - open",
                "is_open": "on",
                "question-0": "What's my name again?",
                "question-1": "What's your name again?",
            },
            {
                "insert_survey": {"survey": Survey},
                "insert_text_question": {"text_question": TextQuestion},
            },
        ),
        (
            {
                "name": "test survey - closed",
                "question-0": "What's my name again?",
                "question-1": "What's your name again?",
            },  # unchecked checkboxes are represented as missing.
            {
                "insert_survey": {"survey": Survey},
                "insert_text_question": {"text_question": TextQuestion},
            },
        ),
        (
            {
                "name": "test survey - closed w/ no questions",
            },  # unchecked checkboxes are represented as missing.
            {
                "insert_survey": {"survey": Survey},
            },
        ),
        (
            {
                "name": "test survey - with questions",
                "is_open": "on",
                "question-0": "How are you today?",
                "question-1": "What day is it?",
            },
            {
                "insert_survey": {"survey": Survey},
                "insert_text_question": {"text_question": TextQuestion},
            },
        ),
    )

    @pytest.mark.parametrize(
        "data, expected_data_service_calls",
        test_cases,
    )
    def test_post_requests_can_return_htmx(
        self,
        app_client,
        mock_data_service: DataService,
        data: dict[str, str],
        expected_data_service_calls: dict[str, list[Survey | TextQuestion]],
    ):
        response = app_client.post(
            "/surveys/new", data=data, headers={"Hx-Request": "true"}
        )

        assert_response_is_valid_htmx(response)
        for method_call, argument_types in expected_data_service_calls.items():
            assert_mocked_class_has_method_call_on_object(
                mock_class=mock_data_service,
                method_call=method_call,
                arguments_of_types=argument_types,
            )

    @pytest.mark.parametrize(
        "data, expected_data_service_calls",
        test_cases,
    )
    def test_post_requests_can_return_html(
        self,
        app_client,
        mock_data_service: DataService,
        data: dict[str, str],
        expected_data_service_calls: str,
    ):
        response = app_client.post("/surveys/new", data=data)

        assert_response_is_valid_html(response)
        for method_call, argument_types in expected_data_service_calls.items():
            assert_mocked_class_has_method_call_on_object(
                mock_class=mock_data_service,
                method_call=method_call,
                arguments_of_types=argument_types,
            )

    @pytest.mark.parametrize(
        "slug, data",
        (
            ("/surveys/new", {}),
            (
                "/surveys/new",
                {
                    "name": "Do not pass uid field in via api.",
                    "uid": "bb92a5f5-7d62-4e77-9cbb-c8c903c4e65f",
                },
            ),
            (
                "/surveys/new",
                {
                    "name": "Malformed questions.",
                    "is_open": "on",
                    "questions": "questions should have a name of question-X",
                },
            ),
            (
                "/surveys/new",
                {
                    "name": "Malformed questions.",
                    "is_open": "on",
                    "question-1": "key should be question-X, starting at x=0",
                },
            ),
            (
                "/surveys/new",
                {
                    "name": "Malformed questions.",
                    "is_open": "on",
                    "question-0": "key should be question-X, starting at x=0",
                    "question-2": "questions should have an incrementing index.",
                },
            ),
            (
                "/surveys/new",
                {},
            ),
            (
                "/surveys/new",
                [],
            ),
        ),
    )
    def test_malformed_requests_return_400_code(
        self, app_client, mock_data_service: DataService, slug: str, data: dict
    ) -> None:
        response = app_client.post(slug, data=data)
        assert response.status_code == 400
