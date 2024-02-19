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


def assert_mocked_class_has_method_call_on_object(
    mock_class: type,
    method_call: str,
    arguments: dict | None = None,
    argument_types: list[type] | None = None,
) -> None:
    """
    Assert that a mocked class was instantiated and then a method was called on
    the object.

    If arguments is passed, then assert that the method was called once with the
    provided arguments.

    Else-if argument_types is passed, assert that the method was called with a set
    of arguments where each argument has the appropriate types.

    Otherwise, assert that the method was called once.
    """

    method = mock_class.return_value.__getattr__(method_call)

    if arguments is not None:
        method.assert_called_once_with(**arguments)
    elif argument_types is not None:
        assert len(method.call_args.args) == len(argument_types)
        for arg, of_type in zip(method.call_args.args, argument_types):
            assert isinstance(arg, of_type)
    else:
        method.assert_called_once()
