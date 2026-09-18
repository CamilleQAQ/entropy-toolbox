# Multiscale constructions

English | [简体中文](../zh-CN/algorithms/multiscale-constructions.md)

Let the input signal be

$$
x = (x_1,x_2,\ldots,x_N).
$$

The toolbox combines a single-scale entropy estimator with one of four ways
of representing the signal at increasing scales.

## Standard multiscale

### Definition

Standard multiscale analysis replaces consecutive, non-overlapping blocks of
length $s$ by their means.

### Core steps

At scale $s$, construct

$$
y_j^{(s)}
=
\frac{1}{s}
\sum_{i=(j-1)s+1}^{js}x_i,
\qquad
j=1,\ldots,\left\lfloor\frac{N}{s}\right\rfloor.
$$

Samples at the end that do not complete a block are discarded. Apply the
selected single-scale entropy estimator to $y^{(s)}$ and repeat for
$s=1,\ldots,S$.

### Parameter meanings

- $s$ is one scale.
- `scale=S` is the largest requested scale.
- Larger scales produce shorter coarse-grained series.

### Result

The output is

$$
(H^{(1)},H^{(2)},\ldots,H^{(S)}),
$$

where element `i` of the Python array corresponds to scientific scale
`i + 1`.

## Composite multiscale

### Definition

Composite analysis uses every possible starting offset at a scale instead of
only the first block alignment.

### Core steps

For scale $s$ and offset $r=1,\ldots,s$, construct

$$
y_{r,j}^{(s)}
=
\frac{1}{s}
\sum_{i=0}^{s-1}x_{r+(j-1)s+i}.
$$

Calculate one entropy value $H_r^{(s)}$ for each offset and average them:

$$
H_{\mathrm{CM}}^{(s)}
=
\frac{1}{s}\sum_{r=1}^{s}H_r^{(s)}.
$$

### Parameter meanings

- `scale` has the same meaning as in standard multiscale analysis.
- Scale $s$ produces $s$ offset series and therefore requires more
  computation than the standard construction.

### Result

The output contains one averaged entropy value for every scale from 1 through
`scale`.

## Refined composite multiscale

### Definition

Refined composite analysis combines the pattern distributions from all
offsets before entropy is calculated.

### Core steps

At scale $s$:

1. Construct the $s$ offset series $y_r^{(s)}$.
2. Estimate the pattern distribution
   $\mathbf{p}_r^{(s)}$ for every offset.
3. Average the distributions:

   $$
   \bar{\mathbf{p}}^{(s)}
   =
   \frac{1}{s}\sum_{r=1}^{s}\mathbf{p}_r^{(s)}.
   $$

4. Calculate Shannon entropy from the averaged distribution:

   $$
   H_{\mathrm{RCM}}^{(s)}
   =
   -\sum_c \bar p_c^{(s)}\ln \bar p_c^{(s)}.
   $$

This differs from the composite construction, which averages already
calculated entropy values.

### Parameter meanings

- `scale` is the largest refined-composite scale.
- The entropy-family parameters determine how each offset distribution is
  constructed.

### Result

The output contains one entropy value from the pooled offset distribution at
each scale.

## Time-shift multiscale

### Definition

Time-shift analysis represents scale $k$ with $k$ phase subsequences sampled
at interval $k$.

### Core steps

For phase $\beta=1,\ldots,k$, construct

$$
x_{\beta}^{(k)}
=
(x_\beta,x_{\beta+k},x_{\beta+2k},\ldots).
$$

Calculate the selected entropy for every phase and average:

$$
H_{\mathrm{TSM}}^{(k)}
=
\frac{1}{k}
\sum_{\beta=1}^{k}H\!\left(x_\beta^{(k)}\right).
$$

### Parameter meanings

- `kmax` is the largest time-shift scale.
- At scale $k$, each phase contains approximately $N/k$ samples.
- The entropy-family parameters are applied independently to every phase.

### Result

The output contains one phase-averaged entropy value for each
$k=1,\ldots,k_{\max}$, where `kmax` supplies $k_{\max}$.
