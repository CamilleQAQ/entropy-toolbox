# Changelog

## Unreleased

- Created a clean distribution tree for the Python toolbox.
- Kept the 15-method high-level API and all numerical implementation modules.
- Added a compact API-level test suite for the public distribution.
- Completed the provenance review and excluded non-distributed MATLAB
  validation material.
- Added BSD-3-Clause licensing for project-owned code and preserved CC BY 4.0
  terms and attribution for the four MDE/RCMDE-lineage adaptations.
- Added citation metadata and a method-level scientific reference list.
- Reworked the README and examples around a beginner-first usage path.
- Added getting-started, method-selection, parameter, preprocessing, signal
  length, missing-data, and result-comparison guidance.
- Added high-level validation for invalid parameter ranges, non-finite input,
  empty signals, and clearly insufficient effective signal length.
- Made ``gamma`` the documented Slope Entropy keyword while retaining
  ``gama`` as a backward-compatible alias.
- Simplified core docstrings into concise algorithm descriptions
  and moved the compatibility policy to ``docs/compatibility.md``.
- Added a family-based mathematical algorithm guide covering definitions,
  calculation steps, parameter meanings, and returned results for all 15
  registered methods.
- Added Simplified Chinese versions of the README, getting-started guide,
  method-selection guide, parameter and data-preparation guide, and algorithm
  manual, with reciprocal language links to the English pages.
