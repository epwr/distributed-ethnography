from functools import wraps
from typing import Callable, Dict, Any
from typing_extensions import ParamSpec

from flask import request, render_template

P = ParamSpec("P")


def htmx_endpoint(
    template: str,
) -> Callable[[Callable[..., Dict[str, Any]]], Callable[..., str]]:
    """
    Decorator that converts data to either HTMX or HTML depending on request headers.
    """

    def decorator(f: Callable[..., Dict[str, Any]]) -> Callable[..., str]:
        @wraps(f)
        def decorated_route(*args: P.args, **kwargs: P.kwargs) -> str:
            data = f(*args, **kwargs)
            request_is_htmx = all(
                (
                    "Hx-Request" in request.headers,
                    request.headers.get("Hx-Request", "").lower() == "true",
                )
            )

            if request_is_htmx:
                resp = render_template(template, **data)

            else:
                resp = render_template(
                    "_htmx_wrapper.html", partial=template, data=data
                )

            return resp

        return decorated_route

    return decorator


def validate_survey_data(data: Any) -> str | None:
    """
    Validate HTML form data submission to ensure correct request submitted.

    Returns None if data validates, else an error string.
    """

    if not isinstance(data, dict):
        return f"Survey data was passed as a {type(data)}, should be a dict."

    for key in data.keys():
        if not (
            isinstance(key, str)
            and any(
                (
                    key == "name",
                    key == "is_open",
                    key.startswith("question-"),
                )
            )
        ):
            return f"Unexpected key '{key}'."

    if not isinstance(data.get("is_open", ""), str):
        return f"'is_open' field was {type(data.get('is_open'))}, expected str or None."

    if not (data.get("is_open") is None or data.get("is_open", "").lower() == "on"):
        return f"'is_open' field was {data.get('is_open')}, expected 'on' or missing."

    if not isinstance(data.get("name"), str):
        return f"'name' field was a {type(data['name'])}, expected string."

    questions = [
        (key, value) for key, value in data.items() if key.startswith("question-")
    ]
    questions.sort(key=lambda q: q[0])

    for index, (question_key, question) in enumerate(questions):
        if int(question_key[9:]) != index:
            return "The X in 'question-X' fields should start at 0 and increment."
        if not isinstance(question, str):
            return f"Field '{question_key}' should be a string"

    return None
