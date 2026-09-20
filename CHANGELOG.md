# Changelog

## Unreleased

- Added a consistent high-level API for the numerical implementation modules.
- Added a compact API-level test suite.
- Documented method provenance and third-party licensing scope.
- Added BSD-3-Clause licensing for project-owned code and preserved CC BY 4.0
  terms and attribution for the four MDE/RCMDE-lineage adaptations.
- Added citation metadata and a method-level scientific reference list.
- Organized the README and examples around a beginner-first usage path.
- Added getting-started, method-selection, parameter, preprocessing, signal
  length, missing-data, and result-comparison guidance.
- Added high-level validation for invalid parameter ranges, non-finite input,
  empty signals, and clearly insufficient effective signal length.
- Documented ``gamma`` as the Slope Entropy keyword and supported ``gama`` as
  an alias.
- Added concise algorithm descriptions to core docstrings and documented the
  numerical compatibility policy in ``docs/compatibility.md``.
- Added a family-based mathematical algorithm guide covering definitions,
  calculation steps, parameter meanings, and returned results for every
  registered method.
- Added Simplified Chinese versions of the README, getting-started guide,
  method-selection guide, parameter and data-preparation guide, and algorithm
  manual, with reciprocal language links to the English pages.
- Registered all 20 supported multiscale methods in the high-level API,
  including MSE, MFE, MAttEn, RCMPE, and RCMSlopEn.
