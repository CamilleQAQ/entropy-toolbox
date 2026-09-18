"""Multiscale Sample Entropy with mean coarse-graining.

The signal is standardized once, coarse-grained at each scale, and evaluated
with single-scale sample entropy."""

import numpy as np
from numpy.typing import ArrayLike

from msentropy.core.decomposition import coarse_grain
from msentropy.core.sampen import _as_integral, sampen

__all__ = ["mse_mu"]


def _standardize(x_flat: np.ndarray) -> np.ndarray:
    """MATLAB ``x = x - mean(x); x = x./std(x);`` on a flattened signal."""
    n = x_flat.size
    with np.errstate(invalid="ignore", divide="ignore"):
        if n == 0:
            centered = x_flat - np.nan
            sd = np.nan
        else:
            centered = x_flat - float(np.mean(x_flat))
            sd = 0.0 if n == 1 else float(np.std(centered, ddof=1))
        return centered / sd


def mse_mu(
    x: ArrayLike,
    m: int,
    r: float,
    tau: int,
    scale: int,
) -> np.ndarray:
    """Multiscale Sample Entropy with mean coarse-graining.

    The signal is standardized once, coarse-grained at each scale, and evaluated
    with single-scale sample entropy."""
    x_arr = np.asarray(x, dtype=np.float64)
    if x_arr.ndim > 2 or (x_arr.ndim == 2 and 1 not in x_arr.shape):
        raise ValueError(
            "mse_mu: x must be 1-D (MATLAB row convention) or a "
            "vector-shaped 2-D array (1xN or Nx1); general matrices are "
            "not supported. MATLAB would silently linear-index one, but "
            "every other implemented wrapper rejects the convention instead of "
            "reproducing it (the supported entropy branch0)"
        )
    scale = _as_integral(scale, "mse_mu: scale")

    # MATLAB indexes the samples element-wise, so the flattened signal is
    # what every step below consumes; the accepted shapes are all vectors.
    x_flat = x_arr.ravel()

    # MATLAB pre-fills NaN*ones(1, Scale) and then writes index 1 plus
    # 2:Scale, i.e. every index; for Scale <= 0 the pre-fill is 1-by-0 and
    # the Out_MSE(1) write grows it to exactly one element.
    out = np.full(max(scale, 1), np.nan)

    x_std = _standardize(x_flat)

    # Scale 1 is a direct leaf call: no coarse graining, and it is evaluated
    # BEFORE the loop, so a leaf failure fires there first.
    out[0] = sampen(x_std, m, r, tau)[0]

    for j in range(2, scale + 1):
        out[j - 1] = sampen(coarse_grain(x_std, j), m, r, tau)[0]
    return out
