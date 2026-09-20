"""Multiscale Attention Entropy.

The method applies attention entropy to the original signal and to one
non-overlapping coarse-grained series per scale."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

from msentropy.core.attention_entropy import attention_entropy
from msentropy.core.decomposition import coarse_grain

__all__ = ["multiscale_attention_entropy"]


def multiscale_attention_entropy(
    data: ArrayLike, scale: int | float
) -> np.ndarray:
    """Multiscale Attention Entropy.

    The method applies attention entropy to the original signal and to one
    non-overlapping coarse-grained series per scale."""
    data_arr = np.asarray(data, dtype=np.float64)
    if data_arr.ndim > 2 or (data_arr.ndim == 2 and 1 not in data_arr.shape):
        raise ValueError(
            "multiscale_attention_entropy: data must be 1-D or a "
            "vector-shaped 2-D array; general matrices are not supported"
        )

    # The direct compatibility function truncates finite fractional scales.
    if not np.isfinite(scale):
        raise ValueError(
            "multiscale_attention_entropy: scale must be finite"
        )
    n_scales = max(int(np.trunc(scale)), 0)

    out = np.empty(n_scales, dtype=np.float64)
    for j in range(1, n_scales + 1):
        att_e, *_ = attention_entropy(coarse_grain(data_arr, j))
        out[j - 1] = att_e
    return out
