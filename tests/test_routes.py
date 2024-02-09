import pytest
from app.routes import app

from app.data_service.sqlite3 import Sqlite3Driver

@pytest.fixture
def patch_db_driver(populated_db_driver, monkeypatch):

    def patched_init(self, driver):
        self._driver = populated_db_driver

    monkeypatch.setattr("app.routes.DataService.__init__", patched_init)

    yield

    monkeypatch.undo()


@pytest.mark.parametrize('endpoint', (
    '/',
    '/admin',
))
def test_get_requests_provide_an_html_page(endpoint):

    client = app.test_client()
    response = client.get(endpoint)

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert 'text/html' in response.headers['Content-Type']

    assert response.data.decode('utf-8').startswith("<!DOCTYPE html")


@pytest.mark.parametrize('endpoint', (
    '/surveys',
))
def test_get_requests_return_partial_html_if_htmx_headers_are_present(endpoint: str, patch_db_driver):

    client = app.test_client()
    response = client.get(endpoint, headers={"Hx-Request": 'true'})

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert 'text/html' in response.headers['Content-Type']

    assert not response.data.decode('utf-8').startswith("<!DOCTYPE html")

@pytest.mark.parametrize('endpoint', (
    '/surveys',
))
def test_htmx_endpoints_returns_full_html_page_if_htmx_headers_are_not_present(
        endpoint: str,
        patch_db_driver: Sqlite3Driver
):

    client = app.test_client()
    response = client.get(endpoint)

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert 'text/html' in response.headers['Content-Type']

    assert response.data.decode('utf-8').startswith("<!DOCTYPE html")

@pytest.mark.parametrize('endpoint, filetype', (
    ('/style.css', 'text/css'),
))
def test_static_files_can_be_served(endpoint: str, filetype: str):

    client = app.test_client()
    response = client.get('/static' + endpoint)

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert filetype in response.headers['Content-Type']


@pytest.mark.parametrize('survey', (
    {'name': 'endpoint test survey', 'is_open': True},
))
def test_post_to_insert_survey_works(
        survey: dict[str:str],
        patch_db_driver: Sqlite3Driver,
):

    client = app.test_client()
    response = client.post('/surveys/new', json=survey)

    # Redirect to the new survey page
    assert response.status_code == 200

    # TODO: add that '/surveys/uid' returns same values.


