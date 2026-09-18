# Permutation entropy

English | [简体中文](../zh-CN/algorithms/permutation-entropy.md)

Implemented multiscale methods: **MPE** and **TSMPE**.

## Definition

Permutation entropy describes a signal through the relative ordering of
samples inside delayed embedding windows. It uses ordinal patterns, so adding
a constant or applying a strictly increasing amplitude transformation does not
change the pattern order when no ties are introduced.

## Core steps

For a signal $x=(x_1,\ldots,x_N)$, embedding dimension $m$, and delay
$\tau$, form

```math
\mathbf{x}_i^{(m,\tau)}
=
(x_i,x_{i+\tau},\ldots,x_{i+(m-1)\tau}),
```

for every complete window.

Replace each window by the permutation $\pi$ that sorts its samples in
ascending order. Equal values retain their original order. If $c(\pi)$ is the
number of observed windows with pattern $\pi$, estimate

```math
p(\pi)
=
\frac{c(\pi)}
{N-(m-1)\tau}.
```

The toolbox returns the unnormalized natural-log entropy

```math
H_{\mathrm{PE}}
=
-\sum_{\pi:p(\pi)>0}p(\pi)\ln p(\pi).
```

MPE applies this estimator to the standard coarse-grained series. TSMPE
applies it to every phase at each time-shift scale and averages the phase
values.

## Parameter meanings

- `m`: number of samples in each ordinal window. The number of possible
  patterns is $m!$, so larger values need more observations.
- `tau`: spacing between samples inside a window, measured in samples.
- `scale`: largest standard multiscale index for MPE.
- `kmax`: largest time-shift scale for TSMPE.

## Result

MPE returns `scale` values and TSMPE returns `kmax` values. A larger value
means the ordinal patterns are more evenly distributed for that method and
parameter setting. The value is not normalized by $\ln(m!)$.

See [Multiscale constructions](multiscale-constructions.md) for the difference
between MPE and TSMPE and [Scientific references](../references.md) for the
source publications.
