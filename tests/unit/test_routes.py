import pytest
from unittest.mock import MagicMock

from app.data_service import DataService
from app.models import Survey

from tests.unit.test_routes_utils import (
    assert_response_is_valid_htmx,
    assert_response_is_valid_html,
    assert_response_is_valid,
    assert_mocked_class_has_method_call_on_object,
)


@pytest.fixture
def mock_data_service_class(monkeypatch):
    data_service = MagicMock()
    monkeypatch.setattr("app.routes.DataService", data_service)

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
        mock_data_service_class,
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
        mock_data_service_class,
        endpoint: str,
    ):
        response = app_client.get(endpoint)
        assert response.status_code == 404


class TestGetHTMXEndpoints:

    """
    Test endpoints that respond to GET requests that include HTMX headers with
    HTMX responses, and to GET requests without HTMX headers with HTML responses.
    """

    test_cases = (
        (
            "/surveys",
            "get_open_surveys",
        ),
    )

    @pytest.mark.parametrize(
        "slug, expected_data_service_call",
        test_cases,
    )
    def test_get_requests_return_partial_html_if_htmx_headers_are_present(
        self,
        app_client,
        mock_data_service_class,
        slug: str,
        expected_data_service_call: str,
    ):
        response = app_client.get(slug, headers={"Hx-Request": "true"})
        assert_mocked_class_has_method_call_on_object(
            mock_class=mock_data_service_class,
            method_call=expected_data_service_call,
        )
        assert_response_is_valid_htmx(response)

    @pytest.mark.parametrize(
        "slug, expected_data_service_call",
        test_cases,
    )
    def test_htmx_endpoints_returns_html_page_if_htmx_headers_are_not_present(
        self,
        app_client,
        mock_data_service_class,
        slug: str,
        expected_data_service_call: str,
    ):
        response = app_client.get(slug)
        assert_mocked_class_has_method_call_on_object(
            mock_class=mock_data_service_class,
            method_call=expected_data_service_call,
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


class TestPostHTMXFormEndpoints:
    test_cases = (
        (
            "/surveys/new",
            {"name": "test survey - open", "is_open": True},
            "insert_survey",
            Survey,
        ),
        (
            "/surveys/new",
            {
                "name": "test survey - closed"
            },  # unchecked checkboxes are represented as missing.
            "insert_survey",
            Survey,
        ),
    )

    @pytest.mark.parametrize(
        "slug, data, expected_data_service_call, argument_class",
        test_cases,
    )
    def test_post_requests_can_return_htmx(
        self,
        app_client,
        slug: str,
        data: dict[str, str],
        expected_data_service_call: str,
        argument_class: str,
        mock_data_service_class: DataService,
    ):
        response = app_client.post(slug, data=data, headers={"Hx-Request": "true"})

        assert_mocked_class_has_method_call_on_object(
            mock_class=mock_data_service_class,
            method_call=expected_data_service_call,
            argument_types=[argument_class],
        )
        assert_response_is_valid_htmx(response)

    @pytest.mark.parametrize(
        "slug, data, expected_data_service_call, argument_class",
        test_cases,
    )
    def test_post_requests_can_return_html(
        self,
        app_client,
        slug: str,
        data: dict[str, str],
        expected_data_service_call: str,
        argument_class: str,
        mock_data_service_class: DataService,
    ):
        response = app_client.post(slug, data=data)

        assert_mocked_class_has_method_call_on_object(
            mock_class=mock_data_service_class,
            method_call=expected_data_service_call,
            argument_types=[argument_class],
        )
        assert_response_is_valid_html(response)

    @pytest.mark.parametrize(
        "slug, data",
        (
            ("/surveys/new", {}),
            (
                "/surveys/new",
                {"name": "Testing", "uid": "bb92a5f5-7d62-4e77-9cbb-c8c903c4e65f"},
            ),
        ),
    )
    def test_malformed_requests_return_400_code(self, app_client, slug, data) -> None:
        response = app_client.post(slug, data=data)
        assert response.status_code == 400
