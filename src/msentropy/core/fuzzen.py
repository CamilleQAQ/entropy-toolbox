"""Single-scale Fuzzy Entropy.

Fuzzy Entropy compares embedded templates with an exponential membership of
their Chebyshev distance and returns the logarithmic ratio for dimensions
m and m + 1."""

import numpy as np

from msentropy.core.sampen import _as_integral, _matlab_divide, _matlab_max
from msentropy.core.toolbox import downsample


def fuzzen(
    x: np.ndarray,
    m: int,
    r: float,
    n: float = 2,
    tau: int = 1,
) -> tuple[float, np.ndarray]:
    """Single-scale Fuzzy Entropy.

    Fuzzy Entropy compares embedded templates with an exponential membership of
    their Chebyshev distance and returns the logarithmic ratio for dimensions
    m and m + 1."""
    x_arr = np.asarray(x, dtype=np.float64)
    if x_arr.ndim > 2 or (x_arr.ndim == 2 and 1 not in x_arr.shape):
        raise ValueError(
            "fuzzen: x must be 1-D (MATLAB row convention) or a "
            "vector-shaped 2-D array (1xN or Nx1); general matrices are "
            "not supported. MATLAB silently linear-indexes one "
            "(compatibility testing), but every other implemented leaf rejects the "
            "convention instead of reproducing it (the supported entropy branch0)"
        )
    m = _as_integral(m, "fuzzen: m")
    if m < 1:
        raise ValueError(
            f"fuzzen: m must be >= 1, got {m}. MATLAB errors here as well "
            "-- m = 0 or m < 0 gives MATLAB:matrix:"
            "singleSubscriptNumelMismatch, so the guard mirrors the "
            "original rather than adding a restriction"
        )

    if tau > 1:
        x_arr = downsample(x_arr, _as_integral(tau, "fuzzen: tau"))

    # MATLAB indexes element-wise, so the flattened signal is what the
    # template matrix is built from; accepted shapes are all vectors.
    x_flat = x_arr.ravel()
    size = x_flat.size
    nm = size - m
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
        for i in range(1, max(size - k, 0) + 1):
            # MATLAB tempMat(:, i+1:N-m) has max(N-m-i, 0) columns, and
            # repmat(tempMat(:,i), 1, N-m-i) broadcasts that column across
            # them. The subtraction below is the same broadcast.
            n_cols = max(nm - i, 0)
            window = temp_mat[:, i : i + n_cols]
            anchor = temp_mat[:, i - 1 : i]
            dist = _matlab_max(np.abs(window - anchor))
            # MATLAB DF = exp((-dist.^n)/r). The exponentiation is done
            # under errstate because r = 0, r < 0 and n < 0 are all legal
            # inputs that legitimately produce Inf/NaN memberships
            # rather than programming errors.
            with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
                df = np.exp(-(dist**n) / r)
            count[i - 1] = _matlab_divide(np.sum(df), nm)
        p[k - m] = _matlab_divide(float(np.sum(count)), nm)

    with np.errstate(divide="ignore", invalid="ignore"):
        entropy = float(np.log(_matlab_divide(p[0], p[1])))
    return entropy, p
