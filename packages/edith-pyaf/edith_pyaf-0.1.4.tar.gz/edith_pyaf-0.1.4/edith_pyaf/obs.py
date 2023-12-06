#!/usr/bin/env python
############################################################################################
##### This module calculates various observables
############################################################################################

####################################
###########  IMPORTS   #############
####################################
from __future__ import division
from __future__ import print_function
import numpy as np

# Custom modules:
from . import utils
####################################


########################################################################
def scaled_IPR(Ham, state, **kwargs):
    """
    Compute the scaled inverse participation ratio.
    
    Parameters:
    -----------
    Ham, object of class Hamiltonian: the Hamiltonian and its properties.

    state, list or 1-dim: the state in the sector basis.


    Returns
    -------
    IPR


    References
    ----------
    https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.128.146601

    Notes
    -----
    state: |psi>
    filling: nu = N/L

    IPR = 1/(1-nu)*(1/N*sum_{i=1}^L |<psi| n_i |psi>|^2 - nu)

    Examples
    --------

    """

    N = Ham.pars["N"]
    sites = Ham.sites
    filling = N/sites

    IPR = 0
    # project state into each site to get particle number at each site:
    state_arr = utils.get_state_population_spinless(Ham, state, **kwargs)
    #print("state:", state)
    #print("state_arr:", state_arr)
    for i in range(sites):
        IPR += np.abs(state_arr[i])**2

    IPR = 1/(1-filling)*(IPR/N - filling)

    return IPR

########################################################################


########################################################################
def average_IPR(Ham, evecs, verbose, **kwargs):
    """
    Compute the average inverse participation ratio for all eigenstates.
    
    Parameters:
    -----------
    Ham, object of class Hamiltonian: the Hamiltonian and its properties.

    evecs, list or 1-dim: the eigenvectors of the Hamiltonian.


    Returns
    -------
    IPR


    References
    ----------
    https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.128.146601

    Notes
    -----
    state: |psi>
    filling: nu = N/L
    
    IPR = 1/(1-nu)*(1/N*sum_{i=1}^L |<psi| n_i |psi>|^2 - nu)

    Examples
    --------

    """

    print("Calculating IPR...")

    dim = Ham.sector_dim
    #print("dim", dim)
    IPR_avg = 0
    for state in evecs:
        IPR = scaled_IPR(Ham, state, **kwargs)
        #print("IPR", IPR)
        IPR_avg += IPR
    #print(IPR_avg)
    IPR_avg /= dim
    
    if verbose:
        print("IPR average:", IPR_avg)
    return IPR_avg

########################################################################