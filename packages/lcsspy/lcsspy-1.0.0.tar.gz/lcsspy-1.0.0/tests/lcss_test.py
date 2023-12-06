import math

import matplotlib as mpl
import numpy as np
import pandas as pd
import pytest

from lcsspy.lcss import _error_messages, continuous_lcss, discrete_lcss

mpl.use("Agg")


@pytest.mark.parametrize(
    "ts1,ts2,epsilon,delta,plot,error",
    [
        (
            [1, 2, 3],
            np.arange(3),
            2.0,
            1,
            True,
            _error_messages["TYPE_MUST_BE_ARRAY_OR_SERIES"].format("ts1"),
        ),
        (
            np.array(["a", "b"]),
            np.arange(3),
            2.0,
            1,
            True,
            _error_messages["DTYPE_MUST_BE_REAL"].format("ts1"),
        ),
        (
            np.array([1.2, 2.3]),
            [5, 7],
            2.0,
            1,
            True,
            _error_messages["TYPE_MUST_BE_ARRAY_OR_SERIES"].format("ts2"),
        ),
        (
            pd.Series([4, 9, 12]),
            pd.Series(["hello", "world"]),
            2.0,
            1,
            True,
            _error_messages["DTYPE_MUST_BE_REAL"].format("ts2"),
        ),
        (
            np.array([2.3, 4.8]),
            pd.Series([6, 14, 22]),
            10,
            1,
            True,
            _error_messages["TYPE_MUST_BE_ONE"].format("epsilon", "float"),
        ),
        (
            np.array([49, 128]),
            np.array([13, 27, 49]),
            4.8,
            3.2,
            False,
            _error_messages["TYPE_MUST_BE_ONE"].format("delta", "int"),
        ),
        (
            pd.Series([42, 45, 67]),
            pd.Series([34.6, 47.8]),
            2.3,
            12,
            "True",
            _error_messages["TYPE_MUST_BE_ONE"].format("plot", "bool"),
        ),
        (
            pd.Series([42, 45, 67]),
            pd.Series([34.6, 47.8]),
            2.3,
            12,
            1,
            _error_messages["TYPE_MUST_BE_ONE"].format("plot", "bool"),
        ),
    ],
)
def test_discrete_lcss_type_exceptions(ts1, ts2, epsilon, delta, plot, error):
    with pytest.raises(TypeError, match=error):
        discrete_lcss(ts1, ts2, epsilon, delta, plot)


