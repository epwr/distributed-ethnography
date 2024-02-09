import pytest

from app.routes import app
from app.data_service.sqlite3 import Sqlite3Driver

from tests.test_routes_utils import (
    assert_response_is_valid_htmx,
    assert_response_is_valid_html,
    assert_response_is_valid,
)


@pytest.fixture
def patch_db_driver(populated_db_driver, monkeypatch):
    """
    Ensure every test uses the populated test database.
    """

    def patched_init(self, driver):
        self._driver = populated_db_driver

    monkeypatch.setattr("app.routes.DataService.__init__", patched_init)

    yield

    monkeypatch.undo()


@pytest.fixture
def app_client():
    with app.test_client() as client:
        yield client


class TestGetHTMLEndpoints:

    """
    Test endpoints that respond to GET requests with HTML pages.
    """

    @pytest.fixture(
        params=(
            "/",
            "/admin",
        )
    )
    def endpoint(self, request):
        return request.param

    def test_get_requests_provide_an_html_page(self, app_client, endpoint):
        response = app_client.get(endpoint)
        assert_response_is_valid_html(response)


class TestGetHTMXEndpoints:

    """
    Test endpoints that respond to GET requests that include HTMX headers with
    HTMX responses, and to GET requests without HTMX headers with HTML responses.
    """

    @pytest.fixture(params=("/surveys",))
    def endpoint(self, request):
        return request.param

    def test_get_requests_return_partial_html_if_htmx_headers_are_present(
        self, endpoint: str, app_client, patch_db_driver
    ):
        response = app_client.get(endpoint, headers={"Hx-Request": "true"})
        assert_response_is_valid_htmx(response)

    def test_htmx_endpoints_returns_html_page_if_htmx_headers_are_not_present(
        self, endpoint: str, app_client, patch_db_driver: Sqlite3Driver
    ):
        response = app_client.get(endpoint)
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
    @pytest.mark.parametrize(
        "slug, data",
        (
            ("/surveys/new", {"name": "test survey - open", "is_open": True}),
            ("/surveys/new", {"name": "test survey - closed", "is_open": False}),
        ),
    )
    def test_post_to_insert_survey_works(
        self,
        app_client,
        slug: str,
        data: dict[str, str],
        patch_db_driver: Sqlite3Driver,
    ):
        response = app_client.post(slug, data=data)
        assert_response_is_valid_htmx(response)
