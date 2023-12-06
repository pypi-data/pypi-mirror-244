"""Provides functions to compute the LCSS similarity measure."""
from dataclasses import dataclass
from typing import Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.api.types import is_any_real_numeric_dtype

_error_messages = {
    "TYPE_MUST_BE_ONE": "The type of parameter {0} must be {1}.",
    "TYPE_MUST_BE_ARRAY_OR_SERIES": (
        "The type of parameter {0} must be numpy.ndarray or pandas.Series."
    ),
    "INDEX_MUST_BE_DATETIME": (
        "The index object of parameter {0} must be of pandas.DateTimeIndex type."
    ),
    "DTYPE_MUST_BE_REAL": (
        "The values within parameter {0} must be of a real number dtype."
    ),
    "VALUE_CANNOT_BE_NEGATIVE": "Parameter {0} cannot be negative.",
    "VALUE_ATTRIBUTE_CANNOT_BE_NEGATIVE": (
        "The value attribute of parameter {0} cannot be negative."
    ),
    "VALUE_MUST_BE_POSITIVE": "Parameter {0} must be positive.",
}


@dataclass
class LcssResult:
    """Represents the outcome of the LCSS algorithm.

    Attributes:
        lcss_measure: LCSS similarity measure. Belongs to the range [0, 1].
        series_plot: Figure object displaying the input time series and
            their matched elements (with green lines).
        sequence_plot: Figure object displaying the elements of the input
            time series that are part of the longest common subsequence.
    """

    lcss_measure: float
    series_plot: Union[mpl.figure.Figure, None]
    sequence_plot: Union[mpl.figure.Figure, None]


def _validate_discrete_ts(ts, ts_name):
    if not (isinstance(ts, (np.ndarray, pd.Series))):
        raise TypeError(_error_messages["TYPE_MUST_BE_ARRAY_OR_SERIES"].format(ts_name))
    elif not (is_any_real_numeric_dtype(ts.dtype)):
        raise TypeError(_error_messages["DTYPE_MUST_BE_REAL"].format(ts_name))


def _validate_continuous_ts(ts, ts_name):
    if not (isinstance(ts, pd.Series)):
        raise TypeError(
            _error_messages["TYPE_MUST_BE_ONE"].format(ts_name, "pandas.Series")
        )
    elif not (isinstance(ts.index, pd.DatetimeIndex)):
        raise TypeError(_error_messages["INDEX_MUST_BE_DATETIME"].format(ts_name))
    elif not (is_any_real_numeric_dtype(ts.dtype)):
        raise TypeError(_error_messages["DTYPE_MUST_BE_REAL"].format(ts_name))


def _validate_epsilon(epsilon):
    if not (isinstance(epsilon, float)):
        raise TypeError(_error_messages["TYPE_MUST_BE_ONE"].format("epsilon", "float"))
    elif epsilon <= 0:
        raise ValueError(_error_messages["VALUE_MUST_BE_POSITIVE"].format("epsilon"))


def _validate_plot(plot):
    if not (isinstance(plot, bool)):
        raise TypeError(_error_messages["TYPE_MUST_BE_ONE"].format("plot", "bool"))


def _validate_discrete_delta(delta):
    if not (isinstance(delta, int)):
        raise TypeError(_error_messages["TYPE_MUST_BE_ONE"].format("delta", "int"))
    elif delta < 0:
        raise ValueError(_error_messages["VALUE_CANNOT_BE_NEGATIVE"].format("delta"))


def _validate_continuous_delta(delta):
    if not (isinstance(delta, pd.Timedelta)):
        raise TypeError(
            _error_messages["TYPE_MUST_BE_ONE"].format("delta", "pandas.Timedelta")
        )
    elif delta.value < 0:
        raise ValueError(
            _error_messages["VALUE_ATTRIBUTE_CANNOT_BE_NEGATIVE"].format("delta")
        )


def _validate_discrete_lcss(ts1, ts2, epsilon, delta, plot):
    _validate_discrete_ts(ts1, "ts1")
    _validate_discrete_ts(ts2, "ts2")
    _validate_epsilon(epsilon)
    _validate_discrete_delta(delta)
    _validate_plot(plot)


