"""Refined Composite Multiscale Slope Entropy.

The method combines slope-pattern distributions across all composite offsets
before calculating entropy at each scale."""

import numpy as np

from msentropy.core.decomposition import coarse_grain
from msentropy.core.slop_entropy import slop_entropy


def rcmslopen(
    x: np.ndarray,
    m: int,
    delta: float,
    gama: float,
    scale: int,
) -> np.ndarray:
    """Refined Composite Multiscale Slope Entropy.

    The method combines slope-pattern distributions across all composite offsets
    before calculating entropy at each scale."""
    x_arr = np.asarray(x, dtype=np.float64)
    if x_arr.ndim > 2 or (x_arr.ndim == 2 and 1 not in x_arr.shape):
        raise ValueError(
            "rcmslopen: x must be 1-D or a vector-shaped 2-D array; "
            "general matrices are not supported"
        )
    if scale <= 0:
        raise UnboundLocalError(
            "rcmslopen: scale must be positive"
        )

    x_flat = x_arr.ravel()
    out = np.empty(scale)
    for j in range(1, scale + 1):
        pdf_rows = [
            slop_entropy(coarse_grain(x_flat[jj - 1 :], j), m, delta, gama)[1]
            for jj in range(1, j + 1)
        ]
        # Average distributions before calculating entropy.
        pdf = pdf_rows[0].copy()
        for row in pdf_rows[1:]:
            pdf = pdf + row
        pdf = pdf / j
        p = pdf[pdf != 0.0]
        out[j - 1] = -np.sum(p * np.log(p))
    return out
