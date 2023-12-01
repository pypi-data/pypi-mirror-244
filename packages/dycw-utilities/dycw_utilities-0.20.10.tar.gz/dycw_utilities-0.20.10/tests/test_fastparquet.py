from __future__ import annotations

from collections.abc import Mapping, Sequence
from collections.abc import Set as AbstractSet
from pathlib import Path
from typing import Any, cast

from fastparquet import write
from hypothesis import assume, given
from hypothesis.extra.pandas import column, data_frames, range_indexes
from hypothesis.strategies import (
    DataObject,
    SearchStrategy,
    booleans,
    data,
    dictionaries,
    floats,
    integers,
    lists,
    none,
    sampled_from,
    sets,
    tuples,
)
from numpy import float32, nan
from pandas import DataFrame, RangeIndex, Series, concat
from pandas.testing import assert_frame_equal, assert_series_equal
from pytest import mark, param, raises

from utilities.fastparquet import (
    _PARQUET_DTYPES,
    GetParquetFileError,
    WriteParquetCoreError,
    _get_parquet_file,
    count_rows,
    get_columns,
    get_dtypes,
    get_num_row_groups,
    read_parquet,
    write_parquet,
)
from utilities.hypothesis import dates_pd, lists_fixed_length, temp_paths, text_ascii
from utilities.numpy import dt64ns
from utilities.pandas import Int64, astype, string
from utilities.pytest import skipif_windows


class TestCountRows:
    @given(rows=lists(booleans(), min_size=1), root=temp_paths())
    def test_main(self, *, rows: Sequence[bool], root: Path) -> None:
        n = len(rows)
        df = DataFrame(rows, index=RangeIndex(n), columns=["value"])
        write_parquet(df, path := root.joinpath("df.parq"))
        result = count_rows(path)
        assert result == n


class TestGetColumns:
    @given(columns=sets(text_ascii()), root=temp_paths())
    def test_main(self, *, columns: AbstractSet[str], root: Path) -> None:
        as_list = list(columns)
        df = DataFrame(nan, index=RangeIndex(1), columns=as_list, dtype=float)
        write_parquet(df, path := root.joinpath("df.parq"))
        result = get_columns(path)
        assert result == as_list


class TestGetDtypes:
    @given(
        dtypes=dictionaries(
            text_ascii(), sampled_from(sorted(_PARQUET_DTYPES, key=repr))
        ),
        root=temp_paths(),
    )
    def test_main(self, *, dtypes: Mapping[str, Any], root: Path) -> None:
        df = DataFrame(None, index=RangeIndex(1), columns=list(dtypes))
        df = astype(df, dtypes)
        write_parquet(df, path := root.joinpath("df.parq"))
        result = get_dtypes(path)
        assert result == dtypes


class TestGetNumRowGroups:
    def test_main(self, *, tmp_path: Path) -> None:
        df = DataFrame(0.0, index=RangeIndex(2), columns=["value"])
        write_parquet(df, path := tmp_path.joinpath("df.parq"), row_group_offsets=1)
        result = get_num_row_groups(path)
        expected = 2
        assert result == expected


class TestGetParquetFile:
    def test_main(self, *, tmp_path: Path) -> None:
        path = tmp_path.joinpath("file")
        df = DataFrame(0.0, index=RangeIndex(1), columns=["value"])
        write(path, df)
        _ = _get_parquet_file(path)

    def test_get_row_group(self, *, tmp_path: Path) -> None:
        path = tmp_path.joinpath("file")
        df = DataFrame(0.0, index=RangeIndex(2), columns=["value"])
        write(path, df, row_group_offsets=1)
        _ = _get_parquet_file(path, row_group=0)
        _ = _get_parquet_file(path, row_group=1)
        with raises(GetParquetFileError):
            _ = _get_parquet_file(path, row_group=2)

    @mark.parametrize("as_str", [param(True), param(False, marks=skipif_windows)])
    def test_error(self, *, tmp_path: Path, as_str: bool) -> None:
        path = tmp_path.joinpath("file")
        path_use = str(path) if as_str else path
        with raises(FileNotFoundError):
            _ = _get_parquet_file(path_use)


