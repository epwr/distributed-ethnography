import pytest
from app.server import app


def test_app_base_route_provides_an_html_page():

    client = app.test_client()
    response = client.get('/')

    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert 'text/html' in response.headers['Content-Type']

