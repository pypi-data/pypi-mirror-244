#!/usr/bin/env python
############################################################################################
##### This module implements symmetry transformations.
############################################################################################

####################################
###########  IMPORTS   #############
####################################
import numpy as np
from scipy.integrate import quad, dblquad
import matplotlib.pyplot as plt
####################################




################################################################################################################################################
def map_continuum_to_lattice(potential_type, 
                             potential_pars, 
                             interaction_type,
                             int_pars, 
                             Wannier_type, 
                             order, 
                             sites):
    """
    
    Parameters:
    ----------
    potential_type, str: name for the chosen one-body potential.
                        Options:
                        - "sine":                       V(x) = V0*sin(k0*x)
                        - "sine-squared":               V(x) = V0*sin^2(k0*x)
                        - "quasicrystal":               V(x) = 0.5*Vp*cos(2*kp*x) +  0.5*Vd*cos(2*kd*x + phi)

    potential_pars, dict: parameters describing the potential.

    interaction_type, str: name for the chosen one-body potential.
                        Options:
                        - "regularized-dipolar":        W(x,x') = W0/(|x-x'|^3 + alpha)
                        - "delta":                      W(x,x') = W0*delta(x-x')

    int_pars, dict: parameters describing the interaction.


    Wannier_type, str: name for the chosen Wannier-function approximation.
                        Options:
                        - "gaussian": approximation as Gaussian (ground-state of QHO).
                        - "max-localized":

                        
    order, int: how many neighboring sites to take into account in the overlap integrals.
                        Options:
                        - 1:    nearest-neighbor only.
                        - 2:    next-nearest neighbor contributions.

    sites, int: the number of lattice sites.

    Notes:
    ------
    Standard integration boundaries for hopping: 3 lattice spacings away from mid-point on each site, i.e.:
    xmin= xj + a/2 - 3a, xmax = xj + a/2 + 3a, so if xj=-a/2, x_{j+1} = a/2:
    xmin = -3a, xmax = 3a

    """
    lattice_pars = {}

    if potential_type=="quasicrystal":
        Vp = potential_pars["Vp"]
        Vd = potential_pars["Vd"]
        kp = potential_pars["kp"]
        kd = potential_pars["kd"]
        phi = potential_pars["phi"]

        # Harmonic approx of 0.5*Vp*cos(2*kp*x - pi) is V(x) ~ 0.5*Vp*(2*kp^2*x^2 - 1)
        # The phase -pi is needed to shift the function to be centered around the origin.
        kappa = 2*Vp*kp**2
        a = np.pi/kp    # lattice spacing
        m = 1.0
        
        ###########################################################################
        # Get tunneling integrals:
        # - tp: nn tunneling (site-independent)
        # - td_j: tunneling induced by detuning potential (site-dependent!)
        ###########################################################################
        if order > 0:
            
            if Wannier_type=="gaussian":
                # This is site independent, so we just take xj=-pi/2kp and x_{j+1} = +pi/2kp.
                # Thus following rule above (see Notes) xmin=-3a=-3pi/kp, xmax=3a=3pi/kp
                tp1, _ = quad(lambda x: np.conj(qho_gs(kappa=kappa,m=m,x=x-a/2))*(-1/(2*m)*qho_gs_d2(kappa=kappa,m=m,x=x+a/2) + Vp/2*np.cos(2*kp*x)*qho_gs(kappa=kappa,m=m,x=x+a)), -3*a, 3*a)
                
                
                # This is site dependent! We need to iterate over different positions for xmin, xmax:
                td1_list = []
                for s in range(sites-1):
                    # Define positions of both Wannier functions and integration bounds for each site:
                    xj = (1-sites)/2*a + s*a
                    xjplus1 = (1-sites)/2*a + (s+1)*a
                    xmin = xj + a/2 - 3*a 
                    xmax = xj + a/2 + 3*a
                    # Calculate overlap:
                    td1, _ = quad(lambda x: np.conj(qho_gs(kappa=kappa,m=m,x=x-xj))*(Vd/2*np.cos(2*kd*x+phi)*qho_gs(kappa=kappa,m=m,x=x-xjplus1)), xmin, xmax)
                    td1_list.append(td1)

            lattice_pars["tp1"] = tp1
            lattice_pars["td1"] = td1_list

        if order > 1:
            if Wannier_type=="gaussian":
                # nnn hopping (homogeneous part):
                tp2, _ = quad(lambda x: np.conj(qho_gs(kappa=kappa,m=m,x=x-a/2))*(-1/(2*m)*qho_gs_d2(kappa=kappa,m=m,x=x+3*a/2) + Vp/2*np.cos(2*kp*x)*qho_gs(kappa=kappa,m=m,x=x+a)), -3*a, 3*a)
                
                # nnn hopping (detuning part)
                td2_list = []
                for s in range(sites-2):
                    # Define positions of both Wannier functions and integration bounds for each site:
                    xj = (1-sites)/2*a + s*a
                    xjplus2 = (1-sites)/2*a + (s+2)*a
                    xmin = xj + a/2 - 3*a 
                    xmax = xj + a/2 + 3*a
                    # Calculate overlap:
                    td2 = quad(lambda x: np.conj(qho_gs(kappa=kappa,m=m,x=x-xj))*(Vd/2*np.cos(2*kd*x+phi)*qho_gs(kappa=kappa,m=m,x=x-xjplus2)), xmin, xmax)
                    td2_list.append(td2)
        
            lattice_pars["tp2"] = tp2
            lattice_pars["td2"] = td2_list

        if order > 2:
            print("Third order hopping and higher not implemented!")
            # raise NotImplemented()
            
        ###########################################################################

        ###########################################################################
        # Get chemical potentials:
        ###########################################################################

        lattice_pars["beta"] = kd/kp

        if Wannier_type=="gaussian":
            Delta, _ = quad(lambda x: np.abs(qho_gs(kappa=kappa,m=m,x=x))**2*Vd/2*np.cos(2*kd*x), -3*a, 3*a)

        lattice_pars["Delta"] = Delta

        ########################################################################### 


        ###########################################################################
        # Get interactions:
        ###########################################################################

        if interaction_type=="regularized-dipolar":
            W = int_pars["W"]
            alpha = int_pars["alpha"]

        if order > 0:
                
            if Wannier_type=="gaussian":
                W01,_ = dblquad(lambda x, xp: regularized_dipolar(W=W, alpha=alpha, x=x, xp=xp)
                                  *(np.abs(qho_gs(kappa=kappa,m=m,x=x))**2
                                    *np.abs(qho_gs(kappa=kappa,m=m,x=xp-a))**2 
                                    - np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-a))*
                                    qho_gs(kappa=kappa,m=m,x=xp)*
                                    qho_gs(kappa=kappa,m=m,x=x-a)
                                    ), -3*a, 3*a, -3*a, 3*a)

            lattice_pars["W01"] = W01

        if order > 1:
            
            if Wannier_type=="gaussian":
                W02,_ = dblquad(lambda x, xp: regularized_dipolar(W=W, alpha=alpha, x=x, xp=xp)
                                  *(np.abs(qho_gs(kappa=kappa,m=m,x=x))**2
                                    *np.abs(qho_gs(kappa=kappa,m=m,x=xp-2*a))**2 
                                    - np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-2*a))*
                                    qho_gs(kappa=kappa,m=m,x=xp)*
                                    qho_gs(kappa=kappa,m=m,x=x-2*a)
                                    ), -4*a, 4*a, -4*a, 4*a)
                
                W012,_ = dblquad(lambda x, xp: regularized_dipolar(W=W, alpha=alpha, x=x, xp=xp)
                                  *(np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-a))*
                                    qho_gs(kappa=kappa,m=m,x=xp-2*a)*
                                    qho_gs(kappa=kappa,m=m,x=x)
                                    - np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-a))*
                                    qho_gs(kappa=kappa,m=m,x=xp)*
                                    qho_gs(kappa=kappa,m=m,x=x-2*a)
                                    ), -4*a, 4*a, -4*a, 4*a)

                W102,_ = dblquad(lambda x, xp: regularized_dipolar(W=W, alpha=alpha, x=x, xp=xp)
                                  *(np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-a))*
                                    qho_gs(kappa=kappa,m=m,x=xp-a)*
                                    qho_gs(kappa=kappa,m=m,x=x-2*a)
                                    - np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-a))*
                                    qho_gs(kappa=kappa,m=m,x=xp-2*a)*
                                    qho_gs(kappa=kappa,m=m,x=x-a)
                                    ), -4*a, 4*a, -4*a, 4*a)

                W201,_ = dblquad(lambda x, xp: regularized_dipolar(W=W, alpha=alpha, x=x, xp=xp)
                                  *(np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-2*a))*
                                    qho_gs(kappa=kappa,m=m,x=xp-2*a)*
                                    qho_gs(kappa=kappa,m=m,x=x-a)
                                    - np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-2*a))*
                                    qho_gs(kappa=kappa,m=m,x=xp-a)*
                                    qho_gs(kappa=kappa,m=m,x=x-2*a)
                                    ), -4*a, 4*a, -4*a, 4*a)

                lattice_pars["W02"] = W02
                lattice_pars["W012"] = W012
                lattice_pars["W102"] = W102
                lattice_pars["W201"] = W201                    


        if order > 2:
                            
            W03,_ = dblquad(lambda x, xp: regularized_dipolar(W=W, alpha=alpha, x=x, xp=xp)
                                  *(np.abs(qho_gs(kappa=kappa,m=m,x=x))**2
                                    *np.abs(qho_gs(kappa=kappa,m=m,x=xp-3*a))**2 
                                    - np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-3*a))*
                                    qho_gs(kappa=kappa,m=m,x=xp)*
                                    qho_gs(kappa=kappa,m=m,x=x-3*a)
                                    ), -5*a, 5*a, -5*a, 5*a)

            lattice_pars["W03"] = W03

        if order > 3:
                            
            W04,_ = dblquad(lambda x, xp: regularized_dipolar(W=W, alpha=alpha, x=x, xp=xp)
                                  *(np.abs(qho_gs(kappa=kappa,m=m,x=x))**2
                                    *np.abs(qho_gs(kappa=kappa,m=m,x=xp-4*a))**2 
                                    - np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-4*a))*
                                    qho_gs(kappa=kappa,m=m,x=xp)*
                                    qho_gs(kappa=kappa,m=m,x=x-4*a)
                                    ), -6*a, 6*a, -6*a, 6*a)

            lattice_pars["W04"] = W04


        if order > 4:
                            
            W05,_ = dblquad(lambda x, xp: regularized_dipolar(W=W, alpha=alpha, x=x, xp=xp)
                                  *(np.abs(qho_gs(kappa=kappa,m=m,x=x))**2
                                    *np.abs(qho_gs(kappa=kappa,m=m,x=xp-5*a))**2 
                                    - np.conj(qho_gs(kappa=kappa,m=m,x=x))*
                                    np.conj(qho_gs(kappa=kappa,m=m,x=xp-5*a))*
                                    qho_gs(kappa=kappa,m=m,x=xp)*
                                    qho_gs(kappa=kappa,m=m,x=x-5*a)
                                    ), -7*a, 7*a, -7*a, 7*a)

            lattice_pars["W05"] = W05        
            
        ###########################################################################


    # plot_qho_gs(kappa=kappa,
    #             m=m, 
    #             a=a, 
    #             sites=sites, 
    #             s=0, 
    #             Nx=1001)

    for d in range(1,order):
        plot_qho_gs_2d_overlap(W=W, 
                            alpha=alpha, 
                            kappa=kappa, 
                            m=m, 
                            a=a, 
                            sites=sites,  
                            d=d, 
                            Nx=501,
                            vmax=None)

    return lattice_pars