@pytest.mark.parametrize(
    "ts1,ts2,epsilon,delta,plot,error",
    [
        (
            np.arange(5),
            pd.Series(
                np.arange(10), index=pd.date_range("2022-01-01", periods=10, freq="m")
            ),
            2.3,
            pd.Timedelta(minutes=2),
            True,
            _error_messages["TYPE_MUST_BE_ONE"].format("ts1", "pandas.Series"),
        ),
        (
            pd.Series(np.arange(8)),
            pd.Series(
                np.arange(10), index=pd.date_range("2022-01-01", periods=10, freq="m")
            ),
            2.3,
            pd.Timedelta(minutes=2),
            True,
            _error_messages["INDEX_MUST_BE_DATETIME"].format("ts1"),
        ),
        (
            pd.Series(
                ["a", "b"], index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            pd.Series(
                np.arange(10), index=pd.date_range("2022-01-01", periods=10, freq="m")
            ),
            2.3,
            pd.Timedelta(minutes=2),
            True,
            _error_messages["DTYPE_MUST_BE_REAL"].format("ts1"),
        ),
        (
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            np.arange(4),
            2.3,
            pd.Timedelta(minutes=2),
            True,
            _error_messages["TYPE_MUST_BE_ONE"].format("ts2", "pandas.Series"),
        ),
        (
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            pd.Series([1, 2, 3]),
            2.3,
            pd.Timedelta(minutes=2),
            False,
            _error_messages["INDEX_MUST_BE_DATETIME"].format("ts2"),
        ),
        (
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            pd.Series(
                ["a", "b"], index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            2.3,
            pd.Timedelta(minutes=2),
            True,
            _error_messages["DTYPE_MUST_BE_REAL"].format("ts2"),
        ),
        (
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            pd.Series(
                np.arange(4), index=pd.date_range("2022-01-01", periods=4, freq="m")
            ),
            6,
            pd.Timedelta(minutes=2),
            True,
            _error_messages["TYPE_MUST_BE_ONE"].format("epsilon", "float"),
        ),
        (
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            pd.Series(
                np.arange(4), index=pd.date_range("2022-01-01", periods=4, freq="m")
            ),
            2.3,
            10,
            True,
            _error_messages["TYPE_MUST_BE_ONE"].format("delta", "pandas.Timedelta"),
        ),
        (
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            pd.Series(
                np.arange(4), index=pd.date_range("2022-01-01", periods=4, freq="m")
            ),
            2.3,
            pd.Timedelta(minutes=2),
            3.5,
            _error_messages["TYPE_MUST_BE_ONE"].format("plot", "bool"),
        ),
    ],
)
def test_continuous_lcss_type_exceptions(ts1, ts2, epsilon, delta, plot, error):
    with pytest.raises(TypeError, match=error):
        continuous_lcss(ts1, ts2, epsilon, delta, plot)


@pytest.mark.parametrize(
    "ts1,ts2,epsilon,delta,plot,error",
    [
        (
            np.arange(2),
            np.arange(2),
            -2.0,
            2,
            True,
            _error_messages["VALUE_MUST_BE_POSITIVE"].format("epsilon"),
        ),
        (
            np.arange(2),
            np.arange(2),
            0.0,
            2,
            True,
            _error_messages["VALUE_MUST_BE_POSITIVE"].format("epsilon"),
        ),
        (
            np.arange(2),
            np.arange(2),
            3.2,
            -2,
            False,
            _error_messages["VALUE_CANNOT_BE_NEGATIVE"].format("delta"),
        ),
    ],
)
def test_discrete_lcss_value_exceptions(ts1, ts2, epsilon, delta, plot, error):
    with pytest.raises(ValueError, match=error):
        discrete_lcss(ts1, ts2, epsilon, delta, plot)


@pytest.mark.parametrize(
    "ts1,ts2,epsilon,delta,plot,error",
    [
        (
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            -3.7,
            pd.Timedelta(minutes=2),
            True,
            _error_messages["VALUE_MUST_BE_POSITIVE"].format("epsilon"),
        ),
        (
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            0.0,
            pd.Timedelta(minutes=2),
            True,
            _error_messages["VALUE_MUST_BE_POSITIVE"].format("epsilon"),
        ),
        (
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            pd.Series(
                np.arange(2), index=pd.date_range("2022-01-01", periods=2, freq="m")
            ),
            2.2,
            pd.Timedelta(minutes=-3),
            True,
            _error_messages["VALUE_ATTRIBUTE_CANNOT_BE_NEGATIVE"].format("delta"),
        ),
    ],
)
def test_continuous_lcss_value_exceptions(ts1, ts2, epsilon, delta, plot, error):
    with pytest.raises(ValueError, match=error):
        continuous_lcss(ts1, ts2, epsilon, delta, plot)


@pytest.mark.parametrize(
    "ts1,ts2,epsilon,delta,plot,expected_value",
    [
        # testing array and series types
        (
            np.array([2, 1, 2, 9, 14, 11, 19, 22]),
            np.array([2, 1, 4, 7, 10, 15, 12, 8, 17]),
            1.1,
            1,
            True,
            0.625,
        ),
        (
            pd.Series([2, 1, 2, 9, 14, 11, 19, 22]),
            np.array([2, 1, 4, 7, 10, 15, 12, 8, 17]),
            1.1,
            1,
            True,
            0.625,
        ),
        (
            pd.Series([2, 1, 2, 9, 14, 11, 19, 22]),
            pd.Series([2, 1, 4, 7, 10, 15, 12, 8, 17]),
            1.1,
            1,
            True,
            0.625,
        ),
        (
            np.array([2, 1, 2, 9, 14, 11, 19, 22]),
            pd.Series([2, 1, 4, 7, 10, 15, 12, 8, 17]),
            1.1,
            1,
            False,
            0.625,
        ),
        # testing time series where one contains ints and the other contains floats
        (
            np.array([9, 15, 18, 23, 29]),
            np.array([10.2, 18.4, 12.3, 28.7]),
            1.5,
            2,
            True,
            0.75,
        ),
        # testing time series containing floats
        (
            np.array([12.3, 8.7, 3.5, 4.2]),
            np.array([11.7, 2.9, 3.8, 10.4]),
            0.9,
            1,
            True,
            0.75,
        ),
        # testing 0 value for epsilon
        (
            np.array([1, 7, 12, 19]),
            np.array([1, 3, 8, 3, 7, 12, 19]),
            0.001,
            3,
            False,
            1.0,
        ),
        # testing 0 value for delta
        (
            np.array([1.2, 3.9, 10.8, 12.6, 17.5]),
            np.array([1.4, 3.5, 7.2, 13.4]),
            0.5,
            0,
            True,
            0.5,
        ),
        # testing 0 values for epsilon and delta at the same time
        (
            np.array([3.8, 12.4, 15.7, -2.4, 12.9, 27.5]),
            np.array([3.9, 12.4, 15.9, -2.4, 11.0, 27.5, 29.4]),
            0.001,
            0,
            False,
            0.5,
        ),
        # testing limit case where value distance is close to epsilon
        (
            np.array([3.5, 10.2, 17.3, 32.1]),
            np.array([1.9, 2.7, 10.4, 17.1, 25.2, 29.7, 32.5]),
            0.81,
            2,
            True,
            0.75,
        ),
        # testing time series with nan values
        (
            np.array([1, 5, np.nan, 7, 9, 12]),
            np.array([np.nan, 1.8, 3.4, 8.7, 13.1]),
            0.9,
            2,
            True,
            0.4,
        ),
    ],
)
def test_discrete_lcss_result(ts1, ts2, epsilon, delta, plot, expected_value):
    assert math.isclose(
        discrete_lcss(ts1, ts2, epsilon, delta, plot).lcss_measure, expected_value
    )


def test_discrete_lcss_plot_result():
    no_plot = discrete_lcss(
        np.array([2, 1, 2, 9, 14, 11, 19, 22]),
        np.array([2, 1, 4, 7, 10, 15, 12, 8, 17]),
        1.1,
        1,
        False,
    )
    assert no_plot.sequence_plot is None and no_plot.series_plot is None
    plot = discrete_lcss(
        np.array([2, 1, 2, 9, 14, 11, 19, 22]),
        np.array([2, 1, 4, 7, 10, 15, 12, 8, 17]),
        1.1,
        1,
        True,
    )
    assert isinstance(plot.sequence_plot, mpl.figure.Figure) and isinstance(
        plot.series_plot, mpl.figure.Figure
    )


@pytest.mark.parametrize(
    "ts1,ts2,epsilon,delta,plot",
    [
        (np.array([]), np.array([1, 2, 3]), 2.2, 3, True),
        (np.array([]), np.array([]), 3.5, 4, False),
    ],
)
def test_discrete_lcss_empty_series(ts1, ts2, epsilon, delta, plot):
    assert math.isnan(discrete_lcss(ts1, ts2, epsilon, delta, plot).lcss_measure)


@pytest.mark.parametrize(
    "ts1,ts2,epsilon,delta,plot,expected_value",
    [
        # testing series containing floats
        (
            pd.Series(
                [12.4, 13.7, 15.8, 8.7],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:23",
                        "2023-11-17 08:43:35",
                        "2023-11-17 08:45:06",
                        "2023-11-17 08:50:23",
                    ]
                ),
            ),
            pd.Series(
                [12.8, 14.2, 19.0, 9.0, 9.2],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:39",
                        "2023-11-17 08:44:02",
                        "2023-11-17 08:45:32",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:51:12",
                    ]
                ),
            ),
            0.9,
            pd.Timedelta(minutes=1),
            True,
            0.75,
        ),
        # testing series containing ints
        (
            pd.Series(
                [12, 13, 15, 8],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:23",
                        "2023-11-17 08:43:35",
                        "2023-11-17 08:45:06",
                        "2023-11-17 08:50:23",
                    ]
                ),
            ),
            pd.Series(
                [13, 14, 19, 9, 9],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:39",
                        "2023-11-17 08:44:02",
                        "2023-11-17 08:45:32",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:51:12",
                    ]
                ),
            ),
            1.5,
            pd.Timedelta(minutes=1),
            True,
            0.75,
        ),
        # testing series where one contains ints and the other contains floats
        (
            pd.Series(
                [12, 13, 15, 8],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:23",
                        "2023-11-17 08:43:35",
                        "2023-11-17 08:45:06",
                        "2023-11-17 08:50:23",
                    ]
                ),
            ),
            pd.Series(
                [13.9, 14.8, 19.2, 9.3, 9.9],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:39",
                        "2023-11-17 08:44:02",
                        "2023-11-17 08:45:32",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:51:12",
                    ]
                ),
            ),
            1.5,
            pd.Timedelta(minutes=1),
            True,
            0.5,
        ),
        # testing 0 value for epsilon
        (
            pd.Series(
                [12.4, 13.7, 15.8, 8.7],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:23",
                        "2023-11-17 08:43:35",
                        "2023-11-17 08:45:06",
                        "2023-11-17 08:50:23",
                    ]
                ),
            ),
            pd.Series(
                [12.4, 14.2, 13.7, 9.0, 8.7],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:39",
                        "2023-11-17 08:44:02",
                        "2023-11-17 08:45:32",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:51:12",
                    ]
                ),
            ),
            0.001,
            pd.Timedelta(minutes=1),
            True,
            0.5,
        ),
        # testing 0 value for delta
        (
            pd.Series(
                [12.4, 13.7, 15.8, 8.7],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:23",
                        "2023-11-17 08:42:39",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:50:23",
                    ]
                ),
            ),
            pd.Series(
                [12.7, 14.2, 13.8, 9.0, 8.4],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:39",
                        "2023-11-17 08:44:02",
                        "2023-11-17 08:45:32",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:51:12",
                    ]
                ),
            ),
            1.3,
            pd.Timedelta(minutes=0),
            True,
            0.25,
        ),
        # testing 0 values for epsilon and delta at the same time
        (
            pd.Series(
                [12.4, 13.8, 15.8, 8.7],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:23",
                        "2023-11-17 08:45:32",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:50:23",
                    ]
                ),
            ),
            pd.Series(
                [12.4, 14.2, 13.8, 9.0, 8.4],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:39",
                        "2023-11-17 08:44:02",
                        "2023-11-17 08:45:32",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:51:12",
                    ]
                ),
            ),
            0.001,
            pd.Timedelta(minutes=0),
            True,
            0.25,
        ),
        # testing limit case where value distance is close to epsilon
        (
            pd.Series(
                [12.4, 13.8, 15.8, 8.7],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:23",
                        "2023-11-17 08:45:38",
                        "2023-11-17 08:46:37",
                        "2023-11-17 08:50:23",
                    ]
                ),
            ),
            pd.Series(
                [13.4, 14.2, 13.8, 9.0, 8.4],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:39",
                        "2023-11-17 08:44:02",
                        "2023-11-17 08:45:32",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:51:12",
                    ]
                ),
            ),
            1.01,
            pd.Timedelta(minutes=1, seconds=30),
            True,
            0.75,
        ),
        # testing series with nan values
        (
            pd.Series(
                [12.4, 13.7, 15.8, np.nan],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:23",
                        "2023-11-17 08:43:35",
                        "2023-11-17 08:45:06",
                        "2023-11-17 08:50:23",
                    ]
                ),
            ),
            pd.Series(
                [12.7, 14.2, np.nan, 9.0, 9.2],
                index=pd.DatetimeIndex(
                    [
                        "2023-11-17 08:42:39",
                        "2023-11-17 08:44:02",
                        "2023-11-17 08:45:32",
                        "2023-11-17 08:49:37",
                        "2023-11-17 08:51:12",
                    ]
                ),
            ),
            0.9,
            pd.Timedelta(minutes=1),
            True,
            0.5,
        ),
    ],
)
def test_continuous_lcss_result(ts1, ts2, epsilon, delta, plot, expected_value):
    assert math.isclose(
        continuous_lcss(ts1, ts2, epsilon, delta, plot).lcss_measure, expected_value
    )


