from functools import wraps
from typing import Callable, Dict, Any
from typing_extensions import ParamSpec

from flask import request, render_template

P = ParamSpec('P')

def htmx_endpoint(template: str) -> Callable[
        [Callable[..., Dict[str, Any]]], Callable[..., str]
]:
    """
    Return either HTMX or HTML depending on request headers.
    """

    def decorator(f: Callable[..., Dict[str, Any]]) -> Callable[..., str]:

        @wraps(f)
        def decorated_route(*args: P.args, **kwargs: P.kwargs) -> str:

            data = f(*args, **kwargs)
            request_is_htmx = all((
                'Hx-Request' in request.headers,
                request.headers.get('Hx-Request', '').lower() == 'true',
            ))

            if request_is_htmx:
                resp = render_template(template, **data)

            else:
                resp = render_template(
                    "_htmx_wrapper.html",
                    partial=template,
                    data=data
                )

            return resp

        return decorated_route

    return decorator
