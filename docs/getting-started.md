# Getting started

English | [简体中文](zh-CN/getting-started.md)

This guide uses the high-level `msentropy.compute` interface. It is the
recommended entry point for ordinary analysis because it accepts a
one-dimensional signal, checks common input mistakes, and always returns a
one-dimensional NumPy array.

## 1. Install the package

From a local clone of the repository:

```bash
python -m pip install .
```

Use `python -m pip install -e ".[dev]"` instead if you are developing the
toolbox or running its tests.

## 2. Prepare one signal

```python
import numpy as np

x = np.random.default_rng(0).standard_normal(2048)
```

`x` may be a Python sequence or a NumPy array. A flat array, a single row, and
a single column are accepted. A matrix containing several channels is not:
select or loop over its channels explicitly.

Before calculating entropy, decide how missing samples, detrending, filtering,
resampling, and normalization should be handled for the experiment. The
toolbox does not make those scientific choices automatically.

## 3. Calculate a curve

MDE is a compact first example:

```python
import msentropy

curve = msentropy.compute(
    "MDE",
    x,
    m=3,
    nc=6,
    tau=1,
    scale=20,
)
```

`curve` has 20 elements. `curve[0]` is scale 1, `curve[1]` is scale 2, and
`curve[-1]` is scale 20. Scales use one-based scientific notation even though
Python array indexes start at zero.

These values are a starting example, not automatic best parameters. Read
[Parameters and data preparation](parameters.md) before choosing settings for
an experiment.

## 4. Plot the result

```python
import matplotlib.pyplot as plt

scales = np.arange(1, curve.size + 1)
plt.plot(scales, curve, marker="o")
plt.xlabel("Scale")
plt.ylabel("MDE")
plt.show()
```

Matplotlib is not a runtime dependency of the toolbox; install it separately
if a plot is needed.

## 5. Choose another method

The toolbox registers 20 multiscale methods:

```python
print(msentropy.list_methods())
```

Inspect the accepted parameters for one method:

```python
print(msentropy.get_method("TSMEFuDE").signature)
```

Use the [method selection table](methods.md) to understand the families before
changing methods. If an experiment compares methods, keep the signal segments
and preprocessing identical and report the parameters of every method.

For the mathematical definition and calculation steps, continue with the
[algorithm guide](algorithms/index.md).

## High-level and compatibility APIs

Use `msentropy.compute(...)` for normal analysis. It provides consistent
keyword arguments, input normalization, and readable validation errors.

Use `msentropy.core.*` only when direct access to an implementation or exact
MATLAB-compatible edge behavior is required. The compatibility functions may
accept degenerate inputs that the high-level API rejects.

## Next examples

- [`examples/quickstart.py`](../examples/quickstart.py) is the runnable version
  of the basic MDE example.
- [`examples/all_methods.py`](../examples/all_methods.py) demonstrates all 20
  registered methods with one reproducible signal.
- [Parameters and data preparation](parameters.md) explains signal length,
  preprocessing, non-finite values, and valid comparisons.
