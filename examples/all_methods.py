"""Advanced example: run all 15 registered methods on one signal.

Run from the repository root:

    python examples/all_methods.py

The parameter sets make a reproducible API demonstration. They are not
universal recommendations for experimental work.
"""

import numpy as np

import msentropy

signal = np.random.default_rng(20260911).standard_normal(1024)

PARAMS = {
    "MPE": dict(m=3, tau=1, scale=5),
    "MSlopEn": dict(m=3, delta=0.1, gamma=1.0, scale=5),
    "MDE": dict(m=3, nc=6, tau=1, scale=5),
    "MFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "CMFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "RCMFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "MEFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "CMEFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "RCMEFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "RCMDE": dict(m=3, nc=6, tau=1, scale=5),
    "TSMPE": dict(m=3, tau=1, kmax=5),
    "TSMSlopEn": dict(m=3, delta=0.1, gamma=1.0, kmax=5),
    "TSMDE": dict(m=3, nc=6, tau=1, kmax=5),
    "TSMFuDE": dict(m=3, nc=6, tau=1, kmax=5),
    "TSMEFuDE": dict(m=3, nc=6, tau=1, kmax=5),
}

print(f"{'method':10s}  curve")
for name in msentropy.list_methods():
    curve = msentropy.compute(name, signal, **PARAMS[name])
    text = np.array2string(curve, precision=4, suppress_small=True)
    print(f"{name:10s}  {text}")
