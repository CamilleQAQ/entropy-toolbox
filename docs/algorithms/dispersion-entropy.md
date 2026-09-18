# Dispersion entropy

English | [简体中文](../zh-CN/algorithms/dispersion-entropy.md)

Implemented multiscale methods: **MDE**, **RCMDE**, and **TSMDE**.

## Definition

Dispersion entropy maps amplitudes into `nc` discrete classes, forms delayed
class patterns, and measures how evenly those patterns occur. Unlike
permutation entropy, amplitude location affects the assigned pattern.

## Core steps

Estimate the signal mean $\mu$ and sample standard deviation $\sigma$. Map
each sample with the normal cumulative distribution function:

```math
y_i
=
\Phi\!\left(\frac{x_i-\mu}{\sigma}\right),
\qquad 0\le y_i\le1.
```

Convert the mapped value to a class

```math
z_i
=
\mathrm{round}\!\left(n_c y_i+\frac{1}{2}\right),
\qquad
z_i\in\{1,\ldots,n_c\}.
```

Form delayed dispersion patterns

```math
\mathbf{z}_i^{(m,\tau)}
=
(z_i,z_{i+\tau},\ldots,z_{i+(m-1)\tau}).
```

There are at most $n_c^m$ possible patterns. From their observed relative
frequencies $p(\pi)$, calculate

```math
H_{\mathrm{DE}}
=
-\sum_{\pi:p(\pi)>0}p(\pi)\ln p(\pi).
```

The multiscale variants combine this estimator with different constructions:

- **MDE** uses one standard coarse-grained series per scale and keeps the
  original signal's mapping statistics across scales.
- **RCMDE** averages pattern distributions over all composite offsets before
  calculating entropy.
- **TSMDE** calculates dispersion entropy separately for each time-shift
  phase and averages the phase values.

## Parameter meanings

- `m`: number of classes in each delayed pattern. The pattern space grows
  as $n_c^m$.
- `nc`: number of amplitude classes.
- `tau`: delay between pattern elements, measured in samples.
- `scale`: largest scale for MDE or RCMDE.
- `kmax`: largest time-shift scale for TSMDE.

Increasing `m`, `nc`, or `tau` normally requires a longer signal to
estimate the pattern distribution.

## Result

MDE and RCMDE return `scale` values; TSMDE returns `kmax` values. Larger
values mean the observed dispersion patterns are more evenly distributed for
that method and parameter setting.

The result is not divided by $\ln(n_c^m)$. Changing `m` or `nc` therefore
changes both the pattern space and the possible numerical range.

See [Multiscale constructions](multiscale-constructions.md) and
[Scientific references](../references.md).
