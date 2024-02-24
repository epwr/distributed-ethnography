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
    arguments_of_types: dict[str, type] | None = None,
) -> None:
    """
    Assert that a mocked class was instantiated and then a method was called on
    the object.

    If arguments is passed, then assert that the method was called once with the
    provided arguments.

    Else-if argument_of_types is passed, assert that the method was called with a set
    of arguments where each argument has the appropriate type.

    Otherwise, assert that the method was called once.
    """

    method = mock_class.return_value.__getattr__(method_call)
    assert method.called
    assert len(method.call_args.args) == 0  # Use kwargs

    if arguments is not None:
        method.assert_called_once_with(**arguments)
    elif arguments_of_types is not None:
        assert len(method.call_args.kwargs) == len(arguments_of_types)
        for argument, arg_type in arguments_of_types.items():
            value = method.call_args.kwargs[argument]
            assert isinstance(value, arg_type)
