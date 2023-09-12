"""
A **lightweight** Flask wrapper built specifically for writing an API that interacts with a SQL database using pydantic model validation.
"""
from functools import wraps
import logging
import sqlite3
from typing import (
    Any,
    Callable,
    Literal,
    LiteralString,
    ParamSpec,
    Type,
    TypeVar,
    Unpack,
    overload,
)
from flask import has_request_context, request
import pydantic

DB = "app.db"


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


UnsafeStr = str
O = TypeVar("O", bound=BaseModel)


@overload
def model_cast(
    keys: tuple[LiteralString], values: tuple[str], obj: Callable[..., O]
) -> O:
    ...


@overload
def model_cast(keys: tuple[LiteralString], values: tuple[str], obj=tuple) -> tuple[str]:
    ...


def model_cast(
    keys: tuple[LiteralString],
    values: tuple[str],
    obj: Callable[..., O] | Type[tuple] = tuple,
):
    """Creates a model from the "Any" type returned from the database.

    Args:
        keys (tuple[LiteralString]): _description_
        values (tuple[str]): _description_
        obj (Callable[..., O] | Type[tuple], optional): _description_. Defaults to tuple.

    Returns:
        _type_: _description_
    """
    if obj == tuple:
        return values
    return obj(**{k: v for k, v in zip(keys, values)})


@overload
def get_from_db(
    select: tuple[LiteralString],
    where: dict[LiteralString, UnsafeStr],
    table: str,
    fetch: Literal["one"] = "one",
    DB_PATH: str = DB,
) -> Any:
    ...


@overload
def get_from_db(
    select: tuple[LiteralString],
    where: dict[LiteralString, UnsafeStr],
    table: str,
    fetch: Literal["all"],
    DB_PATH: str = DB,
) -> list[Any]:
    ...


@overload
def get_from_db(
    select: tuple[LiteralString],
    where: dict[LiteralString, UnsafeStr],
    table: str,
    fetch: int,
    DB_PATH: str = DB,
) -> list[Any]:
    ...


def get_from_db(
    select: tuple[LiteralString],
    where: dict[LiteralString, UnsafeStr],
    table: str,
    fetch: Literal["one", "all"] | int = "one",
    DB_PATH: str = DB,
) -> O | list[O]:
    """Gets an object from the database.

    Args:
        select (tuple[LiteralString]):column ids e.g. ('name','num')
        where (dict[LiteralString, UnsafeStr]): e.g. {'id':input()}
        table (str): table name
        fetch (Literal[&quot;one&quot;, &quot;all&quot;] | int, optional): Whether to use algorithm for fetching one, many, or all. Defaults to "one".
        DB_PATH (str, optional): Path. Defaults to DB.

    Raises:
        Exception: _description_

    Returns:
        O | list[O]: _description_
    """
    conn = sqlite3.connect(DB_PATH)
    # guarantee pair order
    where_keys: list[LiteralString] = []
    where_values: list[UnsafeStr] = []
    for k, v in where.items():
        where_keys.append(k)
        where_values.append(v)

    def get_helper():
        logging.debug(f"Fetching {select=} {table=} {where_keys=} {where_values=}")
        cur = conn.execute(
            f"""
                SELECT {', '.join(select)} FROM {table} 
                WHERE {" AND ".join([f'{k}=?' for k in where_keys])};
            """,
            where_values,
        )
        if isinstance(fetch, str):
            if fetch == "one":
                return cur.fetchone()
            if fetch == "all":
                return cur.fetchall()
        else:
            return cur.fetchmany(fetch)

    r = get_helper()

    if not r:
        command = f"""
            INSERT INTO {table} ({', '.join(where_keys)}) VALUES({', '.join([f"'{i}'" for i in where_values])});
        """.strip()
        logging.debug(f"Inserting using {command=}")
        conn.execute(command)
        conn.commit()
        r = get_helper()
        if not r:
            raise Exception(f"Unsuccessful select after insertion: got {r}")

    return r
