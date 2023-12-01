from __future__ import annotations

from polars import DataFrame, Float64, Int64, Utf8
from polars.testing import assert_frame_equal
from pytest import mark, param, raises

from utilities.polars import (
    CheckPolarsDataFrameError,
    CheckPolarsDataFrameHeightError,
    SetFirstRowAsColumnsError,
    check_polars_dataframe,
    check_polars_dataframe_height,
    join,
    set_first_row_as_columns,
)


class TestCheckPolarsDataFrame:
    def test_main(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df)

    def test_columns_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, columns=[])

    def test_columns_error(self) -> None:
        df = DataFrame()
        with raises(CheckPolarsDataFrameError):
            check_polars_dataframe(df, columns=["value"])

    def test_dtypes_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, dtypes=[])

    def test_dtypes_error(self) -> None:
        df = DataFrame()
        with raises(CheckPolarsDataFrameError):
            check_polars_dataframe(df, dtypes=[Float64])

    def test_height(self) -> None:
        df = DataFrame({"value": [0.0]})
        check_polars_dataframe(df, height=1)

    def test_min_height_pass(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        check_polars_dataframe(df, min_height=1)

    def test_min_height_error(self) -> None:
        df = DataFrame()
        with raises(CheckPolarsDataFrameError):
            check_polars_dataframe(df, min_height=1)

    def test_max_height_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, max_height=1)

    def test_max_height_error(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        with raises(CheckPolarsDataFrameError):
            check_polars_dataframe(df, max_height=1)

    def test_schema_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, schema={})

    def test_schema_error(self) -> None:
        df = DataFrame()
        with raises(CheckPolarsDataFrameError):
            check_polars_dataframe(df, schema={"value": Float64})

    def test_shape_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, shape=(0, 0))

    def test_shape_error(self) -> None:
        df = DataFrame()
        with raises(CheckPolarsDataFrameError):
            check_polars_dataframe(df, shape=(1, 1))

    def test_sorted_pass(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        check_polars_dataframe(df, sorted="value")

    def test_sorted_error(self) -> None:
        df = DataFrame({"value": [1.0, 0.0]})
        with raises(CheckPolarsDataFrameError):
            check_polars_dataframe(df, sorted="value")

    def test_unique_pass(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        check_polars_dataframe(df, unique="value")

    def test_unique_error(self) -> None:
        df = DataFrame({"value": [0.0, 0.0]})
        with raises(CheckPolarsDataFrameError):
            check_polars_dataframe(df, unique="value")

    def test_width_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, width=0)

    def test_width_error(self) -> None:
        df = DataFrame()
        with raises(CheckPolarsDataFrameError):
            check_polars_dataframe(df, width=1)


class TestCheckPolarsDataFrameHeight:
    @mark.parametrize("height", [param(10), param((11, 0.1))])
    def test_main(self, *, height: int | tuple[int, float]) -> None:
        df = DataFrame({"value": range(10)})
        check_polars_dataframe_height(df, height)

    @mark.parametrize("height", [param(0), param((12, 0.1))])
    def test_error(self, *, height: int | tuple[int, float]) -> None:
        df = DataFrame({"value": range(10)})
        with raises(CheckPolarsDataFrameHeightError):
            check_polars_dataframe_height(df, height)


class TestJoin:
    def test_main(self) -> None:
        df1 = DataFrame([{"a": 1, "b": 2}], schema={"a": Int64, "b": Int64})
        df2 = DataFrame([{"a": 1, "c": 3}], schema={"a": Int64, "c": Int64})
        result = join(df1, df2, on="a")
        expected = DataFrame(
            [{"a": 1, "b": 2, "c": 3}], schema={"a": Int64, "b": Int64, "c": Int64}
        )
        assert_frame_equal(result, expected)


class TestSetFirstRowAsColumns:
    def test_empty(self) -> None:
        df = DataFrame()
        with raises(SetFirstRowAsColumnsError):
            _ = set_first_row_as_columns(df)

    def test_one_row(self) -> None:
        df = DataFrame(["value"])
        check_polars_dataframe(df, height=1, schema={"column_0": Utf8})
        result = set_first_row_as_columns(df)
        check_polars_dataframe(result, height=0, schema={"value": Utf8})

    def test_multiple_rows(self) -> None:
        df = DataFrame(["foo", "bar", "baz"])
        check_polars_dataframe(df, height=3, schema={"column_0": Utf8})
        result = set_first_row_as_columns(df)
        check_polars_dataframe(result, height=2, schema={"foo": Utf8})
