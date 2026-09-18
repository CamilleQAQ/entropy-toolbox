# Third-party notices

## MDE/RCMDE MATLAB code lineage

Four Python modules contain adaptations in the MDE/RCMDE MATLAB code lineage:

- `src/msentropy/core/mde.py`
- `src/msentropy/core/rcmde.py`
- `src/msentropy/core/dis_en_ncdf_cumulative.py`
- `src/msentropy/core/dis_en_ncdf_ms_cumulative.py`

Original work: Hamed Azami and Javier Escudero, *Matlab codes for Refined
Composite Multiscale Dispersion Entropy of Biomedical Signals*, University of
Edinburgh DataShare (2017), DOI 10.7488/ds/1982.

Source: https://datashare.ed.ac.uk/handle/10283/2637

License: Creative Commons Attribution 4.0 International (CC BY 4.0),
https://creativecommons.org/licenses/by/4.0/

The historical headers also credit Mostafa Rostaghi for the underlying
dispersion entropy method. This project translated the relevant MATLAB
behavior to Python, consolidated shared helpers, added explicit input and edge
handling, integrated the functions into the `msentropy` API, and added tests
and documentation. These are modified adaptations; the upstream authors do
not endorse this project.

The files listed above remain subject to CC BY 4.0. The repository's BSD
3-Clause License applies to project-owned files and does not replace the
license on those files.

## Historical numerical references

The toolbox was numerically compared with separately retained historical
reference implementations. Those files are not included in this public
distribution and no redistribution rights are claimed for them.

Runtime dependencies:

- NumPy
- SciPy

Each dependency is distributed under its own license.
