"""Single-scale Slope Entropy.

Consecutive differences are encoded into five symbols using delta and gama
thresholds. Shannon entropy is calculated from length-(m - 1) symbol patterns;
the compatibility implementation supports 2 <= m <= 5."""

from itertools import product

import numpy as np

_SYMBOLS = [-2, -1, 0, 1, 2]

#: Largest supported embedding dimension. The reference pattern generator
#: grows impractically at m=6 (about 5.6 TiB before duplicate rows collapse),
#: so larger dimensions are outside the validated compatibility range.
_MAX_SUPPORTED_M = 5


def slop_entropy(
    x: np.ndarray,
    m: int,
    delta: float,
    gama: float,
) -> tuple[float, np.ndarray]:
    """Single-scale Slope Entropy.

    Consecutive differences are encoded into five symbols using delta and gama
    thresholds. Shannon entropy is calculated from length-(m - 1) symbol patterns;
    the compatibility implementation supports 2 <= m <= 5."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 2 or (x.ndim == 2 and 1 not in x.shape):
        raise ValueError(
            "slop_entropy: x must be 1-D (MATLAB row convention) or a "
            "vector-shaped 2-D array (1xN or Nx1); general matrices are "
            "not supported (MATLAB degenerates to length(x) = max(size) "
            "with linear indexing)"
        )
    if m < 2:
        raise ValueError(
            f"slop_entropy: m must be >= 2 (got m={m}); MATLAB errors on "
            "m <= 1 because the symbol window is never created"
        )
    if m > _MAX_SUPPORTED_M:
        raise ValueError(
            f"slop_entropy: m must be <= {_MAX_SUPPORTED_M} (got m={m}); "
            "the historical reference's all_patterns builder squares its row count at "
            "every symbol column, so m=6 would allocate 390625**2 = "
            "152587890625 rows x 5 columns (~5.6 TiB) and deadlock before "
            "unique() can reduce it. A restated builder CAN compute m=6 "
            "but this compatibility function intentionally supports only "
            "the validated range m=2..5"
        )
    if gama < delta:
        print("gama should be greater than delta ")

    x = x.ravel()
    diffs = np.diff(x)
    symbols = _symbol_map(diffs, delta, gama)
    patterns = _all_patterns(m)

    w = x.size - (m - 1)  # MATLAB N-(m-1): window count / normalizer
    if w <= 0:
        # MATLAB: the window loop never runs, npdf stays 0 and the
        # division by W gives NaN (W == 0) or -0 (W < 0).
        npat = patterns.shape[0]
        with np.errstate(divide="ignore", invalid="ignore"):
            npdf = np.zeros(npat, dtype=np.float64) / w
        p = npdf[npdf != 0]
        with np.errstate(divide="ignore", invalid="ignore"):
            slop_en = -np.sum(p * np.log(p))
        return float(slop_en), npdf

    windows = _symbol_windows(symbols, m, w)
    counts = _count_patterns(patterns, windows)
    npdf = counts / w
    p = npdf[npdf != 0]
    slop_en = -np.sum(p * np.log(p))
    return float(slop_en), npdf


def _symbol_map(diffs: np.ndarray, delta: float, gama: float) -> np.ndarray:
    """Encode consecutive differences into symbols, branch order of the original (first condition wins; NaN differences satisfy no condition and come out NaN — the historical reference assigns nothing to them)."""
    c0 = (-delta <= diffs) & (diffs <= delta)
    c1 = (delta < diffs) & (diffs <= gama)
    c2 = gama < diffs
    c3 = (-gama <= diffs) & (diffs < -delta)
    c4 = diffs < -gama
    return np.select([c0, c1, c2, c3, c4], [0, 1, 2, -1, -2], default=np.nan)


def _all_patterns(m: int) -> np.ndarray:
    """All ``5^(m-1)`` symbol patterns in ascending row order."""
    return np.array(
        list(product(_SYMBOLS, repeat=m - 1)), dtype=np.int64
    ).reshape(-1, m - 1)


def _symbol_windows(symbols: np.ndarray, m: int, w: int) -> np.ndarray:
    """Per-window symbol rows with the historical reference's NaN semantics."""
    win = np.empty((w, m - 1), dtype=np.float64)
    buf = np.full(m - 1, np.nan)
    for j in range(w):
        for p in range(m - 1):
            s = symbols[j + p]
            if not np.isnan(s):
                buf[p] = s
        if j == 0:
            if np.isnan(buf[-1]):
                if np.all(np.isnan(buf)):
                    raise UnboundLocalError(
                        "slop_entropy: NaN differences left every symbol "
                        "of the first window unassigned; MATLAB errors "
                        "with 'MATLAB:UndefinedFunction: 函数或变量 "
                        "'Symbx_temp' 无法识别'"
                    )
                raise ValueError(
                    "slop_entropy: a NaN difference left the last symbol "
                    "of the first window unassigned; MATLAB errors with "
                    "'MATLAB:subsassigndimmismatch' because the symbol "
                    "row is shorter than m-1"
                )
            # Holes below the last assigned position fill with implicit 0.
            buf[np.isnan(buf)] = 0.0
        win[j] = buf
    return win


def _count_patterns(patterns: np.ndarray, windows: np.ndarray) -> np.ndarray:
    """Histogram of window rows against the pattern rows (exact integer arithmetic; every window matches exactly one pattern when its symbols are all real, and a window with filled/stale symbols is counted against the pattern it equals)."""
    npat = patterns.shape[0]
    length = patterns.shape[1]
    weights = np.power(5, np.arange(length, dtype=np.int64))
    pattern_keys = (patterns + 2) @ weights
    window_keys = (windows + 2).astype(np.int64) @ weights
    order = np.argsort(pattern_keys)
    pos = np.searchsorted(pattern_keys[order], window_keys)
    return np.bincount(order[pos], minlength=npat)
