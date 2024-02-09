def assert_response_is_valid_htmx(response) -> None:
    assert response.status_code == 200
    assert "Content-Type" in response.headers
    assert "text/html" in response.headers["Content-Type"]

    assert not response.data.decode("utf-8").startswith("<!DOCTYPE html")


def assert_response_is_valid_html(response) -> None:
    assert response.status_code == 200
    assert "Content-Type" in response.headers
    assert "text/html" in response.headers["Content-Type"]

    assert response.data.decode("utf-8").startswith("<!DOCTYPE html")


def assert_response_is_valid(response, mime_type: str) -> None:
    assert response.status_code == 200
    assert "Content-Type" in response.headers
    assert mime_type in response.headers["Content-Type"]
