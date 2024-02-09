import pytest
import unittest
from dataclasses import dataclass

from app.routes import app
from app.data_service.sqlite3 import Sqlite3Driver

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
    return app.test_client()

    
class TestGetHTMLEndpoints:

    """
    Test endpoints that respond to GET requests with HTML pages.
    """

    @pytest.fixture(params=(
        '/',
        '/admin',
    ))
    def endpoint(self, request):
        return request.param

    def test_get_requests_provide_an_html_page(self, app_client, endpoint):

        response = app_client.get(endpoint)

        assert response.status_code == 200
        assert 'Content-Type' in response.headers
        assert 'text/html' in response.headers['Content-Type']

        assert response.data.decode('utf-8').startswith("<!DOCTYPE html")


class TestGetHTMXEndpoints:

    """
    Test endpoints that respond to GET requests that include HTMX headers with
    HTMX responses, and to GET requests without HTMX headers with HTML responses.
    """

    @pytest.fixture(params=(
        '/surveys',
    ))
    def endpoint(self, request):
        return request.param

    def test_get_requests_return_partial_html_if_htmx_headers_are_present(
            self,
            endpoint: str,
            app_client,
            patch_db_driver
    ):

        response = app_client.get(endpoint, headers={"Hx-Request": 'true'})

        assert response.status_code == 200
        assert 'Content-Type' in response.headers
        assert 'text/html' in response.headers['Content-Type']

        assert not response.data.decode('utf-8').startswith("<!DOCTYPE html")

    def test_htmx_endpoints_returns_html_page_if_htmx_headers_are_not_present(
            self,
            endpoint: str,
            app_client, 
            patch_db_driver: Sqlite3Driver
    ):

        client = app.test_client()
        response = client.get(endpoint)

        assert response.status_code == 200
        assert 'Content-Type' in response.headers
        assert 'text/html' in response.headers['Content-Type']

        assert response.data.decode('utf-8').startswith("<!DOCTYPE html")

class TestGetStaticFileEndpoints:

    """
    Test endpoints that respond to GET requests with static files.
    """

    @pytest.fixture(params=(
        ('/static/style.css', 'text/css'),
    ))
    def test_case(self, request):
        return {
            'slug': request.param[0],
            'mime_type': request.param[1],
        }

    def test_static_files_can_be_served(self, app_client, test_case: dict[str: str]):

        client = app.test_client()
        response = client.get(test_case['slug'])

        assert response.status_code == 200
        assert 'Content-Type' in response.headers
        assert test_case['mime_type'] in response.headers['Content-Type']


class TestPostHTMXFormEndpoints:

    @pytest.fixture(params=(
        ('/surveys/new', {'name': 'endpoint test survey', 'is_open': True}),
    ))
    def test_case(self, request):
        return {
            'slug': request.param[0],
            'data': request.param[1],
        }

    
    def test_post_to_insert_survey_works(
            self,
            app_client,
            test_case: dict[str: str | dict[str, str]],
            patch_db_driver: Sqlite3Driver,
    ):

        response = app_client.post(test_case['slug'], json=test_case['data'])

        # Redirect to the new survey page
        assert response.status_code == 200

        # TODO: add that '/surveys/uid' returns same values.