def _validate_continuous_lcss(ts1, ts2, epsilon, delta, plot):
    _validate_continuous_ts(ts1, "ts1")
    _validate_continuous_ts(ts2, "ts2")
    _validate_epsilon(epsilon)
    _validate_continuous_delta(delta)
    _validate_plot(plot)


def discrete_lcss(
    ts1: Union[np.ndarray, pd.Series],
    ts2: Union[np.ndarray, pd.Series],
    epsilon: float,
    delta: int,
    plot: bool,
) -> LcssResult:
    """Computes LCSS between time series with discrete time indexes.

    Both time series can contain missing values in the form of :obj:`numpy.nan`.
    If a :class:`Series<pandas.Series>` object is supplied, it will be converted
    to a :class:`ndarray<numpy.ndarray>`, discarding its
    :attr:`index<pandas.Series.index>` in the process.

    Args:
        ts1: First time series. Must contain either integer or float values.
        ts2: Second time series. Must contain either integer or float values.
        epsilon: An upper bound to distances between time series values: elements
            can be matched only if their value distance is less than such
            threshold. Must be strictly positive.
        delta: An upper bound to distances between time series indexes: elements
            can be matched only if their index distance is less than or equal to
            such threshold. Must be positive.
        plot: Indicates whether the function will return plots or not.

    Returns:
        A :class:`LcssResult` object.

    """
    _validate_discrete_lcss(ts1, ts2, epsilon, delta, plot)

    if isinstance(ts1, pd.Series):
        ts1 = ts1.to_numpy()
    if isinstance(ts2, pd.Series):
        ts2 = ts2.to_numpy()

    ts1_size = ts1.size
    ts2_size = ts2.size

    C = np.zeros(shape=(ts1_size + 1, ts2_size + 1), dtype=int)

    for i in range(ts1_size):
        for j in range(ts2_size):
            if abs(i - j) <= delta and abs(ts1[i] - ts2[j]) < epsilon:
                C[i + 1, j + 1] = C[i, j] + 1
            else:
                C[i + 1, j + 1] = max(C[i + 1, j], C[i, j + 1])

    path_length = C[ts1_size, ts2_size]
    lcss_measure = path_length / min(ts1_size, ts2_size)

    if plot:
        path = np.zeros(shape=(2, path_length), dtype=int)
        i = ts1_size - 1
        j = ts2_size - 1
        column_count = path_length - 1

        while i >= 0 and j >= 0:
            if abs(i - j) <= delta and abs(ts1[i] - ts2[j]) < epsilon:
                path[:, column_count] = [i, j]
                column_count = column_count - 1
                i = i - 1
                j = j - 1
            elif C[i + 1, j] > C[i, j + 1]:
                j = j - 1
            else:
                i = i - 1

        ts1_indexes = path[0, :]
        ts2_indexes = path[1, :]
        ts1_values = ts1[ts1_indexes]
        ts2_values = ts2[ts2_indexes]
        path_values = np.array([ts1_values, ts2_values])

        fig1, ax1 = plt.subplots()
        ax1.plot(ts1, "-o", color="blue", label="ts1")
        ax1.plot(ts2, "-o", color="red", label="ts2")
        ax1.plot(
            path,
            path_values,
            color="green",
            linestyle="dashed",
            alpha=0.5,
            label="alignment_path",
        )

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax1.legend(by_label.values(), by_label.keys())
        ax1.set_title("Input time series and alignment of matched elements")

        fig2, ax2 = plt.subplots()
        ax2.plot(ts1_values, "-o", color="blue", label="ts1_sequence")
        ax2.plot(ts2_values, "-o", color="red", label="ts2_sequence")
        ax2.legend()
        ax2.set_title("Retrieved common subsequence")
        return LcssResult(
            lcss_measure=lcss_measure, series_plot=fig1, sequence_plot=fig2
        )
    else:
        return LcssResult(
            lcss_measure=lcss_measure, series_plot=None, sequence_plot=None
        )