################################################################################################################################################




###############################
###############################
#####  WANNIER FUNCTIONS  #####
###############################
###############################



################################################################################################################################################
def qho_gs(kappa, m, x):
    """
    
    Parameters:
    -----------
    kappa, float: spring constant, related to harmonic frequency omega (see notes).

    m, float: particle mass.

    x, float: position.

    Notes:
    ------
    This is the ground-state wave function of the following Hamiltonian:

    H = p^2/2m + 1/2*kappa*x^2 = p^2/2m + 1/2*m*omega^2*x^2

    with omega=sqrt(k/m) and p=-1j*d/dx (hbar=1).

    """

    return (np.sqrt(m*kappa)/np.pi)**0.25*np.exp(-np.sqrt(m*kappa)*x**2/2)
################################################################################################################################################

################################################################################################################################################
def qho_gs_d2(kappa, m, x):
    """
    
    Parameters:
    -----------
    kappa, float: spring constant, related to harmonic frequency omega (see notes).

    m, float: particle mass.

    x, float: position.

    Notes:
    ------
    This is the second derivative of the ground-state wave function of the following Hamiltonian:

    H = p^2/2m + 1/2*kappa*x^2 = p^2/2m + 1/2*m*omega^2*x^2

    with omega=sqrt(k/m) and p=-1j*d/dx (hbar=1).

    """

    return (m*kappa)**(0.625)/(np.pi)**(0.25)*np.exp(-np.sqrt(m*kappa)*x**2/2)*(np.sqrt(m*kappa)*x**2 - 1)
