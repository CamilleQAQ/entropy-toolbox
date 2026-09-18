# Numerical compatibility

The numerical functions in `msentropy.core` were validated against reference
outputs. Validation also covered unusual inputs such as empty signals,
non-positive scales, non-finite samples, constant signals, row/column
orientation, and floating-point reduction order.

Core source files document the algorithm and important scientific limitations.

## What the compatibility API preserves

Direct functions under `msentropy.core` retain the validated implementation
behavior, including method-specific behavior on degenerate inputs. Depending
on the function, such inputs may produce an empty array, `NaN`, infinity,
signed zero, or a method-specific exception.

The high-level `msentropy.compute` API rejects common invalid inputs before
they reach those functions. Use the high-level API for new analysis and call
the compatibility functions directly only when reproducing historical
behavior or investigating an implementation in detail.

## Floating-point agreement

MATLAB and NumPy can use different reduction orders or elementary-math
implementations. That can produce a difference in the final binary digits
without changing the scientific result. Validation distinguishes numerical
tolerance from exact structural properties such as array shape, non-finite
positions, and—in tests where it matters—the sign of zero.

## TSMEFuDE definition

The historical MATLAB helper associated with TSMEFuDE discarded intermediate
time-shift phases because its phase container was reset inside the loop. The
Python implementation intentionally follows the published time-shift
multiscale definition instead: all phases at a scale are evaluated and their
entropy values are averaged.

## Detailed validation

The repository contains compact regression tests. Their scope and limitations
are described in [validation.md](validation.md).