def continuous_lcss(
    ts1: pd.Series, ts2: pd.Series, epsilon: float, delta: pd.Timedelta, plot: bool
) -> LcssResult:
    """Computes LCSS between time series with continuous time indexes.

    Both time series can contain missing values in the form of :obj:`numpy.nan`.
    It's expected that each series has sorted and unique timestamps.

    Args:
        ts1: First time series. The :attr:`index<pandas.Series.index>` property
            of **ts1** must be of type
            :class:`DatetimeIndex<pandas.DatetimeIndex>`. Must contain either
            integer or float values.
        ts2: Second time series. The :attr:`index<pandas.Series.index>` property
            of **ts2** must be of type
            :class:`DatetimeIndex<pandas.DatetimeIndex>`. Must contain either
            integer or float values.
        epsilon: An upper bound to distances between time series values: elements
            can be matched only if their value distance is less than such
            threshold. Must be strictly positive.
        delta: An upper bound to distances between time series indexes: elements
            can be matched only if their index distance is less than or equal to
            such threshold. The :attr:`value<pandas.Timedelta.value>` property
            of **delta** must be positive.
        plot: Indicates whether the function will return plots or not.

    Returns:
        A :class:`LcssResult` object.

    """
    _validate_continuous_lcss(ts1, ts2, epsilon, delta, plot)

    ts1_size = ts1.size
    ts2_size = ts2.size
    delta_nanoseconds = delta.value
    ts1_index = ts1.index
    ts2_index = ts2.index

    C = np.zeros(shape=(ts1_size + 1, ts2_size + 1), dtype=int)

    for i in range(ts1_size):
        for j in range(ts2_size):
            if (
                abs(ts1_index[i].value - ts2_index[j].value) <= delta_nanoseconds
                and abs(ts1.iloc[i] - ts2.iloc[j]) < epsilon
            ):
                C[i + 1, j + 1] = C[i, j] + 1
            else:
                C[i + 1, j + 1] = max(C[i + 1, j], C[i, j + 1])

    path_length = C[ts1_size, ts2_size]
    lcss_measure = path_length / min(ts1_size, ts2_size)

    if plot:
        path = np.zeros(shape=(2, path_length), dtype=int)
        i = ts1_size - 1
        j = ts2_size - 1
        column_count = path_length - 1

        while i >= 0 and j >= 0:
            if (
                abs(ts1_index[i].value - ts2_index[j].value) <= delta_nanoseconds
                and abs(ts1.iloc[i] - ts2.iloc[j]) < epsilon
            ):
                path[:, column_count] = [i, j]
                column_count = column_count - 1
                i = i - 1
                j = j - 1
            elif C[i + 1, j] > C[i, j + 1]:
                j = j - 1
            else:
                i = i - 1

        ts1_indexes = path[0, :]
        ts2_indexes = path[1, :]

        path = np.array([ts1_index.values[ts1_indexes], ts2_index.values[ts2_indexes]])

        ts1_values = ts1.iloc[ts1_indexes]
        ts2_values = ts2.iloc[ts2_indexes]
        path_values = np.array([ts1_values, ts2_values])

        fig1, ax1 = plt.subplots()
        ax1.plot(ts1, "-o", color="blue", label="ts1")
        ax1.plot(ts2, "-o", color="red", label="ts2")
        ax1.plot(
            path,
            path_values,
            color="green",
            linestyle="dashed",
            alpha=0.5,
            label="alignment_path",
        )

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax1.legend(by_label.values(), by_label.keys())
        ax1.set_title("Input time series and alignment of matched elements")

        fig2, ax2 = plt.subplots()
        ax2.plot(ts1_values, "-o", color="blue", label="ts1_sequence")
        ax2.plot(ts2_values, "-o", color="red", label="ts2_sequence")
        ax2.legend()
        ax2.set_title("Retrieved common subsequence")

        return LcssResult(
            lcss_measure=lcss_measure, series_plot=fig1, sequence_plot=fig2
        )
    else:
        return LcssResult(
            lcss_measure=lcss_measure, series_plot=None, sequence_plot=None
        )
