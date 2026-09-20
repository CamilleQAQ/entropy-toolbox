"""Attention entropy and its strict peak detector.

The method forms maximum-to-maximum, minimum-to-minimum, and alternating
extremum interval sequences, computes one histogram entropy per sequence, and
returns their unweighted mean. See docs/references.md for the publication."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

__all__ = ["peak_find", "attention_entropy"]


def peak_find(x: ArrayLike) -> np.ndarray:
    """Indices of the strict local maxima of ``x``, as ``PeakFind``."""
    x_arr = np.asarray(x, dtype=np.float64).ravel()
    nx = x_arr.size
    indx = np.zeros(nx, dtype=np.intp)
    for n in range(2, nx):
        if (x_arr[n - 2] < x_arr[n - 1]) and (x_arr[n - 1] > x_arr[n]):
            indx[n - 1] = n
        elif (x_arr[n - 2] < x_arr[n - 1]) and (x_arr[n - 1] == x_arr[n]):
            k = 1
            # Place a flat maximum at the midpoint of its plateau.
            while (n + k) < nx and x_arr[n - 1] == x_arr[n + k - 1]:
                k += 1
            if x_arr[n - 1] > x_arr[n + k - 1]:
                indx[n - 1] = n + (k - 1) // 2
    # Stored positions are one-based until the final conversion.
    return indx[indx != 0] - 1


def _histcounts_unit_edges(values: np.ndarray, n_bins: int) -> np.ndarray:
    """Replicate ``histcounts(values, 1:n_bins+1)`` for integer edges."""
    counts = np.zeros(n_bins, dtype=np.float64)
    if n_bins <= 0 or values.size == 0:
        return counts
    in_range = np.isfinite(values) & (values >= 1.0) & (values <= n_bins + 1.0)
    kept = np.floor(values[in_range]).astype(np.intp) - 1
    # The right-closed last bin is the only place floor() overshoots.
    kept = np.minimum(kept, n_bins - 1)
    return np.bincount(kept, minlength=n_bins).astype(np.float64)


def _channel_entropy(
    intervals: np.ndarray, n_bins: int
) -> tuple[np.ndarray, np.float64]:
    """One channel: histogram, normalize to a pdf, drop zeros, Shannon sum."""
    counts = _histcounts_unit_edges(intervals, n_bins)
    with np.errstate(divide="ignore", invalid="ignore"):
        p_full = counts / np.sum(counts)
    p_kept = p_full[p_full != 0]
    return p_full, np.float64(-np.sum(p_kept * np.log(p_kept)))


def attention_entropy(
    x: ArrayLike,
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Attention entropy and its strict peak detector.

    The method forms maximum-to-maximum, minimum-to-minimum, and alternating
    extremum interval sequences, computes one histogram entropy per sequence, and
    returns their unweighted mean. See docs/references.md for the publication."""
    x_arr = np.asarray(x, dtype=np.float64)
    if x_arr.ndim > 2 or (x_arr.ndim == 2 and 1 not in x_arr.shape):
        raise ValueError(
            "attention_entropy: x must be 1-D or a vector-shaped 2-D array; "
            "general matrices are not supported"
        )
    x_arr = x_arr.ravel()
    n = x_arr.size
    if n < 3:
        raise ValueError(
            "attention_entropy: x must contain at least 3 samples"
        )

    x_max = peak_find(x_arr)
    x_min = peak_find(-x_arr)
    if x_max.size == 0 or x_min.size == 0:
        raise ValueError(
            "attention_entropy: x has no strict local "
            f"{'maximum' if x_max.size == 0 else 'minimum'} "
            f"({x_max.size} maxima, {x_min.size} minima for N={n})"
        )

    t_xx = np.diff(x_max)
    t_nn = np.diff(x_min)
    temp = np.diff(np.sort(np.concatenate((x_max, x_min))))

    # The first extremum determines which alternating interval starts first.
    if x_max[0] < x_min[0]:
        t_xn = temp[0::2]
        t_nx = temp[1::2]
    else:
        t_xn = temp[1::2]
        t_nx = temp[0::2]

    n_bins = n - 2
    p_nx, e_nx = _channel_entropy(t_nx, n_bins)
    p_nn, e_nn = _channel_entropy(t_nn, n_bins)
    p_xx, e_xx = _channel_entropy(t_xx, n_bins)
    p_xn, e_xn = _channel_entropy(t_xn, n_bins)

    att_e = (e_nn + e_xx + e_xn + e_nx) / 4
    return float(att_e), p_nx, p_nn, p_xx, p_xn
