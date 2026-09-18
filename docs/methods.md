# Method selection

English | [简体中文](zh-CN/methods.md)

The toolbox contains related but non-interchangeable entropy estimators. A
method should be selected from its mathematical meaning, published evidence,
and behavior on the target data—not from whichever method produces the largest
number.

## Family overview

| Family | Registered methods | What is encoded | Practical distinction |
|---|---|---|---|
| [Permutation](algorithms/permutation-entropy.md) | MPE, TSMPE | Relative ordering of samples | Focuses on ordinal patterns rather than their absolute amplitudes. |
| [Slope](algorithms/slope-entropy.md) | MSlopEn, TSMSlopEn | Quantized changes between consecutive samples | Uses amplitude-dependent `delta` and `gamma` thresholds; scaling the signal changes their meaning. |
| [Dispersion](algorithms/dispersion-entropy.md) | MDE, RCMDE, TSMDE | Amplitudes mapped into `nc` discrete classes | A direct starting point when amplitude-distribution patterns are of interest. |
| [Fuzzy dispersion](algorithms/fuzzy-dispersion-entropy.md) | MFuDE, CMFuDE, RCMFuDE, TSMFuDE | Fuzzy memberships of dispersion patterns | Replaces hard class boundaries with fuzzy membership. |
| [Ensemble fuzzy dispersion](algorithms/ensemble-fuzzy-dispersion-entropy.md) | MEFuDE, CMEFuDE, RCMEFuDE, TSMEFuDE | An ensemble of fuzzy mappings | Combines multiple mappings; constant or nearly constant signals require particular care. |

## Multiscale construction

Full definitions and formulas are in
[Multiscale constructions](algorithms/multiscale-constructions.md).

| Prefix or form | Meaning in this toolbox | Consequence |
|---|---|---|
| `M` | Standard multiscale construction | One coarse-grained series is evaluated at each scale. |
| `CM` | Composite multiscale construction | Multiple offsets are evaluated at each scale, using more information and more computation. |
| `RCM` | Refined composite multiscale construction | Offset information is combined at the probability level before entropy is calculated. |
| `TSM` | Time-shift multiscale construction | Time-shifted subsequences are evaluated up to `kmax` instead of using the ordinary `scale` interface. |

## A practical starting decision

- Start with **MDE** when you need a straightforward amplitude-pattern
  multiscale baseline.
- Use **MPE** when relative order is the feature of interest and absolute
  amplitude is not.
- Use **MSlopEn** when the sign and magnitude category of local changes is the
  intended representation. Choose its thresholds in the units of the
  preprocessed signal.
- Consider **CM** or **RCM** variants when the scientific method calls for
  composite coarse-graining. They are not drop-in numerical replacements for
  their standard multiscale counterparts.
- Use a **TSM** method when the time-shift multiscale construction is part of
  the intended analysis.
- Use **TSMEFuDE** when reproducing or extending the method described in the
  project paper.

This is navigation guidance, not a claim that one family is universally more
accurate. Validate the choice on data representative of the intended task and
cite the relevant definition from [Scientific references](references.md).

## Registered signatures

| Method | Full name | High-level parameters |
|---|---|---|
| MPE | Multiscale Permutation Entropy | `m`, `tau`, `scale` |
| MSlopEn | Multiscale Slope Entropy | `m`, `delta`, `gamma`, `scale` |
| MDE | Multiscale Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| MFuDE | Multiscale Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale`, optional `type_` |
| CMFuDE | Composite Multiscale Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale`, optional `type_` |
| RCMFuDE | Refined Composite Multiscale Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale`, optional `type_` |
| MEFuDE | Multiscale Ensemble Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| CMEFuDE | Composite Multiscale Ensemble Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| RCMEFuDE | Refined Composite Multiscale Ensemble Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| RCMDE | Refined Composite Multiscale Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| TSMPE | Time-Shift Multiscale Permutation Entropy | `m`, `tau`, `kmax` |
| TSMSlopEn | Time-Shift Multiscale Slope Entropy | `m`, `delta`, `gamma`, `kmax` |
| TSMDE | Time-Shift Multiscale Dispersion Entropy | `m`, `nc`, `tau`, `kmax` |
| TSMFuDE | Time-Shift Multiscale Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `kmax` |
| TSMEFuDE | Time-Shift Multiscale Ensemble Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `kmax` |
