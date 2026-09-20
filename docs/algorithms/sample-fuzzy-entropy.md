# Sample and fuzzy entropy

English | [简体中文](../zh-CN/algorithms/sample-fuzzy-entropy.md)

Implemented multiscale methods: **MSE** and **MFE**.

## Definition

Sample entropy and fuzzy entropy compare delayed templates of length `m` and
`m + 1`. MSE counts pairs whose Chebyshev distance is below a hard tolerance.
MFE replaces that hard decision with a continuous fuzzy membership.

## Core steps

The complete input signal is standardized once. At each scale, the selected
standard coarse-grained series is divided into delayed templates. For two
templates with Chebyshev distance `d`, MSE uses the match rule

```math
d < r.
```

MFE instead assigns the membership

```math
\mu(d)=\exp\!\left(-\frac{d^n}{r}\right).
```

Let `P_m` and `P_{m+1}` denote the resulting average match quantities for
dimensions `m` and `m + 1`. Both methods calculate

```math
H=\ln\!\left(\frac{P_m}{P_{m+1}}\right).
```

The calculation is repeated on one standard coarse-grained series for every
scale.

## Parameter meanings

- `m`: template dimension.
- `r`: positive similarity tolerance on the standardized signal.
- `n`: positive fuzzy-membership exponent used only by MFE.
- `tau`: delay between template samples, measured in samples.
- `scale`: largest requested standard multiscale index.

## Result

MSE and MFE return `scale` values. Larger values indicate that matches become
less likely when the template dimension increases, under the selected method
and parameters. MSE and MFE values are not interchangeable because their
similarity rules differ.

See [Multiscale constructions](multiscale-constructions.md) and
[Scientific references](../references.md).
