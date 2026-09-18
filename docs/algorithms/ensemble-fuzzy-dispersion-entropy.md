# Ensemble fuzzy dispersion entropy

English | [简体中文](../zh-CN/algorithms/ensemble-fuzzy-dispersion-entropy.md)

Implemented multiscale methods: **MEFuDE**, **CMEFuDE**, **RCMEFuDE**, and
**TSMEFuDE**.

## Definition

Ensemble fuzzy dispersion entropy calculates fuzzy pattern distributions
under several amplitude mappings and combines them into one distribution.
The purpose of the ensemble is to avoid making the result depend on only one
mapping of amplitude into fuzzy classes.

## Core steps

For one input series, construct four mapped versions:

1. **LM**: linear min–max mapping.
2. **NCDF**: normal-CDF mapping followed by min–max mapping.
3. **TANSIG**: standardized samples passed through a hyperbolic-tangent
   sigmoid and then min–max mapped.
4. **LOGSIG**: standardized samples passed through a logistic sigmoid and
   then min–max mapped.

For each mapping $q$, calculate the fuzzy dispersion pattern distribution
$\mathbf{p}^{(q)}$ described in
[Fuzzy dispersion entropy](fuzzy-dispersion-entropy.md). Combine the four
distributions component by component:

```math
\bar{\mathbf{p}}
=
\frac{1}{4}
\sum_{q=1}^{4}\mathbf{p}^{(q)}.
```

Calculate

```math
H_{\mathrm{EFuDE}}
=
-\sum_{\pi:\bar p(\pi)>0}
\bar p(\pi)\ln\bar p(\pi).
```

The multiscale variants then apply different constructions:

- **MEFuDE**: ensemble entropy on one standard coarse-grained series per
  scale.
- **CMEFuDE**: ensemble entropy for every composite offset, followed by an
  average of the entropy values.
- **RCMEFuDE**: average the ensemble pattern distributions across composite
  offsets, then calculate entropy.
- **TSMEFuDE**: ensemble entropy for every time-shift phase, followed by an
  average of the phase values.

## Parameter meanings

- `m`: number of fuzzy classes in each pattern.
- `nc`: number of fuzzy amplitude classes; there are $n_c^m$ possible
  class patterns.
- `tau`: delay between pattern elements, measured in samples.
- `scale`: largest scale for MEFuDE, CMEFuDE, and RCMEFuDE.
- `kmax`: largest time-shift scale for TSMEFuDE.

The sigmoid mappings standardize the input by its standard deviation.
Constant or nearly constant series can therefore be unsuitable for this
family. Detect and handle dead or constant channels before feature
extraction.

## Result

MEFuDE, CMEFuDE, and RCMEFuDE return `scale` values. TSMEFuDE returns
`kmax` values. Each element summarizes the ensemble fuzzy pattern
distribution under the corresponding multiscale construction.

The values use the natural logarithm and are not normalized by
$\ln(n_c^m)$. Keep the method, parameters, segment length, and preprocessing
fixed when comparing signals.

See [Multiscale constructions](multiscale-constructions.md) and
[Scientific references](../references.md).
