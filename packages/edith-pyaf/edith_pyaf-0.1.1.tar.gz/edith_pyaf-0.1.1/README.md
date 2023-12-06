# EDITH

## Description

EDITH (PYAF) stands for Exact Diagonalization of Interacting Time-dependent Hamiltonians (in PYthon And Fortran). For now it is a collection of python modules used to calculate the spectral and dynamical properties of  many-body Hamiltonians describing quantum systems on a lattice. One long-term goal is to rewrite the core diagonalization routines in Fortran to make them faster and lighter. Currently, EDITH supports the exact diagonalization of the following models:
- Ising model in a transverse field
- Heisenberg model in a staggered field
- Hubbard model
- Dipolar Aubry-Andre model


## Installation
Currently EDITH is just a collection of python modules that can be downloaded and executed directly.

## Usage
To use EDITH, configure the input file (input.dat) with the parameters of your system. Then run

python3 main.py input.dat

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
