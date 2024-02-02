from functools import wraps
from flask import render_template, redirect, request

def htmx_partial(template: str, redirection: str) -> callable:

    """
    Return partial HTML if the endpoint is called with HTMX headers, else
    return a 302 redirect to the provided endpoint.
    """

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):

            request_is_htmx = all((
                'Hx-Request' in request.headers,
                request.headers.get('Hx-Request', '').lower() == 'true',
            ))

            if request_is_htmx:
                data = f(*args, **kwargs)
                return render_template(template, **data)

            return redirect(redirection)

        return decorated_function

    return decorator
