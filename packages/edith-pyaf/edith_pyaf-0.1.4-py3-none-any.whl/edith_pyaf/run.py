#!/usr/bin/env python
##########################################################################################
# This python program performs exact diagonalization of closed systems.
###########################################################################################

####################################
###########  IMPORTS   #############
####################################
from __future__ import division
from __future__ import print_function
import numpy as np

# CUSTOM modules:
from . import input as inp
from . import glob 
from . import hams
from . import diag
from . import obs
from . import utils
from . import dynamics as dyn
from . import viz
from . import input_output as ino
####################################




############################################################################################################
def main(input_filename):

      # Get the input
      input = inp.Input(input_filename=input_filename)

      # print("input_filename:", input_filename)
      # print("stats:", input.stats)
      # print("model:", input.model)
      # print("sites:", input.sites)
      # print("PBC:", input.PBC)
      # print("sparse:", input.sparse)
      # print("Ham_par1:", input.Ham_par1)
      # print("Ham_par2:", input.Ham_par2)
      # print("Ham_par3:", input.Ham_par3)
      # print("Ham_par4:", input.Ham_par4)
      # print("Ham_par5:", input.Ham_par5)
      # print("Ham_par6:", input.Ham_par6)
      # print("Ham_par7:", input.Ham_par7)
      # print("Ham_par8:", input.Ham_par8)
      # print("Ham_par9:", input.Ham_par9)
      # print("Ham_par10:", input.Ham_par10)
      # print("Ham_par10:", input.Ham_par10)
      # print("Ham_par10:", input.Ham_par10)
      # print("n_lowest_eigenvalues:", input.n_lowest_eigenvalues)
      # print("maxiter_Arnoldi:", input.maxiter_Arnoldi)
      # print("save_evals:", input.save_evals)
      # print("compute_evecs:", input.compute_evecs)
      # print("save_evecs:", input.save_evecs)
      # print("load_input_parameters:", input.load_input_parameters)
      # print("dynamics:", input.dynamics)
      # print("initial_state:", input.initial_state)
      # print("final_time:", input.final_time)
      # print("dt:", input.dt)
      # print("print_gs_energy:", input.print_gs_energy)
      # print("print_es_energies:", input.print_es_energies)
      # print("print_gs:", input.print_gs)
      # print("print_es:", input.print_es)
      # print("dt:", input.dt)
      # print("plot_Hamiltonian:", input.plot_Hamiltonian)
      # print("plot_evals:", input.plot_evals)
      # print("plot_evecs:", input.plot_evecs)
      # print("plot_dynamics:", input.plot_dynamics)
      # print("movie_dynamics:", input.movie_dynamics)
      # print("verbose:", input.verbose)


      ####################################
      ################################################################
      ######### INPUT SELF-CONSISTENCY CHECKS
      ################################################################

      if input.model== "dipolar-Aubry-Andre":

            if input.n_lowest_eigenvalues > utils.binomial(input.sites,int(input.Ham_par1)):
                  raise IOError(f"The given sector N={int(input.Ham_par1)} has {utils.binomial(input.sites,int(input.Ham_par1))} states! Please set \"n_lowest_eigenvalues\" to max this value in the input file.")


            if input.dynamics==True and input.n_lowest_eigenvalues < utils.binomial(input.sites,int(input.Ham_par1)):
                  raise IOError(f"To calculate full-time dynamics of the given sector N={int(input.Ham_par1)}, you need to calculate all the eigenvalues! Please set \"n_lowest_eigenvalues\" to {utils.binomial(input.sites,int(input.Ham_par1))} in the input file.")
             


      ################################################################
      ######### SETTING UP HAMILTONIAN
      ################################################################

      Ham = hams.Hamiltonian(input=input)

      print("====================================")
      print(f"Model: {Ham.model}")   
      print(f"Type of particles: {Ham.stats}")   
      print("====================================")
      print("\n") 

      print("====================================")
      print("Parameters of the Hamiltonian:")
      print("Sites:", Ham.sites)
      print("Hilbert space dimension:", Ham.Hilbert_dim)
      print("Periodic boundary conditions?", Ham.PBC)
      # Ham_par1:
      if Ham.model=="transverse-Ising" or Ham.model=="staggered-Heisenberg":
            print("Hopping value J:", Ham.pars["J"])
      elif Ham.model=="dipolar-Aubry-Andre":
            print("Total particle number N:", Ham.pars["N"])
      elif Ham.model=="Hubbard":
            print("Total spin z-component sz:", Ham.pars["sz"])

      # Ham_par2:
      if Ham.model=="transverse-Ising":
            print("Transverse field value:", Ham.pars["hx"])
      elif Ham.model=="staggered-Heisenberg":
            print("Staggered field value:", Ham.pars["hs"])
      elif Ham.model=="dipolar-Aubry-Andre":
            print("Hopping t:", Ham.pars["t"])
      elif Ham.model=="Hubbard":
            print("Total particle number N:", Ham.pars["N"])

      # Ham_par3:
      if Ham.model=="staggered-Heisenberg":
            print("Total Sz spin component:", Ham.pars["sz"])
      elif Ham.model=="dipolar-Aubry-Andre":
            print("Quasiperiodic potential strength Delta:", Ham.pars["Delta"])
      elif Ham.model=="Hubbard":
            print("Chemical potential mu:", Ham.pars["mu"])

      # Ham_par4:
      if Ham.model=="dipolar-Aubry-Andre":
            print("Quasiperiodicity wave vector beta:", Ham.pars["beta"])
      elif Ham.model=="Hubbard":
            print("Hopping t:", Ham.pars["t"])

      # Ham_par5:
      if Ham.model=="dipolar-Aubry-Andre":
            print("Phase phi:", Ham.pars["phi"])
      elif Ham.model=="Hubbard":
            print("On-site interaction U:", Ham.pars["U"])

      # Ham_par5:
      if Ham.model=="dipolar-Aubry-Andre":
            print("Nearest-neighbor density-density interaction strength eta:", Ham.pars["eta"])

      print("====================================")
      print("\n") 


      print("====================================")
      print("Sparse encoding?", Ham.sparse)
      print("====================================")
      print("\n") 

      # Visualize Hamiltonian matrix:
      if input.plot_Hamiltonian:
            viz.visualize_hamiltonian(Ham)
            #print(Ham.rows)
            #print(Ham.cols)
            #print(Ham.mat_els)
      ################################################################


      ################################################################
      ######### DIAGONALIZATION
      ################################################################      
      eigenvalues, eigenvectors = diag.diagonalize(Ham=Ham, 
                                                   input=input)
      # Saving eigenvalues:
      if input.save_evals == True:
            print("Saving eigenvalues...")
            ino.save_eigenvalues(model=Ham.model,
                                 sites=Ham.sites,
                                 pars=Ham.pars, 
                                 BC=Ham.PBC,
                                 eigs=eigenvalues)

      # Saving eigenvectors:
      if input.save_evecs == True:
            print("Saving eigenvectors...")
            ino.save_eigenvectors(model=Ham.model, 
                                  sites=Ham.sites, 
                                  pars=Ham.pars, 
                                  BC=Ham.PBC, 
                                  evecs=eigenvectors)

      if input.plot_evecs==True:
            for j in range(np.shape(eigenvectors)[1]):
                  if Ham.stats=="spinful-fermions":
                        viz.visualize_eigenstate_multicomponent(evec_Hilbert=eigenvectors[:,j], 
                                                                index=j, 
                                                                Ham=Ham)
                  elif Ham.stats=="spinless-fermions" or Ham.stats=="spin-0.5":
                        viz.visualize_eigenstate(evec_Hilbert=eigenvectors[:,j], 
                                                 index=j, 
                                                 Ham=Ham)
      # Print some info:
      if input.print_gs_energy==True:
            print("Ground state energy:", min(eigenvalues))
            if Ham.model=="Hubbard":
                  if Ham.pars["sz"]==0 and Ham.pars["N"]==Ham.sites:    #half filling -> exact solution by Lieb & Wu
                        ground_state_exact, err = utils.ground_state_Hubbard_half_filling(t=Ham.pars["t"], U=Ham.pars["U"], N=Ham.sites)
                        print("Ground state energy (extensive part):", ground_state_exact, ". Error:", err)
                        print(f"Ratio of finite-size corrections: {(ground_state_exact-min(eigenvalues))/ground_state_exact*100}%")
      if input.n_lowest_eigenvalues>1:
            if input.print_es_energies==True:
                  print("Excited state energies:", eigenvalues)
      if input.print_gs==True:
            print("Ground state:")
            print(eigenvectors[:,0])
      if input.print_es==True: 
            print("Excited states:")
            print(eigenvectors)
            if input.n_lowest_eigenvalues>1:
                  for k in range(1,input.n_lowest_eigenvalues):
                        print(eigenvectors[:,k])

      ################################################################


      ################################################################
      ######### GROUND-STATE OBSERVABLES
      ################################################################
      print("=======")
      print("basis:")
      print("=======")
      if Ham.stats=="spinful-fermions":
            print("Spin up:")
            print(Ham.basis_states_up)
            print("Spin down:")
            print(Ham.basis_states_down)
      else:
            for b in Ham.basis_states:
                  print(np.binary_repr(b,Ham.sites), b)

      if input.IPR==True:
            IPR = obs.average_IPR(Ham=Ham, evecs=eigenvectors, verbose=input.verbose)
            print("IPR value:", IPR)
            ino.save_obs(model=Ham.model,
                         sites=Ham.sites,
                         pars=Ham.pars, 
                         BC=Ham.PBC,
                         obs_name="IPR",
                         obs_value=IPR)


      ################################################################



      ################################################################
      ######### DYNAMICS
      ################################################################
      if input.dynamics == True:
            print("Calculating dynamics...")
            time_evolved_state = dyn.full_time_evolution(Ham=Ham, 
                                                         evals=eigenvalues, 
                                                         evecs=eigenvectors, 
                                                         initial_state=input.initial_state, 
                                                         final_time=input.final_time, 
                                                         dt=input.dt)
            
            
            if input.plot_dynamics == True:
                  if Ham.stats=="spinful-fermions":
                        raise NotImplementedError()
                  else:
                        viz.plot_time_evolution_spinless(time_evolved_state=time_evolved_state, 
                                                         Ham=Ham,
                                                         initial_state=input.initial_state,
                                                         final_time=input.final_time,
                                                         dt=input.dt)
                        viz.plot_density_vs_t_spinless(time_evolved_state=time_evolved_state, 
                                                       Ham=Ham, 
                                                       initial_state=input.initial_state, 
                                                       dt=input.dt, 
                                                       final_time=input.final_time)

            if input.movie_dynamics == True:
                  if Ham.stats=="spinful-fermions":
                        raise NotImplementedError()
                  else:
                        viz.movie_time_evolution_spinless(time_evolved_state=time_evolved_state,
                                                          Ham=Ham,
                                                          initial_state=input.initial_state,
                                                          final_time=input.final_time,
                                                          dt=input.dt)


      ################################################################


      return 
############################################################################################################





############################################################################################################
if __name__=="__main__":
      Ham = main("input.dat")
############################################################################################################