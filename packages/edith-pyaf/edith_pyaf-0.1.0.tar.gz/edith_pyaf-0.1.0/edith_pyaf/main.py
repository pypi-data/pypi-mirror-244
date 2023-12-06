#!/usr/bin/env python
##########################################################################################
# This python program performs exact diagonalization of closed systems.
###########################################################################################

####################################
###########  IMPORTS   #############
####################################
from __future__ import division
from __future__ import print_function
import sys
####################################

input_filename = sys.argv[1]

def main():

      
      ################################################################
      ######### INPUT SELF-CONSISTENCY CHECKS
      ################################################################

      if inp.model== "dipolar-Aubry-Andre":

            if inp.n_lowest_eigenvalues > utils.binomial(inp.sites,int(inp.Ham_par1)):
                  raise IOError(f"The given sector N={int(inp.Ham_par1)} has {utils.binomial(inp.sites,int(inp.Ham_par1))} states! Please set \"n_lowest_eigenvalues\" to max this value in the input file.")


            if inp.dynamics==True and inp.n_lowest_eigenvalues < utils.binomial(inp.sites,int(inp.Ham_par1)):
                  raise IOError(f"To calculate full-time dynamics of the given sector N={int(inp.Ham_par1)}, you need to calculate all the eigenvalues! Please set \"n_lowest_eigenvalues\" to {utils.binomial(inp.sites,int(inp.Ham_par1))} in the input file.")
             


      ################################################################
      ######### SETTING UP HAMILTONIAN
      ################################################################

      Ham = hams.Hamiltonian(model = inp.model,
                        stats = inp.stats,
                        sites = inp.sites,
                        PBC = inp.PBC,
                        sparse = inp.sparse)

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
      if inp.plot_Hamiltonian:
            viz.visualize_hamiltonian(Ham)
            #print(Ham.rows)
            #print(Ham.cols)
            #print(Ham.mat_els)
      ################################################################


      ################################################################
      ######### DIAGONALIZATION
      ################################################################      
      eigenvalues, eigenvectors = diag.diagonalize(Ham=Ham, 
                                                   n_evals=inp.n_lowest_eigenvalues)
      # Saving eigenvalues:
      if inp.save_evals == True:
            print("Saving eigenvalues...")
            ino.save_eigenvalues(model=Ham.model,
                                 sites=Ham.sites,
                                 pars=Ham.pars, 
                                 BC=Ham.PBC,
                                 eigs=eigenvalues)

      # Saving eigenvectors:
      if inp.save_evecs == True:
            print("Saving eigenvectors...")
            ino.save_eigenvectors(model=Ham.model, 
                                  sites=Ham.sites, 
                                  pars=Ham.pars, 
                                  BC=Ham.PBC, 
                                  evecs=eigenvectors)

      if inp.plot_evecs==True:
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
      if inp.print_gs_energy==True:
            print("Ground state energy:", min(eigenvalues))
            if Ham.model=="Hubbard":
                  if Ham.pars["sz"]==0 and Ham.pars["N"]==Ham.sites:    #half filling -> exact solution by Lieb & Wu
                        ground_state_exact, err = utils.ground_state_Hubbard_half_filling(t=Ham.pars["t"], U=Ham.pars["U"], N=Ham.sites)
                        print("Ground state energy (extensive part):", ground_state_exact, ". Error:", err)
                        print(f"Ratio of finite-size corrections: {(ground_state_exact-min(eigenvalues))/ground_state_exact*100}%")
      if inp.n_lowest_eigenvalues>1:
            if inp.print_es_energies==True:
                  print("Excited state energies:", eigenvalues)
      if inp.print_gs==True:
            print("Ground state:")
            print(eigenvectors[:,0])
      if inp.print_es==True: 
            print("Excited states:")
            if inp.n_lowest_eigenvalues>1:
                  for i in range(1,inp.n_lowest_eigenvalues):
                        print(eigenvectors[:,i])

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

      if inp.IPR==True:
            IPR = obs.average_IPR(Ham=Ham, evecs=eigenvectors, verbose=inp.verbose)
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
      if inp.dynamics == True:
            print("Calculating dynamics...")
            time_evolved_state = dyn.full_time_evolution(Ham=Ham, 
                                                         evals=eigenvalues, 
                                                         evecs=eigenvectors, 
                                                         initial_state=inp.initial_state, 
                                                         final_time=inp.final_time, 
                                                         dt=inp.dt)
            
            
            if inp.plot_dynamics == True:
                  if Ham.stats=="spinful-fermions":
                        raise NotImplementedError()
                  else:
                        viz.plot_time_evolution_spinless(time_evolved_state=time_evolved_state, 
                                                         Ham=Ham,
                                                         initial_state=inp.initial_state,
                                                         final_time=inp.final_time,
                                                         dt=inp.dt)
                        viz.plot_density_vs_t_spinless(time_evolved_state=time_evolved_state, 
                                                       Ham=Ham, 
                                                       initial_state=inp.initial_state, 
                                                       dt=inp.dt, 
                                                       final_time=inp.final_time)

            if inp.movie_dynamics == True:
                  if Ham.stats=="spinful-fermions":
                        raise NotImplementedError()
                  else:
                        viz.movie_time_evolution_spinless(time_evolved_state=time_evolved_state,
                                                          Ham=Ham,
                                                          initial_state=inp.initial_state,
                                                          final_time=inp.final_time,
                                                          dt=inp.dt)


      ################################################################



      return 