def test_continuous_lcss_plot_result():
    no_plot = continuous_lcss(
        pd.Series(
            [12.4, 13.7, 15.8, 8.7],
            index=pd.DatetimeIndex(
                [
                    "2023-11-17 08:42:23",
                    "2023-11-17 08:43:35",
                    "2023-11-17 08:45:06",
                    "2023-11-17 08:50:23",
                ]
            ),
        ),
        pd.Series(
            [12.8, 14.2, 19.0, 9.0, 9.2],
            index=pd.DatetimeIndex(
                [
                    "2023-11-17 08:42:39",
                    "2023-11-17 08:44:02",
                    "2023-11-17 08:45:32",
                    "2023-11-17 08:49:37",
                    "2023-11-17 08:51:12",
                ]
            ),
        ),
        0.9,
        pd.Timedelta(minutes=1),
        False,
    )
    assert no_plot.sequence_plot is None and no_plot.series_plot is None

    plot = continuous_lcss(
        pd.Series(
            [12.4, 13.7, 15.8, 8.7],
            index=pd.DatetimeIndex(
                [
                    "2023-11-17 08:42:23",
                    "2023-11-17 08:43:35",
                    "2023-11-17 08:45:06",
                    "2023-11-17 08:50:23",
                ]
            ),
        ),
        pd.Series(
            [12.8, 14.2, 19.0, 9.0, 9.2],
            index=pd.DatetimeIndex(
                [
                    "2023-11-17 08:42:39",
                    "2023-11-17 08:44:02",
                    "2023-11-17 08:45:32",
                    "2023-11-17 08:49:37",
                    "2023-11-17 08:51:12",
                ]
            ),
        ),
        0.9,
        pd.Timedelta(minutes=1),
        True,
    )
    assert isinstance(plot.sequence_plot, mpl.figure.Figure) and isinstance(
        plot.series_plot, mpl.figure.Figure
    )


@pytest.mark.parametrize(
    "ts1,ts2,epsilon,delta,plot",
    [
        (
            pd.Series([], dtype=int, index=pd.DatetimeIndex([])),
            pd.Series(
                [1.2, 2.3],
                index=pd.DatetimeIndex(["2023-11-17 08:42:23", "2023-11-17 08:43:35"]),
            ),
            0.8,
            pd.Timedelta(minutes=4),
            False,
        ),
        (
            pd.Series([], dtype=int, index=pd.DatetimeIndex([])),
            pd.Series([], dtype=int, index=pd.DatetimeIndex([])),
            0.8,
            pd.Timedelta(minutes=4),
            False,
        ),
    ],
)
def test_continuous_lcss_empty_series(ts1, ts2, epsilon, delta, plot):
    assert math.isnan(continuous_lcss(ts1, ts2, epsilon, delta, plot).lcss_measure)