################################################################################################################################################


###################################
###################################
#####  INTERACTION FUNCTIONS  #####
###################################
###################################

################################################################################################################################################
def regularized_dipolar(W, alpha, x, xp):
    """
    
    Parameters:
    -----------
    W, float: strength of the interaction.

    alpha, float: strength of the regularization.

    x, float: position x.

    xp, float: position x'.

    Notes:
    ------
    W(x,x') = W0/(|x-x'|^3 + alpha)

    """

    return W/(np.abs(x-xp)**3 + alpha)
################################################################################################################################################

################################################################################################################################################
def delta(W, x, xp, thresh):
    """
    
    Parameters:
    -----------
    W, float: strength of the interaction.

    x, float: position x.

    xp, float: position x'.

    thresh, float: the threshold to evaluate the delta function peak.

    Notes:
    ------
    W(x,x') = W*delta(x,x')

    """

    if np.abs(x-xp) < thresh:
        return W/thresh
    else:
        return 0.0
################################################################################################################################################
    




###################################
###################################
#####        PLOTTERS         #####
###################################
###################################
################################################################################################################################################
def plot_qho_gs(kappa, m, a, sites, s, Nx):

    x_arr = np.linspace((1-sites)/2.0*a-a/2, (sites-1)/2.0*a+a/2, Nx)

    xj = (1-sites)/2*a + s*a
    xjplus1 = (1-sites)/2*a + (s+1)*a
    xmin = xj + a/2 - 3*a 
    xmax = xj + a/2 + 3*a

    func_arr1 = []
    func_arr2 = []
    for x in x_arr:
        func_arr1.append(qho_gs(kappa, m, x - xj))
        func_arr2.append(qho_gs(kappa, m, x - xjplus1))
    func_arr1=np.array(func_arr1)
    func_arr2=np.array(func_arr2)

    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    plot = ax.plot(x_arr, func_arr1, lw=3, label=f"Wannier function at site s={s+1}, x={xj}")
    plot = ax.plot(x_arr, func_arr2, lw=3, label=f"Wannier function at site s={s+2}, x={xjplus1}")
    for s in range(sites):
        ax.vlines(x=(1-sites)/2*a + s*a, ymin=0.0, ymax=2.0, linestyle="dashed", lw=2, color="black")
    ax.vlines(x=xmin, ymin=0.0, ymax=2.0, linestyle="solid", color="red", lw=3,  label="integration boundaries")
    ax.vlines(x=xmax, ymin=0.0, ymax=2.0, linestyle="solid", color="red", lw=3)
    ax.fill_between(x_arr, np.minimum(func_arr1, func_arr2), 0, color="green", alpha=0.5)

    ax.set_xlabel("position [a]")
    ax.set_ylabel("Wannier function")
    plt.legend(prop={'size': 15})
    plt.show()
    plt.close()

    return

