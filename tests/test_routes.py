import pytest
from app.routes import app

@pytest.fixture
def patch_db_driver(populated_db_driver, monkeypatch):

    def patched_init(self, driver):
        self._driver = populated_db_driver

    monkeypatch.setattr("app.routes.DataService.__init__", patched_init)

    yield

    monkeypatch.undo()


@pytest.mark.parametrize('endpoint', (
    '/',
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
def test_get_requests_return_partial_html_if_htmx_headers_are_present(endpoint, patch_db_driver):

    client = app.test_client()
    response = client.get(endpoint, headers={"Hx-Request": 'true'})

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert 'text/html' in response.headers['Content-Type']

    assert not response.data.decode('utf-8').startswith("<!DOCTYPE html")

@pytest.mark.parametrize('endpoint, expected_redirect', (
    ('/surveys', '/'),
))
def test_htmx_endpoints_redirect_user_if_htmx_headers_not_present(endpoint, expected_redirect):

    client = app.test_client()
    response = client.get(endpoint)

    assert response.status_code == 302
    assert response.location == expected_redirect

@pytest.mark.parametrize('endpoint, filetype', (
    ('/style.css', 'text/css'),
))
def test_static_files_can_be_served(endpoint, filetype):

    client = app.test_client()
    response = client.get('/static' + endpoint)

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert filetype in response.headers['Content-Type']
