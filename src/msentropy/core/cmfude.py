"""Composite Multiscale Fuzzy Dispersion Entropy.

At each scale, CMFuDE evaluates fuzzy dispersion entropy on every composite
coarse-graining offset and averages the resulting entropy values."""

import numpy as np

from msentropy.core.decomposition import coarse_grain
from msentropy.core.fuzzy_disen_ncdf_cumulative import (
    fuzzy_disen_ncdf_cumulative,
)


def cmfude(
    x: np.ndarray,
    m: int,
    nc: int,
    tau: int,
    scale: int,
    type_: int,
) -> np.ndarray:
    """Composite Multiscale Fuzzy Dispersion Entropy.

    At each scale, CMFuDE evaluates fuzzy dispersion entropy on every composite
    coarse-graining offset and averages the resulting entropy values."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 2 or (x.ndim == 2 and 1 not in x.shape):
        raise ValueError(
            "cmfude: x must be 1-D (MATLAB row convention) or a "
            "vector-shaped 2-D array (1xN or Nx1)"
        )

    # MATLAB indexes x(jj:end) element-wise and the nested Multi always
    # emits a row, so the two orientations are indistinguishable (P4).
    x_flat = x.ravel()

    if scale < 1:
        raise UnboundLocalError(
            "CMFuDE: output unassigned (the MATLAB 1:scale loop is "
            "empty and the output variable is never written), matching "
            "the MATLAB-compatible error for scale <= 0"
        )

    out = np.empty(scale)
    with np.errstate(divide="ignore", invalid="ignore"):
        for j in range(1, scale + 1):
            vals = [
                fuzzy_disen_ncdf_cumulative(
                    coarse_grain(x_flat[jj - 1 :], j), m, nc, tau, type_
                )[0]
                for jj in range(1, j + 1)
            ]
            # MATLAB mean of the offset column: sequential accumulation
            # seeded with the first element (this preserves -0 in every
            # isolated check).
            total = vals[0]
            for value in vals[1:]:
                total = total + value
            out[j - 1] = total / j
    return out