################################################################################################################################################


################################################################################################################################################
def plot_qho_gs_2d_overlap(W, alpha, kappa, m, a, sites, d, Nx, vmax):
    """
    Parameters:
    ----------
    W, float: DDI strength.
    alpha, float: DDI regularization parameter.
    kappa, float: spring constant for QHO wavefunction.
    m, float: mass for QHO wavefunction.
    a, float: lattice constant.
    sites, int: number of lattice sites.
    d, int: distance in sites between wavefunctions.
    Nx, int: number of points in the discretized spatial interval.
    max, float: maximal value in the colorbar.
    
    """

    x_arr = np.linspace((1-sites)/2.0*a-a/2, (sites-1)/2.0*a+a/2, Nx)
    xp_arr = x_arr

    overlap = np.zeros(shape=(len(x_arr), len(xp_arr)))
    for idx_x, x in enumerate(x_arr):
        for idx_xp, xp in enumerate(xp_arr):
            overlap[idx_x,idx_xp] = regularized_dipolar(W=W, alpha=alpha, x=x, xp=xp)*(np.abs(qho_gs(kappa=kappa,m=m,x=x))**2*
                                                                               np.abs(qho_gs(kappa=kappa,m=m,x=xp-d*a))**2
                                                                               - np.conj(qho_gs(kappa=kappa,m=m,x=x))*np.conj(qho_gs(kappa=kappa,m=m,x=xp-d*a))
                                                                               *qho_gs(kappa=kappa,m=m,x=xp)*qho_gs(kappa=kappa,m=m,x=x-d*a))


    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    X, Y = np.meshgrid(x_arr, xp_arr)
    if vmax==None:
        vmax = np.amax(overlap)
    plot = ax.pcolormesh(X, Y, overlap.T, cmap="inferno", vmax=vmax)
    plt.colorbar(plot)
    for s in range(sites):
        ax.vlines(x=(1-sites)/2*a + s*a, ymin=-sites*a/2, ymax=sites*a/2, linestyle="dashed", lw=1, color="white")
        ax.hlines(y=(1-sites)/2*a + s*a, xmin=-sites*a/2, xmax=sites*a/2, linestyle="dashed", lw=1, color="white")

    ax.set_xlim([-2*a, 2*a])
    ax.set_ylim([d*a-2*a, d*a+2*a])
    ax.set_xlabel("position x [a]")
    ax.set_ylabel(r"position $x^{\prime}$ [a]")
    plt.show()
    plt.close()

    return

################################################################################################################################################



###################################
###################################
#####          UTILS          #####
###################################
###################################
def derivative(f, x):
    h = 1e-6  # Small step size for numerical differentiation
    return (f(x + h) - f(x)) / h
###################################



###################################
def myfunc(x):
    return x**2
###################################

