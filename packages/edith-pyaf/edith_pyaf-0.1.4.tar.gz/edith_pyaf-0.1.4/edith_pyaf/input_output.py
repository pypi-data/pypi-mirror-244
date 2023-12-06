#!/usr/bin/env python
############################################################################################
##### This module deals with input/output.
############################################################################################


####################################
###########  IMPORTS   #############
####################################
import time

# Custom modules:
from . import utils
####################################

# TODO: unify reading input (observables) into single function
# TODO: unify writing output (observables) into single function



######################################################################################
######################################################################################
########## SAVING DATA
######################################################################################
######################################################################################

######################################################################################
def save_eigenvalues(model, sites, pars, BC, eigs):
    """
    Saves the eigenvalues in a .dat file.

    Parameters:
    -----------
    model, str: name of the model.
    sites, int: number of sites L in the system.
    pars, list of str: parameters for the model.
    BC, bool: flag for periodic boundary conditions.
    eigs, list of floats: the eigenvalues of the Hamiltonian.

    """
    utils.check_dir("data")

    filename = get_filename(model, sites, pars, BC, name="evals")

    eigs_list=eigs.tolist()
    with open(filename, 'w') as f:
        for line in eigs_list:
            f.write(str(line))
            f.write('\n')

    return
######################################################################################

######################################################################################
def save_eigenvectors(model, sites, pars, BC, evecs):
    """
    Saves the eigenvalues in a .dat file.

    Parameters:
    -----------
    Ham, instance of Hamiltonian class: the (possibly sparse) Hamiltonian.
    evecs, list of list of floats: the eigenvectors of the Hamiltonian.

    """

    utils.check_dir("data")
    filename = get_filename(model, sites, pars, BC, name="evecs")

    # Different eigenvectors will be separated by an empty line in the file.
    evecs_list=evecs.T.tolist() #the transpose is needed to save the entries in the correct order in the file
    #print(evecs)
    with open(filename, 'w') as f:
        for line in evecs_list:
            for item in line:
                f.write(str(item))
                f.write('\n')
            f.write('\n')

    return
######################################################################################

######################################################################################
def save_obs(model, 
             sites, 
             pars, 
             BC, 
             obs_name,
             obs_value):
    """
    Saves the observable in a .dat file.

    Parameters:
    -----------
    model, str: name of the model.
    sites, int: number of sites L in the system.
    pars, list of str: parameters for the model.
    BC, bool: flag for periodic boundary conditions.
    obs_name, str: the name of the observable.

    """

    utils.check_dir("data")
    filename = get_filename(model=model, 
                            sites=sites, 
                            pars=pars, 
                            BC=BC, 
                            name=obs_name)

    with open(filename, 'w') as f:
        f.write(str(obs_value))

    return
######################################################################################

######################################################################################
######################################################################################
########## LOADING DATA
######################################################################################
######################################################################################


######################################################################################
def load_eigenvalues(model, sites, pars, BC):
    """
    Saves the eigenvalues in a .dat file.

    Parameters:
    -----------
    eigs, list of floats: the eigenvalues of the Hamiltonian.

    """

    filename = get_filename(model, sites, pars, BC, name="evals")

    eigs = []
    with open(filename) as file:
        for line in file:
            eigs.append(float(line.rstrip()))


    return eigs
######################################################################################

######################################################################################
def load_obs(model, 
             sites, 
             pars, 
             BC, 
             obs_name):
    
    filename = get_filename(model=model, 
                            sites=sites, 
                            pars=pars, 
                            BC=BC, 
                            name=obs_name)

    with open(filename) as file:
        for line in file:
            obs=float(line.rstrip())

    return obs
######################################################################################



######################################################################################
######################################################################################
########## CHANGING STRINGS
######################################################################################
######################################################################################

######################################################################################
def get_filename(model, sites, pars, BC, name):


    par_keys, par_vals = utils.get_parameters_from_dict(pars)

    BC = get_BC(BC)

    filename="data/{0}-model-{1}-sites-{2}-{3}-pars".format(name, model, sites, BC)
    #TODO: this is repeated in viz.py --> unify

    for i in range(len(pars)):
        filename=filename+"-{0}-{1}".format(par_keys[i],par_vals[i])

    filename = filename+".dat"

    return filename
######################################################################################

######################################################################################
def get_BC(BC):
    if BC:
        BC_str="PBC"
    else:
        BC_str="OBC"
    return BC_str
######################################################################################





######################################################################################
######################################################################################
########## MODIFYING INPUTS
######################################################################################
######################################################################################

######################################################################################
def modify_input(target, value):
    """
    Searches for the string "target" and modifies with "value".

    """

    # Convert everything to strings to be safe:
    target = str(target)
    value = str(value)

    # Read in input file and corresponding lines:
    with open('input.py', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Search for target line and modify it with new value:
    for i, line in enumerate(lines):
        if target in line:
            line = target+" = "+value+"\n"
            lines[i] = line

    with open('input.py', 'w', encoding='utf-8') as file:
        file.writelines(lines)
    
    # delay to allow the file to be properly saved:
    time.sleep(1)
    
######################################################################################

