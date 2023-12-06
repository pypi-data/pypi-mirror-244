# EDITH

## Description

EDITH (PYAF) stands for Exact Diagonalization of Interacting Time-dependent Hamiltonians (in PYthon And Fortran). For now it is a collection of python modules used to calculate the spectral and dynamical properties of  many-body Hamiltonians describing quantum systems on a lattice. One long-term goal is to rewrite the core diagonalization routines in Fortran to make them faster and lighter. Currently, EDITH supports the exact diagonalization of the following models:
- Ising model in a transverse field
- Heisenberg model in a staggered field
- Hubbard model
- Dipolar Aubry-Andre model


## Installation
Currently EDITH can be downloaded from PyPI via pip, e.g. with

python3 -m pip install edith-pyaf

Alternatively, you can download the source from the repository (it is just a collection of python modules). The module can then be executed directly.

## Usage
To use EDITH after installation:
1) Copy the template input file:
python3 edith_pyaf.initialize.py
2) Configure the input file (input.dat) with the parameters of your system.
3) Execute EDITH:
python3 edith_pyaf.run.py

## Support
For support, please contact moligninip@gmail.com.

## Roadmap
Short term goals:
- Python packaging.
- Simple GUI.

Medium term goals:
- Extending code to non-Hermitian systems.
- Extending diagonalization to Liouvillians (open quantum systems).
- Extending code to time-dependent Hamiltonians.

Long term goals:
- Rewriting core in Fortran.
- Enabling execution on HPC facilities with MPI.

## Contributing
If you would like to contribute to this project, please let me know!

## Authors and acknowledgment
Paolo Molignini (University of Stockholm)

## License
GPLv3 license.

## Project status
Ongoing
