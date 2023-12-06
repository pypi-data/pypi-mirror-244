#!/usr/bin/env python
############################################################################################
##### This file calculates the eigenvalues of a given matrix (Hamiltonian).
############################################################################################

####################################
###########  IMPORTS   #############
####################################
from __future__ import division
from __future__ import print_function
import scipy as sp
import numpy as np

# Custom modules:
from . import input as inp
####################################


########################################################################
def diagonalize(Ham,
                input, 
                **kwargs):
    """
    Compute the eigenvalues and eigenvectors of the given Hamiltonian.
    
    Parameters:
    -----------
    Ham, instance of Hamiltonian class: the (possibly sparse) Hamiltonian.
    input, instance of Input class: the input information.

    **kwargs:
    - n_evals, int: the number of lowest eigenvalues to be computed.


    Returns
    -------
    evals, list of floats: the n_evals smallest eigenvalues.


    References
    ----------

    Notes
    -----

    Examples
    --------

    """

    n_evals = input.n_lowest_eigenvalues

    # Hamiltonian is saved as sparse matrix:
    if Ham.sparse == True:

        # Assemble sparse matrix from class data:
        H = sp.sparse.csr_matrix((Ham.mat_els, (Ham.rows, Ham.cols)))

        if n_evals==None or n_evals == np.amax([Ham.cols,Ham.rows])+1:
            # Calculate all eigenvalues:
            if input.compute_evecs==True:
                evals, evecs = sp.linalg.eigh(H.todense(),
                                       eigvals_only=False)
                return evals, evecs
            else:
                evals = sp.linalg.eigh(H.todense(),
                                       eigvals_only=True)
                return evals, None

        elif n_evals <= np.amax([Ham.cols,Ham.rows]):    # This assumes the rows and columns contain the bottom right corner of the matrix
            # Calculate only lowest eigenvalues:
            if input.compute_evecs==True:
                evals, evecs = sp.sparse.linalg.eigsh(H, 
                                                      k=n_evals, 
                                                      which='SA', 
                                                      return_eigenvectors=True, 
                                                      maxiter=input.maxiter_Arnoldi)
                return evals, evecs

            else:
                evals = sp.sparse.linalg.eigsh(H,
                                               k=n_evals,
                                               which='SA', 
                                               return_eigenvectors=False,
                                               maxiter=input.maxiter_Arnoldi)
                return evals, None

    # Hamiltonian is full matrix
    else:
        if n_evals==None:
            evals = sp.linalg.eigh(Ham.arr, eigvals_only=True)
            return evals, None
        else:
            subset = [0,n_evals-1]

            if input.compute_evecs==True:
                evals, evecs = sp.sparse.linalg.eigsh(H, 
                                                      k=n_evals, 
                                                      which='SA', 
                                                      return_eigenvectors=False, 
                                                      maxiter=input.maxiter_Arnoldi)
                return evals, evecs
            
            else:
                evals = sp.linalg.eigh(Ham.arr, 
                                       eigvals_only=True, 
                                       subset_by_index=subset)
                return evals, None

########################################################################


