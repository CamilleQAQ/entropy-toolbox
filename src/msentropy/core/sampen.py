"""Single-scale Sample Entropy.

Sample Entropy compares delayed templates with a Chebyshev-distance threshold
and returns the logarithmic ratio of matches for dimensions m and m + 1."""

import numpy as np

from msentropy.core.toolbox import downsample


def _matlab_max(a: np.ndarray) -> np.ndarray:
    """MATLAB ``max`` over the leading non-singleton dimension, NaN-ignoring."""
    if a.size == 0:
        return np.empty(0, dtype=np.float64)
    values = a.ravel() if a.shape[0] == 1 else a
    masked = np.where(np.isnan(values), -np.inf, values)
    reduced = np.max(masked, axis=0)
    return np.where(np.all(np.isnan(values), axis=0), np.nan, reduced)


def _matlab_divide(numerator: float, denominator: float) -> float:
    """MATLAB ``/`` on doubles: ``0/0 -> NaN``, ``0/negative -> -0.0``."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(np.float64(numerator) / np.float64(denominator))


def _as_integral(value, name: str) -> int:
    """Coerce a MATLAB integer-VALUED scalar to ``int``, or raise."""
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer, got a bool")
    try:
        as_float = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be an integer, got {value!r}") from exc
    if not np.isfinite(as_float) or as_float != int(as_float):
        raise ValueError(
            f"{name} must be an integer-valued scalar, got {value!r} "
            "(MATLAB:NonIntegerInput from zeros)"
        )
    return int(as_float)


def sampen(
    x: np.ndarray,
    m: int,
    r: float,
    tau: int = 1,
) -> tuple[float, np.ndarray]:
    """Single-scale Sample Entropy.

    Sample Entropy compares delayed templates with a Chebyshev-distance threshold
    and returns the logarithmic ratio of matches for dimensions m and m + 1."""
    x_arr = np.asarray(x, dtype=np.float64)
    if x_arr.ndim > 2 or (x_arr.ndim == 2 and 1 not in x_arr.shape):
        raise ValueError(
            "sampen: x must be 1-D (MATLAB row convention) or a "
            "vector-shaped 2-D array (1xN or Nx1); general matrices are "
            "not supported. MATLAB silently linear-indexes one "
            "(the original accepts this input), but every "
            "other implemented leaf rejects the convention instead of "
            "reproducing it (the supported entropy branch0)"
        )
    m = _as_integral(m, "sampen: m")
    if m < 1:
        raise ValueError(
            f"sampen: m must be >= 1, got {m}. MATLAB errors here as well "
            "-- m = 0 or m < 0 makes sum(D) stop matching the single "
            "count(i) slot (MATLAB:matrix:singleSubscriptNumelMismatch), "
            "so the guard mirrors the historical reference rather than adding a "
            "restriction"
        )

    if tau > 1:
        x_arr = downsample(x_arr, _as_integral(tau, "sampen: tau"))

    # MATLAB indexes element-wise, so the flattened signal is what the
    # template matrix is built from; accepted shapes are all vectors.
    x_flat = x_arr.ravel()
    n = x_flat.size
    nm = n - m
    width = max(nm, 0)

    x_mat = np.zeros((m + 1, width), dtype=np.float64)
    for i in range(1, m + 2):
        # MATLAB x(i : N-m+i-1), an INCLUSIVE range whose length is
        # max(N-m, 0) for every i >= 1 -- which is exactly `width`. The
        # length is computed explicitly rather than left to a Python
        # slice, because a negative stop would silently mean "from the
        # end" in Python instead of "empty".
        start = i - 1
        x_mat[i - 1, :] = x_flat[start : start + width]

    p = np.zeros(2, dtype=np.float64)
    for k in (m, m + 1):
        count = np.zeros(width, dtype=np.float64)
        temp_mat = x_mat[:k, :]
        for i in range(1, max(n - k, 0) + 1):
            # MATLAB tempMat(:, i+1:N-m) has max(N-m-i, 0) columns, and
            # repmat(tempMat(:,i), 1, N-m-i) broadcasts that column across
            # them. The subtraction below is the same broadcast.
            n_cols = max(nm - i, 0)
            window = temp_mat[:, i : i + n_cols]
            anchor = temp_mat[:, i - 1 : i]
            dist = _matlab_max(np.abs(window - anchor))
            count[i - 1] = _matlab_divide(np.count_nonzero(dist < r), nm)
        p[k - m] = _matlab_divide(float(np.sum(count)), nm)

    with np.errstate(divide="ignore", invalid="ignore"):
        entropy = float(np.log(_matlab_divide(p[0], p[1])))
    return entropy, p
