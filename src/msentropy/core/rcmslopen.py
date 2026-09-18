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
            "rcmslopen: x must be 1-D (MATLAB row convention) or a "
            "vector-shaped 2-D array (1xN or Nx1); general matrices are "
            "not supported. MATLAB would silently linear-index one "
            "(the original accepts this input), but every "
            "other implemented wrapper rejects the convention instead of "
            "reproducing it"
        )
    if scale <= 0:
        raise UnboundLocalError(
            "rcmslopen: output unassigned for scale <= 0, because MATLAB "
            "never initialises RCMSlopE — the only write is "
            "RCMSlopE(j) = ... inside the j = 1:scale loop, so a "
            "non-positive scale leaves the output variable undefined and "
            "MATLAB raises 'MATLAB:unassignedOutputs: Output argument "
            "\"RCMSlopE\" (and possibly others) not assigned a value' "
            "(compatibility testing). Unlike RCMDE/RCMFuDE there is no NaN*ones "
            "pre-fill, and unlike MPE/MSlopEn there is no `= []` either, "
            "so neither a length-1 array nor an empty one is returned"
        )

    # MATLAB indexes x(jj:end) element-wise, so rows and columns yield the
    # same offset slice; a flattened view is sufficient for the coarse
    # graining. The output is grown by the loop from nothing, but the loop
    # always runs at least once (scale >= 1 here), so every element is
    # written.
    x_flat = x_arr.ravel()
    out = np.empty(scale)
    for j in range(1, scale + 1):
        pdf_rows = [
            slop_entropy(coarse_grain(x_flat[jj - 1 :], j), m, delta, gama)[1]
            for jj in range(1, j + 1)
        ]
        # Plain mean over the offset rows, exactly like MATLAB
        # mean(npdf, 1): sequential accumulation seeded with the first row
        # (no +0 identity) then a division by j, so an all--0 column stays
        # negative and NaN propagates through the whole column.
        pdf = pdf_rows[0].copy()
        for row in pdf_rows[1:]:
            pdf = pdf + row
        pdf = pdf / j
        # NaN != 0 is True here, as in MATLAB (npdf ~= 0).
        p = pdf[pdf != 0.0]
        out[j - 1] = -np.sum(p * np.log(p))
    return out
