"""
A **lightweight** Flask wrapper built specifically for writing an API that interacts with a SQL database using pydantic model validation.
"""
from functools import wraps
import logging
from typing import Callable, TypeVar
from flask import has_request_context, request
import pydantic


class NewBaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")


BaseModel = NewBaseModel


T = TypeVar("T")


def do_logging(req: bool = True, res: bool = True):
    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def wrapper() -> T:
            if has_request_context() and req:
                if request.method.lower() == "post":
                    logging.info(f"Got POST: {request.form=}")
                else:
                    logging.info(f"Got {request.method}: {request.form=}")
            else:
                logging.warning(
                    f"Unexpected call to do_logging outside of request context from {fn}"
                )
            if res:
                response = fn()
                logging.info(f"Sending {response=}")
                return response
            return fn()

        return wrapper

    return decorator
