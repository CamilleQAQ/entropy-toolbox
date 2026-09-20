# Parameters and data preparation

English | [简体中文](zh-CN/parameters.md)

Parameter selection is part of the scientific method. The toolbox rejects
clearly invalid high-level inputs, but it cannot determine which valid settings
are appropriate for a particular dataset.

The mathematical role of each parameter within its estimator is described in
the [algorithm guide](algorithms/index.md).

## Parameter reference

| Parameter | Meaning | High-level requirement | Practical note |
|---|---|---|---|
| `m` | Embedding dimension | Integer, at least 2 | Larger values create more possible patterns and normally require more data. |
| `nc` | Number of dispersion classes | Integer, at least 2 | The number of possible dispersion patterns grows rapidly with `nc` and `m`. |
| `tau` | Delay between embedded samples, measured in samples | Integer, at least 1 | `tau=1` means adjacent samples, not one second. Interpret it using the sampling rate. |
| `scale` | Largest ordinary/composite multiscale index | Integer, at least 1 | The returned array contains scales `1..scale`. Larger scales leave shorter coarse-grained signals. |
| `kmax` | Largest time-shift scale | Integer, at least 1 | The returned TSM array contains indices `1..kmax`. |
| `delta` | Lower Slope Entropy threshold | Finite number, at least 0 | It is expressed in the units of differences in the preprocessed signal. |
| `gamma` | Upper Slope Entropy threshold | Finite number, at least `delta` | The compatibility implementation historically calls this argument `gama`; the high-level API accepts both spellings. |
| `r` | Similarity tolerance for MSE and MFE | Finite number, greater than 0 | The multiscale implementations standardize the complete input signal before coarse-graining, so `r` is interpreted on that standardized scale. |
| `n` | Fuzzy membership exponent for MFE | Finite number, greater than 0 | Controls how rapidly fuzzy similarity decreases with template distance. |
| `type_` | Mapping variant retained by selected fuzzy-dispersion methods | Optional; default `0` | Leave it at the documented default unless reproducing a study that specifies another supported value. |

Values such as `m=3`, `nc=6`, and `tau=1` are common starting examples in this
repository. They are not universal recommendations.

## Signal length and maximum scale

Ordinary coarse-graining reduces the available length. For an input of length
`N`, the series at scale `s` has approximately `floor(N / s)` samples. An
embedding with dimension `m` and delay `tau` then needs samples spanning
`(m - 1) * tau` positions.

For example, a 2,000-sample signal has about 100 coarse-grained samples at
scale 20. Increasing the maximum scale, embedding dimension, or delay reduces
the number of usable patterns. A calculation that is technically possible can
still be statistically weak when very few patterns remain.

The high-level API rejects settings that leave no complete embedding window at
the largest requested scale. It does not guarantee statistical reliability.
There is no single reliable minimum length shared by all methods and signals.
MAttEn has no embedding dimension; it instead requires enough local extrema
after coarse-graining. A signal can satisfy the length check and still be
unsuitable if a scale becomes monotone or nearly featureless.

Before fixing a maximum scale:

1. Calculate the effective length at that scale.
2. Consider the size of the pattern space, particularly for `nc**m`.
3. Inspect whether the end of the entropy curve is supported by enough
   patterns for the intended analysis.
4. Apply the same segment length and scale range to samples being compared.

## Preprocessing

The toolbox does not automatically detrend, filter, resample, normalize,
standardize, or divide a recording into windows. These choices can change the
scientific meaning of the result.

Use one documented preprocessing pipeline for every signal in a comparison.
Record at least:

- original sampling rate and any resampling;
- window length and overlap;
- detrending or filtering;
- amplitude normalization or standardization;
- handling of missing and infinite samples;
- entropy method and every parameter.

Avoid a blanket rule that every signal must be standardized. Ordinal methods
and amplitude-based methods respond differently to transformations. In
particular, `delta` and `gamma` are thresholds on differences: rescaling the
signal without adjusting them changes the symbolization.

## NaN and infinity

The high-level `msentropy.compute` API rejects signals containing `NaN`,
positive infinity, or negative infinity. It does not guess whether a missing
sample should be deleted, interpolated, or used to split a segment.

Check explicitly when preparing data:

```python
if not np.isfinite(x).all():
    raise ValueError("Decide how to handle missing or infinite samples first")
```

The low-level compatibility functions retain the validated historical
behavior, which differs by algorithm and may return non-finite values or raise
method-specific errors. That behavior is useful for reproduction but should
not be treated as automatic missing-data handling.

## Comparing results

Reasonable comparisons include:

- the same method and parameters applied to equally prepared signal segments;
- the curve of one method across its scales;
- multiple methods compared through a defined downstream metric or validation
  experiment.

Do not assume that raw entropy values from MPE, MDE, MFuDE, and other families
share one numerical scale. A larger value from one method does not by itself
mean that method detected more physical complexity than another method.
Changing `m`, `nc`, `tau`, thresholds, or preprocessing can also change the
meaning and range of the result.

For reproducibility, report the method name, package version, all parameters,
input segment length, sampling rate, and preprocessing.
