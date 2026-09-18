"""Refined Composite Multiscale Ensemble Fuzzy Dispersion Entropy.

The method combines ensemble fuzzy pattern distributions across all composite
offsets before calculating entropy at each scale."""

import numpy as np

from msentropy.core.decomposition import coarse_grain
from msentropy.core.ensfude import ensfude


def rcmefude(
    x: np.ndarray,
    m: int,
    nc: int,
    tau: int,
    scale: int,
    type_: int,
) -> np.ndarray:
    """Refined Composite Multiscale Ensemble Fuzzy Dispersion Entropy.

    The method combines ensemble fuzzy pattern distributions across all composite
    offsets before calculating entropy at each scale."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 2 or (x.ndim == 2 and 1 not in x.shape):
        raise ValueError(
            "rcmefude: x must be 1-D (MATLAB row convention) or a "
            "vector-shaped 2-D array (1xN or Nx1)"
        )

    # MATLAB orientation: a 1-D input acts as a row vector, so the
    # scale-1 transpose quirk feeds EnsFuDE a column.
    as_row = x.reshape(1, -1) if x.ndim == 1 else x
    # MATLAB indexes x(jj:end) element-wise: rows and columns yield the
    # same offset slice, so a flattened view is sufficient.
    x_flat = x.ravel()

    # MATLAB pre-fills NaN*ones(1, Scale) and overwrites scale 1 plus
    # every scale in 2:Scale; for Scale <= 1 only the first entry is
    # written (see Returns).
    out = np.full(max(scale, 1), np.nan)
    out[0] = ensfude(as_row.T, m, nc, tau)[0]

    with np.errstate(divide="ignore", invalid="ignore"):
        for j in range(2, scale + 1):
            pdf_rows = [
                ensfude(coarse_grain(x_flat[jj - 1 :], j), m, nc, tau)[1]
                for jj in range(1, j + 1)
            ]
            # Plain mean over the offset rows, exactly like MATLAB
            # mean(pdf, 1): NaN propagates. numpy's
            # pairwise summation may differ from MATLAB's sequential
            # sum by ~1e-16; the reference tolerances absorb this.
            pdf_mean = np.mean(pdf_rows, axis=0)
            # NaN != 0 is True here, as in MATLAB (pdf ~= 0).
            p = pdf_mean[pdf_mean != 0.0]
            out[j - 1] = -np.sum(p * np.log(p))
    return out
