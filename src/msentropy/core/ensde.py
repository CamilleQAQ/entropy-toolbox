"""Ensemble Dispersion Entropy.

The method combines pattern distributions produced by several amplitude
mappings before calculating entropy."""

import numpy as np

from msentropy.core import toolbox
from msentropy.core.disp_en import disp_en


def ensde(
    x: np.ndarray,
    m: int,
    nc: int,
    tau: int,
) -> tuple[float, np.ndarray]:
    """Ensemble Dispersion Entropy.

    The method combines pattern distributions produced by several amplitude
    mappings before calculating entropy."""
    n_patterns = nc**m

    # MA is hard-coded inside the historical reference function.
    ma = [1, 2, 3, 4]

    npdf_lm = np.full(n_patterns, np.nan)
    npdf_ncdf = np.full(n_patterns, np.nan)
    npdf_logsig = np.full(n_patterns, np.nan)
    npdf_tansig = np.full(n_patterns, np.nan)
    npdf_sort = np.full(n_patterns, np.nan)

    if 1 in ma:
        _, npdf_lm = disp_en(x, m, nc, "LM", tau)
    if 2 in ma:
        _, npdf_ncdf = disp_en(x, m, nc, "NCDF", tau)
    if 3 in ma:
        _, npdf_tansig = disp_en(x, m, nc, "TANSIG", tau)
    if 4 in ma:
        _, npdf_logsig = disp_en(x, m, nc, "LOGSIG", tau)
    if 5 in ma:
        # Dead code, exactly as in MATLAB: 5 is not in MA. Kept for
        # structural fidelity; disp_en raises NotImplementedError for
        # SORT if this unreachable branch were enabled.
        _, npdf_sort = disp_en(x, m, nc, "SORT", tau)

    # Column-wise nanmean of the 5-row stack (MATLAB nanmean, default
    # dim = 1), shared with EnsFuDE.
    stack = np.vstack([npdf_lm, npdf_ncdf, npdf_tansig, npdf_logsig, npdf_sort])
    npdf = toolbox.nanmean_columns(stack)

    # Entropy. NaN != 0 is True here, as in MATLAB (npdf ~= 0).
    p = npdf[npdf != 0.0]
    out_disp_en = -np.sum(p * np.log(p))

    return float(out_disp_en), npdf
