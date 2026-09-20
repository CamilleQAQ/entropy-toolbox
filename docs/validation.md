# Validation

The numerical code in this distribution was validated during development
against independently generated reference outputs and targeted edge-case
experiments.

The broader numerical validation included:

- 1,490 passing pytest cases;
- 975 reference files;
- coverage of the core multiscale method families and their numerical leaves;
- explicit checks for shapes, NaN/Inf propagation, signed zero, input
  orientation, degenerate windows and floating-point tolerances.

The generated reference artifacts are not required for installing or using
the package.

The compact public test suite focuses on the supported API contract:

- the complete 20-method multiscale registry;
- parameter signatures and aliases;
- bit-identical forwarding between the high-level API and numerical layer
  for valid inputs;
- row/column normalization;
- error reporting;
- a finite end-to-end curve from every registered method.

The public suite is not a replacement for the broader numerical equivalence
suite. Numerical changes require additional regression evaluation before they
are included in a release.
