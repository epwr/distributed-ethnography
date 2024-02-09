from functools import wraps

from pydantic import BaseModel
from flask import request, render_template


def htmx_endpoint(template: str) -> callable:
    """
    Return either HTMX or HTML depending on request headers.
    """

    def decorator(f):

        @wraps(f)
        def decorated_route(*args, **kwargs):

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
