"""Permutation Entropy with its complete pattern histogram.

This form returns both entropy and the full ordinal-pattern distribution used
by refined composite multiscale permutation entropy."""

import numpy as np

from msentropy.core.permutation_entropy import _pattern_counts


def permutation_entropy_forrcmpe(
    data: np.ndarray, m: int, t: int
) -> tuple[float, np.ndarray]:
    """Permutation Entropy with its complete pattern histogram.

    This form returns both entropy and the full ordinal-pattern distribution used
    by refined composite multiscale permutation entropy."""
    x = np.asarray(data, dtype=np.float64)
    if x.ndim != 1 and not (x.ndim == 2 and x.shape[0] == 1):
        raise ValueError(
            "permutation_entropy_forrcmpe: x must be 1-D or a (1, N) row; "
            "general matrices and (N, 1) columns are not supported"
        )
    if m < 1 or t < 1:
        raise ValueError(
            f"permutation_entropy_forrcmpe: m and t must be >= 1 "
            f"(got m={m}, t={t})"
        )

    x = x.ravel()
    _, _, c_full = _pattern_counts(x, m, t)

    total = c_full.sum()
    if total == 0:
        p_full = np.full(c_full.shape, np.nan)
    else:
        p_full = c_full / total
    nz = p_full[p_full != 0.0]
    pe = -np.sum(nz * np.log(nz))
    return float(pe), p_full
