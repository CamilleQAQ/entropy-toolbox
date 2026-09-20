# Attention entropy

English | [简体中文](../zh-CN/algorithms/attention-entropy.md)

Implemented multiscale method: **MAttEn**.

## Definition

Attention entropy describes the timing of local extrema. It builds interval
sequences between successive maxima, successive minima, and alternating
maximum/minimum pairs, then measures the distribution of each sequence.

## Core steps

At each scale:

1. Construct one standard coarse-grained series.
2. Detect strict local maxima and minima.
3. Form four interval sequences: maximum-to-maximum, minimum-to-minimum,
   maximum-to-minimum, and minimum-to-maximum.
4. Estimate a histogram distribution for each sequence and calculate its
   Shannon entropy.
5. Average the four entropy values:

```math
H_{\mathrm{Att}}
=
\frac{H_{XX}+H_{NN}+H_{XN}+H_{NX}}{4}.
```

## Parameter meanings

- `scale`: largest requested standard multiscale index.

MAttEn has no embedding dimension or amplitude threshold. It requires strict
local maxima and minima after coarse-graining; monotone, constant, or nearly
featureless series may therefore be unsuitable.

## Result

MAttEn returns `scale` values. Each value summarizes how evenly the four
extremum-interval distributions are spread at that scale. Compare signals
using the same sampling, segment length, preprocessing, and scale range.

See [Multiscale constructions](multiscale-constructions.md) and
[Scientific references](../references.md).