if __name__=="__main__":

      ####################################
      ###########  IMPORTS   #############
      ####################################

      import sys
      import numpy as np
      from numpy import cos, sin, sqrt, arctan, tan, exp

      # CUSTOM modules:
      import input as inp
      # print("input_filename:", input_filename)
      # print("stats:", inp.stats)
      # print("model:", inp.model)
      # print("sites:", inp.sites)
      # print("PBC:", inp.PBC)
      # print("sparse:", inp.sparse)
      # print("Ham_par1:", inp.Ham_par1)
      # print("Ham_par2:", inp.Ham_par2)
      # print("Ham_par3:", inp.Ham_par3)
      # print("Ham_par4:", inp.Ham_par4)
      # print("Ham_par5:", inp.Ham_par5)
      # print("Ham_par6:", inp.Ham_par6)
      # print("Ham_par7:", inp.Ham_par7)
      # print("Ham_par8:", inp.Ham_par8)
      # print("Ham_par9:", inp.Ham_par9)
      # print("Ham_par10:", inp.Ham_par10)
      # print("Ham_par10:", inp.Ham_par10)
      # print("Ham_par10:", inp.Ham_par10)
      # print("n_lowest_eigenvalues:", inp.n_lowest_eigenvalues)
      # print("maxiter_Arnoldi:", inp.maxiter_Arnoldi)
      # print("save_evals:", inp.save_evals)
      # print("compute_evecs:", inp.compute_evecs)
      # print("save_evecs:", inp.save_evecs)
      # print("load_input_parameters:", inp.load_input_parameters)
      # print("dynamics:", inp.dynamics)
      # print("initial_state:", inp.initial_state)
      # print("final_time:", inp.final_time)
      # print("dt:", inp.dt)
      # print("print_gs_energy:", inp.print_gs_energy)
      # print("print_es_energies:", inp.print_es_energies)
      # print("print_gs:", inp.print_gs)
      # print("print_es:", inp.print_es)
      # print("dt:", inp.dt)
      # print("plot_Hamiltonian:", inp.plot_Hamiltonian)
      # print("plot_evals:", inp.plot_evals)
      # print("plot_evecs:", inp.plot_evecs)
      # print("plot_dynamics:", inp.plot_dynamics)
      # print("movie_dynamics:", inp.movie_dynamics)
      # print("verbose:", inp.verbose)

      import glob 
      import hams
      import diag
      import obs
      import utils
      import dynamics as dyn
      import viz
      import input_output as ino
      ####################################



      Ham = main()