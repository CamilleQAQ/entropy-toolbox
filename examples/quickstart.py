"""Minimal runnable example for the msentropy high-level API.

Run from the repository root:

    python examples/quickstart.py

See ``docs/getting-started.md`` for an explanation and
``examples/all_methods.py`` for a sweep over all registered methods.
"""

import numpy as np

import msentropy

# A reproducible synthetic signal standing in for one preprocessed segment.
n_samples = 2048
time = np.arange(n_samples)
rng = np.random.default_rng(20260911)
signal = rng.standard_normal(n_samples)
signal += 0.5 * np.sin(2 * np.pi * 40 * time / n_samples)

# MDE returns one value for every scale from 1 through ``scale``.
curve = msentropy.compute(
    "MDE",
    signal,
    m=3,
    nc=6,
    tau=1,
    scale=20,
)

scales = np.arange(1, curve.size + 1)
print(f"signal length: {signal.size} samples")
print("scale  MDE")
for scale, value in zip(scales, curve, strict=True):
    print(f"{scale:5d}  {value:.6f}")
