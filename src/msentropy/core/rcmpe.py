"""Refined Composite Multiscale Permutation Entropy.

The method combines ordinal-pattern distributions across all composite
offsets before calculating entropy at each scale."""

import numpy as np

from msentropy.core.decomposition import coarse_grain
from msentropy.core.permutation_entropy_forrcmpe import (
    permutation_entropy_forrcmpe,
)


def rcmpe(x: np.ndarray, m: int, tau: int, scale: int) -> np.ndarray:
    """Refined Composite Multiscale Permutation Entropy.

    The method combines ordinal-pattern distributions across all composite
    offsets before calculating entropy at each scale."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 1 and not (x.ndim == 2 and x.shape[0] == 1):
        raise ValueError(
            "rcmpe: x must be 1-D or a (1, N) row; general matrices and "
            "(N, 1) columns are not supported"
        )
    x_flat = x.ravel()

    out = np.full(max(scale, 1), np.nan)

    # At scale 1 the identity coarse-graining reduces to the single-scale leaf.
    out[0] = permutation_entropy_forrcmpe(x, m, tau)[0]

    for j in range(2, scale + 1):
        pdf_rows = [
            permutation_entropy_forrcmpe(coarse_grain(x_flat[jj - 1 :], j), m, tau)[1]
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
