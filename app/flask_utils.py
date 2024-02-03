from functools import wraps

from pydantic import BaseModel
from flask import render_template, redirect, request

def htmx_or_json(template: str) -> callable:

    """
    Return partial HTML if the endpoint is called with HTMX headers, else
    return JSON
    """

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):

            data = f(*args, **kwargs)
            request_is_htmx = all((
                'Hx-Request' in request.headers,
                request.headers.get('Hx-Request', '').lower() == 'true',
            ))

            if request_is_htmx:
                return render_template(template, **data)

            # Return as python primitives & collections to be parsed into JSON.
            def recursive_parser(obj):
                if isinstance(obj, BaseModel):
                    return obj.model_dump()
                if isinstance(obj, dict):
                    return {
                        recursive_parser(key): recursive_parser(value)
                        for key, value in obj.items()
                    }
                if isinstance(obj, list):
                    return [recursive_parser(item) for item in obj]
                return obj

            return recursive_parser(data)

        return decorated_function

    return decorator
