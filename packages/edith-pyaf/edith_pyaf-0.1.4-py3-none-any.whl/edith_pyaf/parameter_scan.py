#!/usr/bin/env python
##########################################################################################
# This python program performs exact diagonalization of closed systems.
###########################################################################################


######################################
#############  IMPORTS   #############
######################################
from __future__ import division
from __future__ import print_function
import numpy as np
from numpy import cos, sin, sqrt, arctan, tan, exp
import itertools
import importlib as imp
from tqdm import tqdm

# CUSTOM modules:
import input as inp
import input_output as ino
import main
import viz
import utils
######################################

######################################
#### INPUT ####
############################################################################
model = "dipolar-Aubry-Andre"
parameters = ["eta", "Delta"]
static_parameters = {"N": 7, "t": 1.0, "beta": np.round((np.sqrt(5)+1)/2, 3), "phi": 0.0}
start_values = {"eta": -2, "Delta": 0.0}
end_values = {"eta": 2, "Delta": 10.0}
n_points = {"eta": 21, "Delta": 21}
sites = 14
PBC = False
exec = True
# TODO: modify also static parameters in input file?

rounding_prec = 4


plot_parameter_scan=True
plot_IPR=True
plot_evals=False
############################################################################


#TODO: unify all loops over different models
if exec == True:

      ######################################
      #### transverse field Ising model ####
      ############################################################################

      if inp.plot_evals==True:
            evals = []

      if model=="transverse-Ising":
            for par in tqdm(parameters):
                  p_list = np.linspace(start_values[par], end_values[par], n_points[par])
                  for value in tqdm(p_list):

                        value = np.round(value, rounding_prec)

                        print(f"Generating data for {par}={value}")

                        # Modifying the input file:
                        if par=="hx":
                              ino.modify_input(target="Ham_par2", value=value)
                        imp.reload(inp)   # Here the input is reloaded in the import!

                        # Calculating the eigenvalues and saving the data:
                        Ham = main.main() 

                        if inp.plot_evals==True:
                              # Load data:
                              evals.append(ino.load_eigenvalues(Ham=Ham))
      ############################################################################

      ######################################
      #### Staggered Heisenberg model ####
      ############################################################################
      elif model=="staggered-Heisenberg":
            for par in tqdm(parameters):
                  p_list = np.linspace(start_values[par], end_values[par], n_points[par])
                  for value in tqdm(p_list):
                        value = np.round(value, rounding_prec)
                        print(f"Generating data for {par}={value}")

                        # Modifying the input file:
                        if par=="hs":
                              ino.modify_input(target="Ham_par2", value=value)
                              imp.reload(inp)   # Here the input is reloaded in the import!

                        # Calculating the eigenvalues and saving the data:
                        Ham = main.main() 

                        if inp.plot_evals==True:
                              # Load data:
                              evals.append(ino.load_eigenvalues(Ham=Ham))

      ############################################################################





      ######################################
      #### Dipolar Aubry-Andre ####
      ############################################################################
      elif model=="dipolar-Aubry-Andre":

            # Defining all the parameter lists:
            par_lists = {}
            args = []
            for par in parameters:
                  if par=="Delta":
                        par_lists[par] = np.linspace(start_values[par], end_values[par], n_points[par])
                  elif par=="eta":
                        par_lists[par] = 10**(np.linspace(start_values[par], end_values[par], n_points[par]))

                  args.append(par_lists[par])


            # Loop over all combination of parameters:
            for combination in tqdm(itertools.product(*args)):
            
                  out_str = "Generating data for "
                  for i in range(len(parameters)):
                        out_str += f"{parameters[i]}={combination[i]}     "
                  print(out_str)

                  # Iteratively modify the input file for each parameter:
                  for idx, value in enumerate(combination):

                        par=parameters[idx]
                        value = np.round(value, rounding_prec)

                        # Modifying the input file:
                        if par=="Delta":
                              ino.modify_input(target="Ham_par3", value=value)

                        if par=="eta":
                              ino.modify_input(target="Ham_par6", value=[value])    #eta has to be given as a list!

                        if par=="N":
                              ino.modify_input(target="Ham_par1", value=value)


                  imp.reload(inp)   # Here the input is reloaded in the import!

                  # Doing the main calculation:
                  Ham = main.main() 
      ############################################################################



#####################################
#### PLOT of the parameter scan  ####
########################################################################
if plot_parameter_scan == True:

      # Defining all the parameter lists:
      par_lists = {}
      args = []
      for par in parameters:
            if par=="Delta": 
                  par_lists[par] = np.linspace(start_values[par], end_values[par], n_points[par])
            elif par=="eta":
                  par_lists[par] = 10**(np.linspace(start_values[par], end_values[par], n_points[par]))

            args.append(par_lists[par])


      # Loop over all combination of parameters:
      # for combination in tqdm(itertools.product(*args)):
      shape = tuple(n_points[parameters[k]] for k in range(len(parameters)))
      IPR_arr = np.zeros(shape=shape)
      for idx, combination in tqdm(utils.enumerated_product(*args)):

            # Generating output string and dictionary for current parameter selection 
            # (merged with static parameters)
            pars = dict(static_parameters)
            out_str = "Loading data for "
            for i in range(len(parameters)):
                  rounded_value = np.round(combination[i], rounding_prec)
                  out_str += f"{parameters[i]}={rounded_value}     "
                  if parameters[i]=="eta":
                        pars[parameters[i]] = [rounded_value]
                  else:
                        pars[parameters[i]] = rounded_value
            print(out_str)
            
            par_keys = list(pars.keys())
            par_keys.sort()
            sorted_pars = {i: pars[i] for i in par_keys}                
            
            # Load eigenvalue data
            if plot_IPR==True:

                  # Assembling filename for current data to be loaded:
                  IPR_arr[idx] = ino.load_obs(model=model,
                                              sites=sites, 
                                              pars=sorted_pars,
                                              BC=PBC,
                                              obs_name="IPR")

      if len(parameters)==2:

            viz.plot_observable_vs_two_parameters(obs_name="IPR",
                                                  obs=IPR_arr, 
                                                  pars=parameters, 
                                                  par_lists=par_lists, 
                                                  model=model, 
                                                  sites=sites, 
                                                  BC=PBC, 
                                                  static_pars=static_parameters,
                                                  log_opt="eta")
            
########################################################################

