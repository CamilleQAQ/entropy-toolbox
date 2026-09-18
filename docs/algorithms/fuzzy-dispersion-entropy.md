# Fuzzy dispersion entropy

English | [简体中文](../zh-CN/algorithms/fuzzy-dispersion-entropy.md)

Implemented multiscale methods: **MFuDE**, **CMFuDE**, **RCMFuDE**, and
**TSMFuDE**.

## Definition

Fuzzy dispersion entropy replaces the hard class assignment of dispersion
entropy with overlapping membership functions. A sample can contribute
partially to neighboring classes, so small amplitude changes near a class
boundary do not necessarily switch one pattern completely into another.

## Core steps

Map each sample through the normal cumulative distribution function and place
it on the continuous class axis:

$$
y_i
=
\Phi\!\left(\frac{x_i-\mu}{\sigma}\right),
\qquad
z_i=n_c y_i+\frac{1}{2}.
$$

For each class $c\in\{1,\ldots,n_c\}$, calculate a membership
$u_c(z_i)\in[0,1]$. Interior classes use triangular membership functions;
the first and last classes use trapezoidal boundary functions.

For a class pattern

$$
\pi=(c_1,c_2,\ldots,c_m),
$$

the membership of the delayed window beginning at $i$ is

$$
U_i(\pi)
=
\prod_{j=0}^{m-1}
u_{c_{j+1}}\!\left(z_{i+j\tau}\right).
$$

With

$$
W=N-(m-1)\tau
$$

complete windows, estimate the fuzzy pattern distribution:

$$
p(\pi)
=
\frac{1}{W}\sum_{i=1}^{W}U_i(\pi).
$$

Finally,

$$
H_{\mathrm{FuDE}}
=
-\sum_{\pi:p(\pi)>0}p(\pi)\ln p(\pi).
$$

The registered methods use this estimator as follows:

- **MFuDE**: one standard coarse-grained series per scale.
- **CMFuDE**: calculate one entropy per composite offset and average the
  entropy values.
- **RCMFuDE**: average the fuzzy pattern distributions across offsets, then
  calculate entropy.
- **TSMFuDE**: calculate one entropy per time-shift phase and average the
  phase values.

## Parameter meanings

- `m`: number of fuzzy classes in each pattern.
- `nc`: number of fuzzy amplitude classes; the pattern space contains
  $n_c^m$ patterns.
- `tau`: delay between pattern elements, measured in samples.
- `scale`: largest scale for MFuDE, CMFuDE, and RCMFuDE.
- `kmax`: largest time-shift scale for TSMFuDE.
- `type_`: entropy branch selector retained by selected high-level methods.
  Its default is `0`, which is the documented and supported Shannon-entropy
  branch.

## Result

MFuDE, CMFuDE, and RCMFuDE return `scale` values. TSMFuDE returns
`kmax` values. Larger values mean fuzzy dispersion-pattern membership is
spread more evenly across the pattern space.

The result uses the natural logarithm and is not divided by
$\ln(n_c^m)$. Compare signals using the same parameters and multiscale
construction.

See [Multiscale constructions](multiscale-constructions.md) and
[Scientific references](../references.md).