class TestReadAndWriteParquet:
    @given(data=data(), root=temp_paths(), as_series=booleans())
    @mark.parametrize(
        ("elements", "dtype"),
        [
            param(booleans(), bool),
            param(dates_pd() | none(), dt64ns),
            param(floats(-10.0, 10.0) | none(), float),
            param(integers(-10, 10) | none(), Int64),
            param(text_ascii() | none(), string),
        ],
    )
    def test_writing_df(
        self,
        *,
        data: DataObject,
        elements: SearchStrategy[Any],
        dtype: Any,
        root: Path,
        as_series: bool,
    ) -> None:
        rows = data.draw(lists(elements, min_size=1))
        n = len(rows)
        df = DataFrame(rows, index=RangeIndex(n), columns=["value"])
        df = astype(df, dtype)
        write_parquet(df, path := root.joinpath("df.parq"))
        head = data.draw(sampled_from([n, None]))
        columns = "value" if as_series else None
        read = read_parquet(path, head=head, columns=columns)
        if as_series:
            assert isinstance(read, Series)
            assert_series_equal(read, df["value"])
        else:
            assert isinstance(read, DataFrame)
            assert_frame_equal(read, df)

    @given(value1=floats(), value2=floats(), root=temp_paths())
    def test_writing_iterable_of_dfs(
        self, *, value1: float, value2: float, root: Path
    ) -> None:
        df = DataFrame([[value1], [value2]], index=RangeIndex(2), columns=["value"])
        parts = [df.iloc[:1], df.iloc[1:].reset_index(drop=True)]
        write_parquet(parts, path := root.joinpath("df.parq"))
        result = read_parquet(path)
        assert_frame_equal(result, df)

    @given(data=data(), column1=text_ascii(), column2=text_ascii(), root=temp_paths())
    def test_series_from_dataframe_with_two_string_columns(
        self, *, data: DataObject, column1: str, column2: str, root: Path
    ) -> None:
        _ = assume(column1 != column2)
        elements = text_ascii() | none()
        rows = data.draw(lists(tuples(elements, elements), min_size=1))
        df = DataFrame(
            rows, index=RangeIndex(len(rows)), columns=[column1, column2], dtype=string
        )
        write_parquet(df, path := root.joinpath("df.parq"))
        sr = read_parquet(path, columns=column1)
        assert_series_equal(sr, df[column1])

    @given(value1=floats(), value2=floats(), root=temp_paths())
    def test_read_row_groups(self, *, value1: float, value2: float, root: Path) -> None:
        df = DataFrame([[value1], [value2]], index=RangeIndex(2), columns=["value"])
        write_parquet(df, path := root.joinpath("df.parq"), row_group_offsets=1)
        result1 = read_parquet(path, row_group=0)
        expected1 = df.iloc[:1]
        assert_frame_equal(result1, expected1)
        result2 = read_parquet(path, row_group=1)
        expected2 = df.iloc[1:].reset_index(drop=True)
        assert_frame_equal(result2, expected2)
        with raises(GetParquetFileError):
            _ = read_parquet(path, row_group=2)

    @given(
        data=data(),
        root=temp_paths(),
        num_dfs=integers(1, 10),
        row_group_offsets=integers(1, 10),
    )
    def test_iterable_of_dfs_with_strings(
        self, *, data: DataObject, root: Path, num_dfs: int, row_group_offsets: int
    ) -> None:
        def as_str(df: DataFrame, /) -> DataFrame:
            return astype(df, string)

        elements = data_frames(
            [cast(Any, column)("value", elements=text_ascii())],
            index=range_indexes(min_size=1),
        ).map(as_str)
        dfs = data.draw(lists_fixed_length(elements, num_dfs))
        write_parquet(
            dfs, path := root.joinpath("df.parq"), row_group_offsets=row_group_offsets
        )
        result = read_parquet(path)
        expected = concat(dfs).reset_index(drop=True)
        assert_frame_equal(result, expected)


class TestWriteParquetCore:
    @given(value=text_ascii(), root=temp_paths())
    def test_strings_are_stored_as_objects(self, *, value: str, root: Path) -> None:
        df = DataFrame(value, index=RangeIndex(1), columns=["value"], dtype=string)
        write_parquet(df, path := root.joinpath("df.parq"))
        file = _get_parquet_file(path)
        dtypes = file.dtypes
        expected = {"value": object}
        assert dtypes == expected

    def test_extra_dtype(self, *, tmp_path: Path) -> None:
        df = DataFrame(nan, index=RangeIndex(1), columns=["value"], dtype=float32)
        write_parquet(df, tmp_path.joinpath("df.parq"), extra_dtypes={"value": float32})

    @mark.parametrize(
        "df",
        [
            param(DataFrame()),
            param(
                DataFrame(nan, index=RangeIndex(1), columns=["value"], dtype=float32)
            ),
        ],
    )
    def test_error(self, *, df: DataFrame, tmp_path: Path) -> None:
        with raises(WriteParquetCoreError):
            write_parquet(df, tmp_path.joinpath("df.parq"))

    def test_extra_dtype_ignored(self, *, tmp_path: Path) -> None:
        df = DataFrame(nan, index=RangeIndex(1), columns=["value"], dtype=float32)
        with raises(WriteParquetCoreError):
            write_parquet(
                df, tmp_path.joinpath("df.parq"), extra_dtypes={"other": float32}
            )
