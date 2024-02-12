import pytest


@pytest.fixture
def setup_data_service(monkeypatch, populated_db_driver):
    def patched_init(self, driver):
        self._driver = populated_db_driver

    monkeypatch.setattr("app.routes.DataService.__init__", patched_init)

    yield

    monkeypatch.undo()


class TestMutationEndpoints:
    test_cases = [
        ("post", "/surveys/new", {"name": "test", "is_open": True}, "/surveys"),
    ]

    @pytest.mark.parametrize("http_method, slug, data, read_endpoint", test_cases)
    def test_endpoint_changes_response_of_other_endpoint(
        self,
        app_client,
        setup_data_service,
        http_method: str,
        slug: str,
        data: dict[str, str],
        read_endpoint: str,
    ):
        initial_response = app_client.get(read_endpoint)
        mutation_response = app_client.__getattribute__(http_method)(slug, data=data)
        updated_response = app_client.get(read_endpoint)

        assert initial_response.status_code == 200
        assert mutation_response.status_code == 200
        assert updated_response.status_code == 200

        assert initial_response.data != updated_response.data
