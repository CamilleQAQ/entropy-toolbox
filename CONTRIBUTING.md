# Contributing

Contributions are welcome through GitHub issues and pull requests.

## Code and provenance

Submit only code that you wrote or that you are authorized to contribute.
Do not copy code from papers, blogs, repositories, MATLAB File Exchange, or
other toolboxes unless its license is compatible and the source and license
are recorded explicitly. Implementing a published algorithm independently
from its mathematical description is welcome; cite the defining paper in
`docs/references.md`.

By submitting a contribution, you agree that your project-owned contribution
is distributed under the BSD 3-Clause License. Do not modify files marked
`SPDX-License-Identifier: CC-BY-4.0` without preserving their attribution,
license identifier, and change history.

## Development

Install the project and development dependencies with:

```bash
python -m pip install -e ".[dev]"
```

Run the public regression suite and smoke example before opening a pull
request:

```bash
python -m pytest tests/ -q
python examples/quickstart.py
```

Numerical changes should explain their expected effect and must not silently
change documented edge behavior. Numerical changes may require additional
regression evaluation by the project maintainer before acceptance.
