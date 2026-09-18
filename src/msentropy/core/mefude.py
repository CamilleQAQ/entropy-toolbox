"""Multiscale Ensemble Fuzzy Dispersion Entropy.

MEFuDE evaluates ensemble fuzzy dispersion entropy on the signal and on one
non-overlapping coarse-grained series per scale."""

import numpy as np

from msentropy.core.decomposition import coarse_grain
from msentropy.core.ensfude import ensfude

#: Backwards-compatible spelling of
#: :func:`msentropy.core.decomposition.coarse_grain`.
#: Kept as a non-public compatibility alias after the shared implementation
#: moved to ``msentropy.core.decomposition``.
_multi = coarse_grain


def mefude(
    x: np.ndarray,
    m: int,
    nc: int,
    tau: int,
    scale: int,
    type_: int,
) -> np.ndarray:
    """Multiscale Ensemble Fuzzy Dispersion Entropy.

    MEFuDE evaluates ensemble fuzzy dispersion entropy on the signal and on one
    non-overlapping coarse-grained series per scale."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 2 or (x.ndim == 2 and 1 not in x.shape):
        raise ValueError(
            "mefude: x must be 1-D (MATLAB row convention) or a "
            "vector-shaped 2-D array (1xN or Nx1)"
        )

    # MATLAB orientation: a 1-D input acts as a row vector, so the
    # scale-1 transpose quirk feeds EnsFuDE a column.
    as_row = x.reshape(1, -1) if x.ndim == 1 else x

    # MATLAB pre-fills NaN*ones(1, Scale) and overwrites scale 1 plus
    # every scale in 2:Scale; for Scale <= 1 only the first entry is
    # written (see Returns).
    out = np.full(max(scale, 1), np.nan)
    out[0] = ensfude(as_row.T, m, nc, tau)[0]
    for j in range(2, scale + 1):
        out[j - 1] = ensfude(coarse_grain(x, j), m, nc, tau)[0]
    return out
