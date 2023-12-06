#!/usr/bin/env python
############################################################################################
##### This file calculates the time evolution of various quantities.
############################################################################################

####################################
###########  IMPORTS   #############
####################################
from __future__ import division
from __future__ import print_function
import numpy as np

# Custom modules:
from . import input as inp
from . import utils
####################################


########################################################################
def time_evolve(Ham, evals, evecs, initial_state, t, **kwargs):
    """
    Compute the many-body state at time t.
    
    Parameters:
    -----------
    Ham, object of class Hamiltonian: the Hamiltonian and its properties.

    evals, list or 1-dim: the eigenvalues of the Hamiltonian.

    evecs, list or 1-dim: the eigenvectors of the Hamiltonian.

    initial_state, list or 1-dim array: the initial state for the propagation.

    t, float: the time after the quench.



    Returns
    -------
    final_state, numpy array: the many-body state at time t as a vector.


    References
    ----------

    Notes
    -----
    |\psi(t)> = \sum_{n} exp(-i*eps_n*t/hbar) <n|\psi(0)> |n>

    where eps_n is the n-th eigenenergy and |n> is the n-th eigenstate of the Hamiltonian.

    * The time evolution starts at t=0 by default.

    Examples
    --------

    """
    

    # Convert initial state to a vector in the Hilbert subspace of the sector:
    # e.g. |1011> -> (0,0,1,0)
    # because the (lexicographically ordered) basis is:
    # B = [ |1110>, |1101>, |1011>, |0111> ]
    initial_state_vec = utils.convert_state_from_bin_to_vec(state_str=initial_state,
                                                            basis_dim=Ham.sector_dim, 
                                                            sector=Ham.sector)

    final_state = np.zeros(len(Ham.basis_states), dtype=np.complex_)
    
    #print("time:", t)
    for n in range(Ham.sector_dim):
        #print("n:", n)
        npsi0 = utils.calculate_overlap(evecs[:,n], initial_state_vec)
        #print("npsi0:", npsi0)
        #print("Eigenvector:", evecs[:,n])
        #print("Eigenenergy:", evals[n])
        #print("Exponential part:", np.exp(-1j*evals[n]*t))

        final_state += np.exp(-1j*evals[n]*t)*npsi0*evecs[:,n]

    # Normalization:
    final_state /= np.sqrt(np.vdot(final_state,final_state))

    return final_state

########################################################################

