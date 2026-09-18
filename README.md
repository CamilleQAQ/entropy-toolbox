# Entropy Toolbox for Python

English | [简体中文](README.zh-CN.md)

`msentropy` computes single-scale and multiscale entropy features from
one-dimensional signals with NumPy and SciPy. It provides 15 related methods
behind one high-level interface, while keeping the validated numerical
implementations available for reproduction work.

## Installation

Python 3.10 or newer is required. Until the first PyPI release, install from a
local clone:

```bash
git clone https://github.com/CamilleQAQ/entropy-toolbox.git
cd entropy-toolbox
python -m pip install .
```

For development and testing, use an editable installation:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## First calculation

The example below produces one entropy value for each scale from 1 through 20:

```python
import numpy as np
import msentropy

# Replace this reproducible example with your own one-dimensional signal.
x = np.random.default_rng(0).standard_normal(2048)

curve = msentropy.compute(
    "MDE",
    x,
    m=3,       # embedding dimension
    nc=6,      # number of dispersion classes
    tau=1,     # delay in samples
    scale=20,  # evaluate scales 1, 2, ..., 20
)

print(curve)
print(curve[0])   # entropy at scale 1
print(curve[-1])  # entropy at scale 20
```

`m=3`, `nc=6`, and `tau=1` are useful starting values for an MDE example,
not universal settings. The appropriate parameters depend on the signal
length, sampling process, method, and research question.

Start with the [getting-started guide](docs/getting-started.md), then use the
[method selection table](docs/methods.md) and
[parameter guide](docs/parameters.md). Mathematical definitions, core steps,
parameter meanings, and output interpretation are collected in the
[algorithm guide](docs/algorithms/index.md). A runnable version of the basic
example is in [`examples/quickstart.py`](examples/quickstart.py); the
separate [`examples/all_methods.py`](examples/all_methods.py) runs all 15
methods.

## Choosing an interface

- `msentropy.compute(...)` is the high-level API intended for ordinary
  analysis. It normalizes vector orientation, checks common input mistakes,
  and accepts consistent keyword parameters.
- `msentropy.core.*` is the low-level compatibility API. It exposes the
  numerical implementations directly and retains documented MATLAB-compatible
  edge behavior required for scientific reproduction.

For new analysis code, prefer `msentropy.compute`.

The compatibility policy and the intentional TSMEFuDE definition correction
are summarized in [`docs/compatibility.md`](docs/compatibility.md).

Method names are case-insensitive. The available methods can be inspected
without running a calculation:

```python
for name in msentropy.list_methods():
    print(msentropy.get_method(name).signature)
```

## Interpreting results safely

- Keep the method, parameters, signal length, and preprocessing identical when
  comparing signals.
- A large maximum scale leaves fewer samples at the end of the curve. Do not
  select it independently of signal length.
- The high-level API rejects `NaN` and infinite samples. Clean or segment the
  signal deliberately instead of allowing missing data to pass silently.
- Entropy values from different method families or parameter settings are not
  automatically on the same numerical scale. Do not rank methods by comparing
  their raw values alone.
- The toolbox does not automatically filter, detrend, resample, or standardize
  a signal.

The reasoning and practical checks behind these rules are explained in
[`docs/parameters.md`](docs/parameters.md).

## Validation

The numerical implementations were validated against independently generated
reference outputs. The pre-publication validation suite contained 1,490
regression tests and 975 reference files; it passed in full before this clean
public distribution was created.

This repository keeps a compact API-level test suite instead of distributing
the full research validation materials. See
[`docs/validation.md`](docs/validation.md) for the scope and limitations of
that validation.

## Scientific references

Cite the papers relevant to the methods you use. The method-to-paper list is
maintained in [`docs/references.md`](docs/references.md). TSMEFuDE is described
in “Time Shift Multiscale Ensemble Fuzzy Dispersion Entropy and Its Application
in Bearing Fault Diagnosis”
([DOI 10.3390/coatings15070779](https://doi.org/10.3390/coatings15070779)).

Scientific citation and software licensing are separate: references recognize
method provenance, while [`docs/provenance.md`](docs/provenance.md) records
which files are project-owned and which are CC BY 4.0 adaptations.

## Project status

The toolbox is preparing for its first public release. The numerical API,
packaging metadata, automated test workflow, citation metadata, and licensing
provenance are in place. The repository has not yet published a tagged release.

## License

Project-owned Python code is licensed under the BSD 3-Clause License,
copyright 2025-2026 CamilleQAQ. Four MDE/RCMDE-lineage modules are modified
adaptations distributed under CC BY 4.0. See [`LICENSE`](LICENSE),
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md), and
[`docs/provenance.md`](docs/provenance.md) for file-level scope, attribution,
source links, and modification notices.
