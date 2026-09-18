# Algorithm guide

English | [简体中文](../zh-CN/algorithms/index.md)

This guide explains the 15 methods exposed by `msentropy.compute`. Each page
uses the same structure: definition, core steps, parameter meanings, and
result.

## Read in this order

1. [Multiscale constructions](multiscale-constructions.md) explains the
   standard, composite, refined-composite, and time-shift constructions.
2. Select the single-scale entropy family:
   - [Permutation entropy](permutation-entropy.md)
   - [Slope entropy](slope-entropy.md)
   - [Dispersion entropy](dispersion-entropy.md)
   - [Fuzzy dispersion entropy](fuzzy-dispersion-entropy.md)
   - [Ensemble fuzzy dispersion entropy](ensemble-fuzzy-dispersion-entropy.md)

## Method map

| High-level method | Entropy family | Multiscale construction |
|---|---|---|
| MPE | Permutation entropy | Standard |
| MSlopEn | Slope entropy | Standard |
| MDE | Dispersion entropy | Standard |
| MFuDE | Fuzzy dispersion entropy | Standard |
| CMFuDE | Fuzzy dispersion entropy | Composite |
| RCMFuDE | Fuzzy dispersion entropy | Refined composite |
| MEFuDE | Ensemble fuzzy dispersion entropy | Standard |
| CMEFuDE | Ensemble fuzzy dispersion entropy | Composite |
| RCMEFuDE | Ensemble fuzzy dispersion entropy | Refined composite |
| RCMDE | Dispersion entropy | Refined composite |
| TSMPE | Permutation entropy | Time shift |
| TSMSlopEn | Slope entropy | Time shift |
| TSMDE | Dispersion entropy | Time shift |
| TSMFuDE | Fuzzy dispersion entropy | Time shift |
| TSMEFuDE | Ensemble fuzzy dispersion entropy | Time shift |

All entropy values in the registered methods use the natural logarithm and
are returned without dividing by a theoretical maximum. Consequently, raw
values from different families or parameter settings should not be assumed to
share one numerical scale.

The publications associated with each family are listed in
[Scientific references](../references.md).
