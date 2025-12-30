from functools import wraps
from fastapi import Request
from fastapi.responses import RedirectResponse

def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")

        # Fallback: find Request in args (FastAPI flexibility)
        if not request:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

        if not request or "user" not in request.session:
            return RedirectResponse("/login", status_code=303)

        return await func(*args, **kwargs)

    return wrapper
