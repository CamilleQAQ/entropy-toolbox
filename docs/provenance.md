# Code provenance

This document records the provenance decisions for the public Python
distribution. MATLAB validation material is not distributed.

## Project-owned implementations

Except for the files identified in the next section, the Python source was
written independently by CamilleQAQ from published papers, mathematical
descriptions and publicly available explanatory material. No source code was
copied from blogs or unrelated repositories. Those files are licensed under
the BSD 3-Clause License.

This category includes the Python framework and API, tests, documentation,
the independently written TSMEFuDE implementation, and the permutation,
slope, attention, sample, fuzzy and time-shift entropy families. Citations to
method papers acknowledge scientific provenance; they do not imply that the
paper authors wrote these Python files.

## CC BY 4.0 adaptations

The following files contain behavior-preserving Python adaptations in the
MDE/RCMDE lineage and are licensed under CC BY 4.0 rather than BSD-3-Clause:

- `src/msentropy/core/mde.py`
- `src/msentropy/core/rcmde.py`
- `src/msentropy/core/dis_en_ncdf_cumulative.py`
- `src/msentropy/core/dis_en_ncdf_ms_cumulative.py`

Upstream attribution:

- Hamed Azami and Javier Escudero, *Matlab codes for Refined Composite
  Multiscale Dispersion Entropy of Biomedical Signals*, University of
  Edinburgh DataShare, 2017, DOI: 10.7488/ds/1982.
- The historical source headers also credit Mostafa Rostaghi for the
  underlying dispersion entropy method and cite the corresponding papers.
- Upstream dataset: https://datashare.ed.ac.uk/handle/10283/2637
- Upstream license: https://creativecommons.org/licenses/by/4.0/

Changes made by this project include translation from MATLAB to Python,
integration into the `msentropy` API, explicit input handling, consolidation
of shared helpers, documentation, and compatibility behavior verified against
historical numerical reference outputs. The upstream authors do not endorse
this project.

## Reference material

MATLAB reference files were used for numerical comparison. They are excluded
from this repository and from source and wheel
distributions. A citation in the documentation is not a claim that the cited
author licensed unrelated code to this project.

## Project-owner declaration

The project owner, CamilleQAQ, states that the non-CC Python implementations
were written independently without copying third-party source code and that
the owner is authorized to publish them under BSD-3-Clause. The owner also
states that this repository contains no third-party datasets or figures, is
not subject to a known institutional release restriction, and is not
associated with a pending patent application.
