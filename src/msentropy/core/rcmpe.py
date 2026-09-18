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
            "(N, 1) columns are not supported (MATLAB's scale-1 line "
            "transposes the signal and a column then hits an implicit-"
            "broadcasting quirk inside the leaf, see "
            "the documented orientation behavior)"
        )
    # MATLAB indexes x(jj:end) element-wise, so rows and columns yield the
    # same offset slice; a flattened view is sufficient for the coarse
    # graining.
    x_flat = x.ravel()

    # MATLAB pre-fills NaN*ones(1, Scale) and overwrites scale 1 plus
    # every scale in 2:Scale; for Scale <= 1 only the first entry is
    # written (see Returns).
    out = np.full(max(scale, 1), np.nan)

    # CORRECTED scale 1 (the corrected scale-1 policy): the historical reference passes x' here, which makes
    # the leaf see a column and return NaN for every m >= 2. Multi_mu(x, 1)
    # is the identity, so the j = 1 refined-composite value is the bare
    # leaf on the signal -- which is also exactly what the unmodified
    # original returns when it is handed a column.
    out[0] = permutation_entropy_forrcmpe(x, m, tau)[0]

    for j in range(2, scale + 1):
        pdf_rows = [
            permutation_entropy_forrcmpe(coarse_grain(x_flat[jj - 1 :], j), m, tau)[1]
            for jj in range(1, j + 1)
        ]
        # Plain mean over the offset rows, exactly like MATLAB
        # mean(pdf, 1): sequential accumulation seeded with the first row
        # (no +0 identity) then a division by j, so NaN propagates through
        # every column it touches.
        pdf = pdf_rows[0].copy()
        for row in pdf_rows[1:]:
            pdf = pdf + row
        pdf = pdf / j
        # NaN != 0 is True here, as in MATLAB (pdf ~= 0).
        p = pdf[pdf != 0.0]
        out[j - 1] = -np.sum(p * np.log(p))
    return out
