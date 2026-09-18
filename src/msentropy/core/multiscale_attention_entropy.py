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
            "multiscale_attention_entropy: data must be 1-D (MATLAB row "
            "convention) or a vector-shaped 2-D array (1xN or Nx1); "
            "general matrices are not supported. MATLAB silently "
            "linear-indexes one, but every other implemented family rejects "
            "the convention instead of reproducing it (the supported entropy branch0)"
        )

    # MATLAB `for j = 1:scale` with a double endpoint: the colon operator
    # truncates a fractional endpoint towards zero through fix(), and
    # rejects a non-finite endpoint (scale = 2.5 -> two
    # iterations, scale = NaN -> MATLAB:colon:nonFiniteEndpoint).
    if not np.isfinite(scale):
        raise ValueError(
            "multiscale_attention_entropy: scale must be finite; MATLAB's "
            "`1:scale` rejects a non-finite endpoint with "
            "MATLAB:colon:nonFiniteEndpoint"
        )
    n_scales = max(int(np.trunc(scale)), 0)

    # MATLAB: MAttE = [] plus the `1:scale` loop; a non-positive scale
    # leaves the loop empty, so the empty array itself is returned and the
    # leaf is never called.
    out = np.empty(n_scales, dtype=np.float64)
    for j in range(1, n_scales + 1):
        # MATLAB: Xs = Multi(data, j); [AttE, ~, ~, ~, ~] = AttentionEntropy(Xs)
        # — the four pdfs are requested and discarded.
        att_e, *_ = attention_entropy(coarse_grain(data_arr, j))
        out[j - 1] = att_e
    return out
