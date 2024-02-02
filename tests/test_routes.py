import pytest
from app.routes import app


@pytest.mark.parametrize('endpoint', (
    '/',
))
def test_get_requests_provide_an_html_page(endpoint, patch_data_service):

    client = app.test_client()
    response = client.get(endpoint)

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert 'text/html' in response.headers['Content-Type']

    assert response.data.decode('utf-8').startswith("<!DOCTYPE html")


@pytest.mark.parametrize('endpoint', (
    '/surveys',
))
def test_get_requests_return_partial_html_if_htmx_headers_are_present(endpoint, patch_data_service):

    client = app.test_client()
    response = client.get(endpoint, headers={"Hx-Request": 'true'})

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert 'text/html' in response.headers['Content-Type']

    assert not response.data.decode('utf-8').startswith("<!DOCTYPE html")

@pytest.mark.parametrize('endpoint, expected_redirect', (
    ('/surveys', '/'),
))
def test_htmx_endpoints_redirect_user_if_htmx_headers_not_present(endpoint, expected_redirect, patch_data_service):

    client = app.test_client()
    response = client.get(endpoint)

    assert response.status_code == 302
    assert response.location == expected_redirect
