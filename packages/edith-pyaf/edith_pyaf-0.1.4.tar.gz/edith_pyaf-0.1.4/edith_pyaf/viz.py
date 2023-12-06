#!/usr/bin/env python
############################################################################################
##### This file collects visualization routines.
############################################################################################


####################################
###########  IMPORTS   #############
####################################
import matplotlib.pyplot as plt
import numpy as np

from pylab import * #for movies
import matplotlib.animation as animation #for movies

# Custom modules:
from . import utils
from . import input_output as ino
from . import input as inp
from . import dynamics as dyn
####################################


######################################################################################
def visualize_hamiltonian(Ham):

    if Ham.sparse:
        H = utils.get_full_Hamiltonian(Ham)
    
    else:
        H = Ham.matrix

    # Plot:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot = ax.imshow(H)
    cbar = plt.colorbar(plot)
    plt.show()
    plt.close()

    return
######################################################################################


######################################################################################
def visualize_eigenstate(evec_Hilbert, index, Ham):
    """
    
    Notes:
    ------
    This only works for spinless fermions or spin systems.

    """

    model = Ham.model
    pars = Ham.pars
    par_keys, par_vals = utils.get_parameters_from_dict(pars)

    # Assemble the title:
    title = "{0}-th eigenstate for {1} with parameters ".format(index, model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            title = title + "{0}={1}.".format(par_keys[i], par_vals[i])
        else:
            title = title + "{0}={1}, ".format(par_keys[i], par_vals[i])

    # Get eigenvector in visualizable format:
    #print(evec_Hilbert)
    state = utils.get_state_population_spinless(Ham=Ham, state=evec_Hilbert)
    #print("evec:", evec)

    # WRONG DEFINITION OF PARTICLE NUMBER EXPECTATION VALUE:
    # fig = plt.figure(figsize=(12,8))
    # ax1 = fig.add_subplot(211)
    # plot1_re = ax1.plot(np.linspace(1,len(evec),len(evec)), np.real(evec)/np.sum(np.abs(evec)**2), marker='o', color='blue', ms=5, label="Real part")
    # plot1_im = ax1.plot(np.linspace(1,len(evec),len(evec)), np.imag(evec)/np.sum(np.abs(evec)**2), marker='o', color='red', ms=5, label="Imaginary part")
    # ax1.set_xlabel(r"site $j$")
    # ax1.set_ylabel(r"Eigenstate amplitude")
    # plt.legend(loc='best')
    # ax2 = fig.add_subplot(212)
    # plot2 = ax2.plot(np.linspace(1,len(evec),len(evec)), np.abs(evec)**2/np.sum(np.abs(evec)**2), marker='o', color='blue', ms=5, label="Absolute value squared")
    # ax2.set_xlabel(r"site $j$")
    # ax2.set_ylabel(r"Eigenstate probability")
    # plt.legend(loc='best')


    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(111)
    plot1 = ax1.plot(np.linspace(1,len(state),len(state)), state, marker='o', color='blue', ms=5, label="Absolute value squared")
    ax1.set_xlabel(r"site $j$")
    ax1.set_ylabel(r"Eigenstate probability")
    plt.legend(loc='best')
    plt.suptitle(title)
    plt.show()
    plt.close()

    #print("Sum check:", np.sum(np.abs(evec)**2))

    return
######################################################################################


######################################################################################
def visualize_eigenstate_multicomponent(evec_Hilbert, index, Ham):

    """
    
    Notes:
    -----
    This only works for multicomponent fermionic or bosonic systems, e.g. spinful fermions.

    """

    model = Ham.model
    pars = Ham.pars
    par_keys, par_vals = utils.get_parameters_from_dict(pars)

    # Assemble the title:
    title = "{0}-th eigenstate for {1} with parameters ".format(index, model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            title = title + "{0}={1}-".format(par_keys[i], par_vals[i])
        else:
            title = title + "{0}={1}, ".format(par_keys[i], par_vals[i])

    # Get eigenvector in visualizable format:
    #print(evec_Hilbert)
    evec_up, evec_down = utils.get_state_population_spinful(evec_Hilbert, Ham=Ham)
    
    # Plot:
    fig = plt.figure(figsize=(12,8))

    #
    # WRONG DEFINITION OF PARTICLE NUMBER EXPECTATION:
    #
    # ax1 = fig.add_subplot(211)
    # plot_up_re = ax1.plot(np.linspace(1,len(evec_up),len(evec_up)), np.real(evec_up)/np.sum(np.abs(evec_up)**2), marker='o', color='blue', ms=5, linestyle='solid', label="Spin up (real part)")
    # plot_up_im = ax1.plot(np.linspace(1,len(evec_up),len(evec_up)), np.imag(evec_up)/np.sum(np.abs(evec_up)**2), marker='o', color='lightblue', ms=5, linestyle='dashed', label="Spin up (imaginary part)")
    # plot_up_re = ax1.plot(np.linspace(1,len(evec_down),len(evec_down)), np.real(evec_down)/np.sum(np.abs(evec_down)**2), marker='x', color='crimson', ms=5, linestyle='solid', label="Spin down (real part)")
    # plot_up_im = ax1.plot(np.linspace(1,len(evec_down),len(evec_down)), np.imag(evec_down)/np.sum(np.abs(evec_down)**2), marker='x', color='lightcoral', ms=5, linestyle='dashed', label="Spin down (imaginary part)")
    # ax1.set_xlabel(r"site $j$")
    # ax1.set_ylabel(r"Eigenstate amplitude")
    # plt.legend(loc='best')
    # ax2 = fig.add_subplot(111)
    # plot2 = ax2.plot(np.linspace(1,len(evec_up),len(evec_up)), np.abs(evec_up)**2/np.sum(np.abs(evec_up)**2), marker='o', color='blue', ms=5, label="Spin up (absolute value squared)")
    # plot2 = ax2.plot(np.linspace(1,len(evec_down),len(evec_down)), np.abs(evec_down)**2/np.sum(np.abs(evec_down)**2), marker='x', color='crimson', ms=5, label="Spin down (absolute value squared)")
    # ax2.set_xlabel(r"site $j$")
    # ax2.set_ylabel(r"Eigenstate probability")
    # plt.legend(loc='best')

    ax1 = fig.add_subplot(111)
    plot1 = ax1.plot(np.linspace(1,len(evec_up),len(evec_up)), evec_up, marker='o', color='blue', ms=5, label="Spin up (absolute value squared)")
    plot1 = ax1.plot(np.linspace(1,len(evec_down),len(evec_down)), evec_down, marker='x', color='crimson', ms=5, label="Spin down (absolute value squared)")
    ax1.set_xlabel(r"site $j$")
    ax1.set_ylabel(r"Eigenstate probability")
    plt.legend(loc='best')

    plt.suptitle(title)
    plt.show()
    plt.close()

    #print("Sum check:", np.sum(np.abs(evec)**2))

    return
######################################################################################

######################################################################################
def plot_time_evolution_spinless(time_evolved_state, Ham, initial_state, dt, final_time):
    """
    Creates a plot of the time evolution of a many-body state. Each projection onto different basis states is plotted.

    Parameters:
    ----------
    time_evolved_state, list of (list of) floats: the many-body state in the eigenbasis as time evolves.

    Ham, instance of Hamiltonian class: the (possibly sparse) Hamiltonian.

    initial_state, str: the string encoding of the initial state as zeros and ones.

    dt, float: time step in the propagation.

    final_time, float: the final time in the propagation.


    Notes:
    ------
    
    
    """

    utils.check_dir("plots")

    # Extracting metadata for labels etc:
    model = Ham.model
    pars = Ham.pars
    stats = Ham.stats
    par_keys, par_vals = utils.get_parameters_from_dict(pars)

    # Assemble the title:
    title = "Many-body dynamics for {0} with parameters ".format(model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            title = title + "{0}={1}.".format(par_keys[i], par_vals[i])
        else:
            title = title + "{0}={1}, ".format(par_keys[i], par_vals[i])
    title = title + " and initial state "+initial_state

    times = np.arange(0, final_time, dt)

    # Create figure
    fig = plt.figure(figsize=(16,8))

    # Plot of real/imaginary part:    
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    colormap = plt.cm.rainbow #nipy_spectral, Set1,Paired 
    colors = [colormap(i) for i in np.linspace(0, 1, Ham.sector_dim)]
    #print("Ham.sector_dim", Ham.sector_dim)

    for b in Ham.basis_states:
        #print("b:",b)
        bin = np.binary_repr(b, width=Ham.sites)
        idx_b, _ = utils.lexRank(bin)   # index of basis state in the given sector
        #print("idx_b", idx_b)
        #print("time evolved state:", time_evolved_state)
        #print("time evolved state:", time_evolved_state[:, idx_b])
        plot1_re = ax1.plot(times, np.real(time_evolved_state[:,idx_b]), marker='o', color=colors[idx_b], ms=5, lw=2, linestyle='solid', label=bin+"(Real part)")
        plot1_im = ax1.plot(times, np.imag(time_evolved_state[:,idx_b]), marker='x', color=colors[idx_b], ms=5, lw=2, linestyle='dashed', label=bin+"(Imaginary part)")
        plot2 = ax2.plot(times, np.abs(time_evolved_state[:,idx_b])**2, marker='o', color=colors[idx_b], ms=5, lw=2, linestyle='solid', label=bin)
    
    # Analytical results for benchmark:
    if Ham.model=="dipolar-Aubry-Andre" and Ham.sites==2 and Ham.pars["N"]==1:
        time_evolved_state_anal = dyn.dipolar_Aubry_Andre_dynamics_check(Delta=Ham.pars["Delta"],
                                                                         beta=Ham.pars["beta"],
                                                                         phi=Ham.pars["phi"],
                                                                         hopp=Ham.pars["t"], 
                                                                         final_time=final_time,
                                                                         dt=dt)
        plot1_comp1_re_anal = ax1.plot(times, np.real(time_evolved_state_anal[:,0]), marker='o', color="dimgray", ms=5, lw=2, linestyle='solid', label="01"+"(Real part - analytical)")
        plot1_comp1_im_anal = ax1.plot(times, np.imag(time_evolved_state_anal[:,0]), marker='x', color="gray", ms=5, lw=2, linestyle='dashed', label="01"+"(Imaginary part - analytical)")
        plot1_comp2_re_anal = ax1.plot(times, np.real(time_evolved_state_anal[:,1]), marker='o', color="gainsboro", ms=5, lw=2, linestyle='solid', label="10"+"(Real part - analytical)")
        plot1_comp2_im_anal = ax1.plot(times, np.imag(time_evolved_state_anal[:,1]), marker='x', color="whitesmoke", ms=5, lw=2, linestyle='dashed', label="10"+"(Imaginary part - analytical)")
        plot2_comp1_anal = ax2.plot(times, np.abs(time_evolved_state_anal[:,0])**2, marker='o', color="dimgray", ms=5, lw=2, linestyle='solid', label="01 (analytical)")
        plot2_comp2_anal = ax2.plot(times, np.abs(time_evolved_state_anal[:,1])**2, marker='o', color="gainsboro", ms=5, lw=2, linestyle='solid', label="10 (analytical)")

    
    elif Ham.model=="dipolar-Aubry-Andre" and Ham.sites==4 and Ham.pars["N"]==1 and Ham.pars["Delta"]==1.0 and Ham.pars["beta"]==0.1591549431 and Ham.pars["phi"]==1.0 and Ham.pars["t"]==1.0:
        time_evolved_state_anal = dyn.dipolar_Aubry_Andre_dynamics_check2(final_time=final_time,
                                                                         dt=dt)
        plot2_comp1_anal = ax2.plot(times, np.abs(time_evolved_state_anal[:,0])**2, marker='o', color="dimgray", ms=5, lw=2, linestyle='solid', label="0001 (analytical)")
        plot2_comp2_anal = ax2.plot(times, np.abs(time_evolved_state_anal[:,1])**2, marker='o', color="gray", ms=5, lw=2, linestyle='solid', label="0010 (analytical)")
        plot2_comp3_anal = ax2.plot(times, np.abs(time_evolved_state_anal[:,2])**2, marker='o', color="gainsboro", ms=5, lw=2, linestyle='solid', label="0100 (analytical)")
        plot2_comp4_anal = ax2.plot(times, np.abs(time_evolved_state_anal[:,3])**2, marker='o', color="whitesmoke", ms=5, lw=2, linestyle='solid', label="1000 (analytical)")

    ax1.set_xlabel(r"Time $t$")
    ax1.set_ylabel(r"State amplitude")
    ax2.set_xlabel(r"Time $t$")
    ax2.set_ylabel(r"State probability")
    if Ham.sector_dim <= 16:
        ax1.legend(loc='best', ncols=4)
        ax2.legend(loc='best', ncols=4)

    plt.suptitle(title)
    plt.tight_layout()
    #plt.show()

    # Creating a descriptive filename for the plot
    filename = "plots/time-evolution-{0}-".format(model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            filename = filename + "{0}-{1}-".format(par_keys[i], par_vals[i])
        else:
            filename = filename + "{0}-{1}, ".format(par_keys[i], par_vals[i])
    filename = filename + "dt-{0}-tfinal-{1}-initial-state-{2}.png".format(dt, final_time, initial_state)

    plt.savefig(filename)
    plt.close()

    if Ham.model=="dipolar-Aubry-Andre":
        if (Ham.sites==2 and Ham.pars["N"]==1) or (Ham.sites==4 and Ham.pars["N"]==1):
            print("time_evolved_state:")
            print(time_evolved_state)
            print("time_evolved_state_anal:")
            print(time_evolved_state_anal)

    return
######################################################################################


######################################################################################
def plot_density_vs_t_spinless(time_evolved_state, Ham, initial_state, dt, final_time):
    """
    Creates a plot of the time evolution of the many-body state density at each site as a heatmap.

    Parameters:
    ----------
    time_evolved_state, list of (list of) floats: the many-body state in the eigenbasis as time evolves.

    Ham, instance of Hamiltonian class: the (possibly sparse) Hamiltonian.

    initial_state, str: the string encoding of the initial state as zeros and ones.

    dt, float: time step in the propagation.

    final_time, float: the final time in the propagation.


    Notes:
    ------
    
    
    """

    utils.check_dir("plots")

    # Extracting metadata for labels etc:
    model = Ham.model
    pars = Ham.pars
    stats = Ham.stats
    sites = Ham.sites
    par_keys, par_vals = utils.get_parameters_from_dict(pars)

    # Assemble the title:
    title = "Many-body state for {0} with parameters ".format(model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            title = title + "{0}={1}.".format(par_keys[i], par_vals[i])
        else:
            title = title + "{0}={1}, ".format(par_keys[i], par_vals[i])

    dens_arr = []
    for state in time_evolved_state:
        # Get state in visualizable format:
        dens_arr.append(utils.get_state_population_spinless(Ham=Ham,state=state))

    dens_arr = np.real(np.array(dens_arr))

    # Plot:
    fig = plt.figure(figsize=(14,8))
    ax1 = fig.add_subplot(111)
    X, Y = np.meshgrid(np.arange(0.0, final_time, dt), np.arange(1,sites+1,1))
    plot = ax1.pcolormesh(X, Y, dens_arr.T, cmap='inferno')
    plt.colorbar(plot)
    ax1.set_ylim([1, sites])
    ax1.set_xlabel(r"Time $t$")
    ax1.set_ylabel(r"Site $j$")

    plt.suptitle(title)
    plt.tight_layout()
    #plt.show()
    filename = "plots/density-dynamics-{0}-".format(model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            filename = filename + "{0}-{1}-".format(par_keys[i], par_vals[i])
        else:
            filename = filename + "{0}-{1}, ".format(par_keys[i], par_vals[i])
    filename = filename + "dt-{0}-tfinal-{1}-initial-state-{2}.png".format(dt, final_time, initial_state)

    plt.savefig(filename)    
    plt.close()

    return
######################################################################################

######################################################################################
def plot_density_vs_t_spinful(time_evolved_state, Ham, initial_state, dt, final_time):
    """
    Creates a plot of the time evolution of the many-body state density at each site as a heatmap.

    Parameters:
    ----------
    time_evolved_state, list of (list of) floats: the many-body state in the eigenbasis as time evolves.

    Ham, instance of Hamiltonian class: the (possibly sparse) Hamiltonian.

    initial_state, str: the string encoding of the initial state as zeros and ones.

    dt, float: time step in the propagation.

    final_time, float: the final time in the propagation.


    Notes:
    ------
    
    
    """

    utils.check_dir("plots")

    # Extracting metadata for labels etc:
    model = Ham.model
    pars = Ham.pars
    stats = Ham.stats
    sites = Ham.sites
    par_keys, par_vals = utils.get_parameters_from_dict(pars)

    # Assemble the title:
    title = "Many-body state for {0} with parameters ".format(model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            title = title + "{0}={1}.".format(par_keys[i], par_vals[i])
        else:
            title = title + "{0}={1}, ".format(par_keys[i], par_vals[i])

    dens_arr_up = []
    dens_arr_down = []
    for state in time_evolved_state:
        # Get state in visualizable format:
        dens_up, dens_down = utils.get_state_population_spinful(Ham=Ham,state=state)
        dens_arr_up.append(dens_up)
        dens_arr_down.append(dens_down)

    dens_arr_up = np.array(dens_arr_up)
    dens_arr_down = np.array(dens_arr_down)

    # Plot:
    fig = plt.figure(figsize=(14,8))
    ax1 = fig.add_subplot(211)
    X, Y = np.meshgrid(np.arange(0.0, final_time, dt), np.arange(1,sites+1,1))
    plot = ax1.pcolormesh(X, Y, dens_arr_up.T, cmap='inferno')
    plt.colorbar(plot)
    ax1.set_ylim([1, sites])
    ax1.set_xlabel(r"Time $t$")
    ax1.set_ylabel(r"Site $j$")
    ax1.set_title("Spin up component")

    ax2 = fig.add_subplot(212)
    plot2 = ax2.pcolormesh(X, Y, dens_arr_down.T, cmap='inferno')
    plt.colorbar(plot2)
    ax2.set_ylim([1, sites])
    ax2.set_xlabel(r"Time $t$")
    ax2.set_ylabel(r"Site $j$")
    ax2.set_title("Spin down component")

    plt.suptitle(title)
    plt.tight_layout()
    #plt.show()

    filename = "plots/density-dynamics-{0}-".format(model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            filename = filename + "{0}-{1}-".format(par_keys[i], par_vals[i])
        else:
            filename = filename + "{0}-{1}, ".format(par_keys[i], par_vals[i])
    filename = filename + "dt-{0}-tfinal-{1}-initial-state-{2}.png".format(dt, final_time, initial_state)

    plt.savefig(filename)    
    plt.close()

    return
######################################################################################

######################################################################################
def movie_time_evolution_spinless(time_evolved_state, Ham, initial_state, dt, final_time):
    """
    Creates a movie of the time evolution of a many-body state.

    Parameters:
    ----------
    time_evolved_state, list of (list of) floats: the many-body state in the eigenbasis as time evolves.

    Ham, instance of Hamiltonian class: the (possibly sparse) Hamiltonian.

    initial_state, str: the string encoding of the initial state as zeros and ones.

    dt, float: time step in the propagation.

    final_time, float: the final time in the propagation.


    Notes:
    ------
    
    
    """

    utils.check_dir("movies")


    # Extracting metadata for labels etc:
    model = Ham.model
    pars = Ham.pars
    stats = Ham.stats
    par_keys, par_vals = utils.get_parameters_from_dict(pars)

    # Assemble the title:
    title = "Many-body state at time t={0} for {1} with parameters ".format(0, model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            title = title + "{0}={1}.".format(par_keys[i], par_vals[i])
        else:
            title = title + "{0}={1}, ".format(par_keys[i], par_vals[i])

    # Get initial state in visualizable format:
    state_pop = utils.get_state_population_spinless(Ham=Ham,state=time_evolved_state[0])

    ##############
    # movie part #
    ##############

    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='PaoloMolignini'), bitrate=1800)
        
    # Create figure
    fig = plt.figure(figsize=(14,8))

    # First plot:
    ax1 = fig.add_subplot(111)
    plot = ax1.plot(np.linspace(1,len(state_pop),len(state_pop)), state_pop, marker='o', color='blue', ms=5, lw=3, label="Absolute value squared")
    ax1.set_ylim([-0.1, 1.1])
    ax1.set_xlabel(r"site $j$")
    ax1.set_ylabel(r"State probability")
    plt.legend(loc='best')

    plt.suptitle(title)
    plt.tight_layout()


    # Total number of frames:
    frame_number = len(time_evolved_state)
    # Defines the frame speed of the movie (interval between frames in ms):
    speed_movie = 50
    #values of the function to be updated:
    fargs = [fig, ax1, model, par_keys, par_vals, dt, time_evolved_state, Ham]
            
    # Animation iteration routine:
    ani = animation.FuncAnimation(fig, animate_time_evol_spinless, frames=np.arange(0,frame_number), fargs=[fargs], interval=speed_movie, blit=False, repeat=False)

    # Creating a descriptive filename for the movie
    filename = "movies/time-evolution-{0}-".format(model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            filename = filename + "{0}-{1}".format(par_keys[i], par_vals[i])
        else:
            filename = filename + "{0}-{1}, ".format(par_keys[i], par_vals[i])
    filename = filename + "dt-{0}-tfinal-{1}-initial-state-{2}.mp4".format(dt, final_time, initial_state)

    ani.save(filename, writer=writer, dpi=500)

    plt.close()
    return

########################################################################################################
#callable function for the iteration of the frames in the animation:
def animate_time_evol_spinless(frames, fargs):
    
    # Get fargs:
    fig = fargs[0]
    ax1 = fargs[1]
    model = fargs[2]
    par_keys = fargs[3]
    par_vals = fargs[4]
    dt = fargs[5]
    state = fargs[6]
    Ham = fargs[7]
    current_state_pop = utils.get_state_population_spinless(Ham=Ham,
                                                            state=state[frames])


    # Assemble the title:
    title = "Many-body state at time t={0} for {1} with parameters ".format(np.round(dt*frames,2), model)
    for i in range(len(par_keys)):
        if i==len(par_keys)-1:
            title = title + "{0}={1}.".format(par_keys[i], par_vals[i])
        else:
            title = title + "{0}={1}, ".format(par_keys[i], par_vals[i])


    # Print status:    
    print(f"Working on frame: {frames}")
    
    # Clear canvas and plot current data:
    ax1.cla()

    # plot
    plot = ax1.plot(np.linspace(1,len(current_state_pop),len(current_state_pop)), current_state_pop, marker='o', color='blue', ms=5, lw=3, label="Absolute value squared")
    ax1.set_xlabel(r"site $j$")
    ax1.set_ylabel(r"State probability")
    ax1.legend(loc='best')
    ax1.set_ylim([-0.1, 1.1])

    plt.suptitle(title)
    plt.tight_layout()

    return ax1,
########################################################################################################


######################################################################################
def movie_time_evolution_spinful(time_evolved_state, Ham, initial_state, dt, final_time):
    raise NotImplementedError()
######################################################################################








######################################################################################
def plot_eigenvalues_vs_parameter(evals, 
                                  p_list, 
                                  **kwargs):
    """
    Plots the spectrum as a function of a tuning parameter.

    Parameters:
    ----------
    evals, list of (list of) floats: the eigenvalues as the parameter is tuned.

    p_list, list of floats: the values of the parameter.

    Notes:
    ------
    This assumes that the eigenvalues are sorted.
    
    """

    utils.check_dir("plots")

    # Extracting parameters and labels:
    param_len, evals_len = np.shape(evals)
    print("evals_len:", evals_len)
    print("param_len:", param_len)    
    param_name = kwargs.get("param_name")
    model = kwargs.get("model")
    sites = kwargs.get("sites")
    BC = ino.get_BC(kwargs.get("PBC"))
    pars = kwargs.get("pars")
    del pars[param_name]    # removing the parameter we are looping over from namelist!
    pi = p_list[0]
    pf = p_list[-1]


    # Setting up the colors:
    colormap = plt.cm.rainbow #nipy_spectral, Set1,Paired 
    colors = [colormap(i) for i in np.linspace(0, 1, evals_len)]

    # Normalizing wrt to ground state energy:
    for i in range(param_len):
        evals[i,:] = evals[i,:] - np.amin(evals[i,:])

    # Plot(s):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(evals_len):
        ax.plot(np.array(p_list), evals[:,i], color=colors[i], linestyle="None", marker='o', ms=5)
    plt.xlabel(param_name)
    plt.ylabel("$E_i - E_0$")
    plt.title(f"Lowest {inp.n_lowest_eigenvalues} eigenvalues of the {model} model")

    # Saving plot:
    filename="plots/evals-{0}-model-{1}-sites-{2}-{3}-pars".format(inp.n_lowest_eigenvalues, model, sites, BC)

    par_keys=[]
    par_vals=[]
    for par in pars:
        par_keys.append(par)
        par_vals.append(pars[par])

    for i in range(len(pars)):
        filename=filename+"-{0}-{1}".format(par_keys[i],par_vals[i])

    filename=filename+"-{0}-{1}-{2}-{3}.png".format(param_name, pi, pf, param_len)

    plt.savefig(filename)

    #plt.show()
    plt.close()

    return
######################################################################################


######################################################################################
def plot_observable_vs_two_parameters(obs_name, obs, pars, par_lists, model, sites, BC, static_pars, **kwargs):
    """
    Plots a real observable as a heatmap (function of two tuning parameters).

    Parameters:
    ----------
    obs_name, str: the name of the observable.

    obs, numpy array: the observable to plot.

    pars, dict: the names of the parameters that are being tuned.

    par_lists, dict of lists: the values of the parameters being tuned.

    model, str: the name of the model.

    site, int: the number of sites in the system.

    BC, str: flag for boundary conditions.

    static_pars, dict: the other parameters that are NOT being tuned.

    Notes:
    ------
    
    """
    log_opt = kwargs.get("log_opt", "")

    # Constructing the filename and the title:
    filename="plots/{0}-model-{1}-sites-{2}-{3}-pars".format(obs_name, model, sites, BC)
    title = f"{obs_name} for {model} model with {sites} sites and parameters"+"\n"
    
    par_keys=[]
    par_vals=[]
    for par in static_pars:
        par_keys.append(par)
        par_vals.append(static_pars[par])
    for i in range(len(static_pars)):
        filename += "-{0}-{1}".format(par_keys[i],par_vals[i])
        title += "{0}={1}, ".format(par_keys[i],par_vals[i])

    filename=filename+"-{0}-{1}-{2}-{3}-{4}-{5}-{6}.png".format(pars[0], par_lists[pars[0]][0], par_lists[pars[0]][1], len(par_lists[pars[0]]), par_lists[pars[1]][0], par_lists[pars[1]][1], len(par_lists[pars[1]]))  


    # Plot(s):
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    X, Y = np.meshgrid(par_lists[pars[0]], par_lists[pars[1]])
    Z = obs
    heatmap = ax.pcolormesh(X, Y, Z.T, cmap="inferno", shading="auto")
    if pars[0] in log_opt:
        ax.set_xscale("log")    
    if pars[1] in log_opt:
        ax.set_yscale("log")    
    plt.colorbar(heatmap)
    plt.xlabel(pars[0])
    plt.ylabel(pars[1])
    plt.title(title)

    # Saving plot:
    plt.savefig(filename)
    #plt.show()
    plt.close()

    return


######################################################################################