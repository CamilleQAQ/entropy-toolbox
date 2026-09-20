# Slope entropy

English | [简体中文](../zh-CN/algorithms/slope-entropy.md)

Implemented multiscale methods: **MSlopEn**, **RCMSlopEn**, and **TSMSlopEn**.

## Definition

Slope entropy represents local changes by five symbols. The symbol records
whether a consecutive difference is small, moderately positive or negative,
or strongly positive or negative. Entropy is then calculated from sequences
of those symbols.

## Core steps

For consecutive differences

```math
d_i=x_{i+1}-x_i,
```

assign

```math
s_i=
\begin{cases}
0, & -\delta\le d_i\le\delta,\\
1, & \delta<d_i\le\gamma,\\
2, & d_i>\gamma,\\
-1, & -\gamma\le d_i<-\delta,\\
-2, & d_i<-\gamma.
\end{cases}
```

Create overlapping patterns containing $m-1$ consecutive symbols. If
$p(\mathbf{s})$ is the relative frequency of a symbol pattern, calculate

```math
H_{\mathrm{SlopEn}}
=
-\sum_{\mathbf{s}:p(\mathbf{s})>0}
p(\mathbf{s})\ln p(\mathbf{s}).
```

MSlopEn applies this estimator to standard coarse-grained signals. RCMSlopEn
averages slope-pattern distributions across composite offsets before
calculating entropy. TSMSlopEn calculates the estimator for every time-shift
phase and averages the values.

## Parameter meanings

- `m`: original sample-window dimension; each slope pattern contains
  $m-1$ differences. The current implementation supports $2\le m\le5$.
- `delta`: lower magnitude threshold. Differences within
  $[-\delta,\delta]$ receive symbol 0.
- `gamma`: upper magnitude threshold, with $\gamma\ge\delta$.
- `scale`: largest standard scale for MSlopEn or refined-composite scale for RCMSlopEn.
- `kmax`: largest time-shift scale for TSMSlopEn.

`delta` and `gamma` use the units of differences in the preprocessed
signal. Rescaling the signal without adjusting both thresholds changes the
symbol sequence.

The high-level API uses the spelling `gamma`; `gama` remains an accepted
compatibility spelling.

## Result

MSlopEn and RCMSlopEn return `scale` values; TSMSlopEn returns `kmax` values. A
larger value indicates a more even distribution of slope-symbol patterns for
the selected thresholds and dimension. Values obtained with different
thresholds should not be treated as the same measurement scale.

See [Multiscale constructions](multiscale-constructions.md) and
[Scientific references](../references.md).