########################################################################
def full_time_evolution(Ham, evals, evecs, initial_state, final_time, dt):
    """
    Compute the eigenvalues and eigenvectors of the given Hamiltonian.
    
    Parameters:
    -----------
    Ham, object of class Hamiltonian: the Hamiltonian and its properties.

    evals, list or 1-dim: the eigenvalues of the Hamiltonian.

    evecs, list or 1-dim: the eigenvectors of the Hamiltonian.

    initial_state, list or 1-dim array: the initial state for the propagation.

    final_time, float: the final time in the propagation.

    dt, float: step size of the time evolution.


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

    time_evolved_state = []
    initial_state_vec = utils.convert_state_from_bin_to_vec(state_str=initial_state,
                                                            basis_dim=Ham.sector_dim,
                                                            sector=Ham.sector)
    time_evolved_state.append(initial_state_vec)

    #print("time:", 0)
    #print("initial state:", initial_state_vec)
    for t in np.arange(dt,final_time,dt):
        time_evolved_state.append(time_evolve(Ham=Ham,
                                              evals=evals, 
                                              evecs=evecs, 
                                              initial_state=initial_state, 
                                              t=t)
                                )
        if np.floor(t)%10==1:
            print(f"Time {t} calculated.")
    #print(time_evolved_state)

    return np.array(time_evolved_state)

########################################################################


########################################################################
def dipolar_Aubry_Andre_dynamics_check(Delta, beta, phi, hopp, final_time, dt):


    a = Delta*np.cos(2*np.pi*beta + phi)
    b = hopp
    c = Delta*np.cos(4*np.pi*beta + phi)
    d = np.sqrt(a**2 - 2*a*c + 4*b**2 + c**2)

    #print("a:", a)
    #print("b:", b)
    #print("c:", c)
    #print("d:", d)

    time_evolved_state = []
    for t in np.arange(0.0, final_time, dt):
        state = np.zeros(2, dtype=np.complex_)
            
        if inp.initial_state=="01":
            state[0] = np.exp(-1j*t/2*(-d+a+c))*((-d+a-c)/(2*b))**2/(((-d+a-c)/(2*b))**2+1) + np.exp(-1j*t/2*(d+a+c))*((d+a-c)/(2*b))**2/(((d+a-c)/(2*b))**2+1)
            state[1] = np.exp(-1j*t/2*(-d+a+c))*((-d+a-c)/(2*b))/(((-d+a-c)/(2*b))**2+1) + np.exp(-1j*t/2*(d+a+c))*((d+a-c)/(2*b))/(((d+a-c)/(2*b))**2+1)

        elif inp.initial_state=="10":
            state[0] = np.exp(-1j*t/2*(-d+a+c))*(-d+a-c)/(2*b)/(((-d+a-c)/(2*b))**2+1) + np.exp(-1j*t/2*(d+a+c))*(d+a-c)/(2*b)/(((d+a-c)/(2*b))**2+1)
            state[1] = np.exp(-1j*t/2*(-d+a+c))/(((-d+a-c)/(2*b))**2+1) + np.exp(-1j*t/2*(d+a+c))/(((d+a-c)/(2*b))**2+1)

        time_evolved_state.append(state)

    return np.array(time_evolved_state)

########################################################################


########################################################################
def dipolar_Aubry_Andre_dynamics_check2(final_time, dt):


    energies=np.array([-2.3074509,  -0.94707149,  0.32274683,  1.15565479])
    eigenstates=np.array([[-0.37440638,  0.70811631, -0.5585074,   0.21554729], [0.57556858, -0.30558355, -0.58868453,  0.47832], [0.68406366,  0.50545031, -0.02053916, -0.52550455], [0.24616575, 0.38692372, 0.58403608, 0.66977183]])

    time_evolved_state = []
    for t in np.arange(0.0, final_time, dt):
        state = np.zeros(4, dtype=np.complex_)  

        if inp.initial_state=="0001":            
            state += np.exp(-1j*t*energies[0])*np.vdot(eigenstates[0],[1,0,0,0])*eigenstates[0]
            state += np.exp(-1j*t*energies[1])*np.vdot(eigenstates[1],[1,0,0,0])*eigenstates[1]
            state += np.exp(-1j*t*energies[2])*np.vdot(eigenstates[2],[1,0,0,0])*eigenstates[2]
            state += np.exp(-1j*t*energies[3])*np.vdot(eigenstates[3],[1,0,0,0])*eigenstates[3]

        if inp.initial_state=="0010":            
            state += np.exp(-1j*t*energies[0])*np.vdot(eigenstates[0],[0,1,0,0])*eigenstates[0]
            state += np.exp(-1j*t*energies[1])*np.vdot(eigenstates[1],[0,1,0,0])*eigenstates[1]
            state += np.exp(-1j*t*energies[2])*np.vdot(eigenstates[2],[0,1,0,0])*eigenstates[2]
            state += np.exp(-1j*t*energies[3])*np.vdot(eigenstates[3],[0,1,0,0])*eigenstates[3]

        if inp.initial_state=="0100":            
            state += np.exp(-1j*t*energies[0])*np.vdot(eigenstates[0],[0,0,1,0])*eigenstates[0]
            state += np.exp(-1j*t*energies[1])*np.vdot(eigenstates[1],[0,0,1,0])*eigenstates[1]
            state += np.exp(-1j*t*energies[2])*np.vdot(eigenstates[2],[0,0,1,0])*eigenstates[2]
            state += np.exp(-1j*t*energies[3])*np.vdot(eigenstates[3],[0,0,1,0])*eigenstates[3]

        if inp.initial_state=="1000":            
            state += np.exp(-1j*t*energies[0])*np.vdot(eigenstates[0],[0,0,0,1])*eigenstates[0]
            state += np.exp(-1j*t*energies[1])*np.vdot(eigenstates[1],[0,0,0,1])*eigenstates[1]
            state += np.exp(-1j*t*energies[2])*np.vdot(eigenstates[2],[0,0,0,1])*eigenstates[2]
            state += np.exp(-1j*t*energies[3])*np.vdot(eigenstates[3],[0,0,0,1])*eigenstates[3]

        time_evolved_state.append(state)


    return np.array(time_evolved_state)

########################################################################

