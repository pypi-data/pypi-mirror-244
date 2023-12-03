from __future__ import annotations

from collections.abc import Iterable, Sequence
from functools import reduce
from itertools import chain

from polars import DataFrame, Expr, PolarsDataType
from polars.exceptions import OutOfBoundsError
from polars.testing import assert_frame_equal
from polars.type_aliases import IntoExpr, JoinStrategy, JoinValidation, SchemaDict

from utilities.errors import redirect_error
from utilities.math import is_equal_or_approx
from utilities.types import SequenceStrs


def check_polars_dataframe(
    df: DataFrame,
    /,
    *,
    columns: SequenceStrs | None = None,
    dtypes: list[PolarsDataType] | None = None,
    height: int | tuple[int, float] | None = None,
    min_height: int | None = None,
    max_height: int | None = None,
    schema: SchemaDict | None = None,
    shape: tuple[int, int] | None = None,
    sorted: IntoExpr | Iterable[IntoExpr] | None = None,  # noqa: A002
    unique: IntoExpr | Iterable[IntoExpr] | None = None,
    width: int | None = None,
) -> None:
    """Check the properties of a DataFrame."""
    if (columns is not None) and (df.columns != list(columns)):
        msg = f"{df=}, {columns=}"
        raise CheckPolarsDataFrameError(msg)
    if (dtypes is not None) and (df.dtypes != dtypes):
        msg = f"{df=}, {dtypes=}"
        raise CheckPolarsDataFrameError(msg)
    if (height is not None) and not is_equal_or_approx(df.height, height):
        msg = f"{df=}, {height=}"
        raise CheckPolarsDataFrameError(msg)
    if (min_height is not None) and (len(df) < min_height):
        msg = f"{df=}, {min_height=}"
        raise CheckPolarsDataFrameError(msg)
    if (max_height is not None) and (len(df) > max_height):
        msg = f"{df=}, {max_height=}"
        raise CheckPolarsDataFrameError(msg)
    if (schema is not None) and (df.schema != schema):
        set_act, set_exp = map(set, [df.schema, schema])
        extra = set_act - set_exp
        missing = set_exp - set_act
        differ = {
            col: (left, right)
            for col in set_act & set_exp
            if (left := df.schema[col]) != (right := schema[col])
        }
        msg = f"{df=}, {extra=}, {missing=}, {differ=}"
        raise CheckPolarsDataFrameError(msg)
    if (shape is not None) and (df.shape != shape):
        msg = f"{df=}"
        raise CheckPolarsDataFrameError(msg)
    if sorted is not None:
        df_sorted = df.sort(sorted)
        with redirect_error(AssertionError, CheckPolarsDataFrameError(f"{df=}")):
            assert_frame_equal(df, df_sorted)
    if (unique is not None) and df.select(unique).is_duplicated().any():
        msg = f"{df=}, {unique=}"
        raise CheckPolarsDataFrameError(msg)
    if (width is not None) and (df.width != width):
        msg = f"{df=}"
        raise CheckPolarsDataFrameError(msg)


class CheckPolarsDataFrameError(Exception):
    ...


def join(
    df: DataFrame,
    *dfs: DataFrame,
    on: str | Expr | Sequence[str | Expr],
    how: JoinStrategy = "inner",
    validate: JoinValidation = "m:m",
) -> DataFrame:
    def inner(left: DataFrame, right: DataFrame, /) -> DataFrame:
        return left.join(right, on=on, how=how, validate=validate)

    return reduce(inner, chain([df], dfs))


def set_first_row_as_columns(df: DataFrame, /) -> DataFrame:
    """Set the first row of a DataFrame as its columns."""

    with redirect_error(OutOfBoundsError, SetFirstRowAsColumnsError(f"{df=}")):
        row = df.row(0)
    mapping = dict(zip(df.columns, row, strict=True))
    return df[1:].rename(mapping)


class SetFirstRowAsColumnsError(Exception):
    ...


__all__ = [
    "CheckPolarsDataFrameError",
    "SetFirstRowAsColumnsError",
    "check_polars_dataframe",
    "join",
    "set_first_row_as_columns",
]


try:
    from utilities._polars.bs4 import (
        TableTagToDataFrameError,
        table_tag_to_dataframe,
        yield_tables,
    )
except ModuleNotFoundError:  # pragma: no cover
    pass
else:
    __all__ += ["TableTagToDataFrameError", "table_tag_to_dataframe", "yield_tables"]
