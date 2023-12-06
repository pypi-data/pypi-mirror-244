#!/usr/bin/env python

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


######################################################################################
class Hamiltonian:
    """
    Methods
    ----------
     

    Parameters
    ----------
    

    Examples
    --------
  
    """
  
  
    def __init__(self, 
                 input,
                 **kwargs):
        
        """
        Parameters:
        ----------
        input, instance of Input class

        """
        
        self.model = input.model
        self.stats = input.stats
        self.sites = input.sites
        self.PBC = input.PBC
        if self.stats=="bosons" or self.stats=="spinless-fermions" or self.stats=="anyons" or self.stats=="spin-0.5":
            self.Hilbert_dim = 2**self.sites
        elif self.stats=="spinful-fermions":
            self.Hilbert_dim = 4**self.sites
        else:
            spin = int(self.stats[5:])
            self.Hilbert_dim = input.spin_dim(spin, input.sites)    # not defined!
        self.sparse = input.sparse
        self.get_parameters(input)

        #self.plot_flag = kwargs.get("plot_flag", True)
        self.input_checks(input)

        if self.sparse==True:
            self.rows, self.cols, self.mat_els = self.load_Hamiltonian_sparse(input)
        else:
            raise NotImplementedError
            self.matrix = self.load_Hamiltonian()

        #########################################

    ######################################################################################

    ######################################################################################
    def input_checks(self,
                     input):
        if self.model=="staggered-Heisenberg" and self.sites%2==1:
            raise NotImplementedError("Staggered Heisenberg model for odd number of sites not implemented!")
        

        if input.n_lowest_eigenvalues > self.Hilbert_dim:
            raise ArithmeticError(f"The number of lowest eigenvalues {input.n_lowest_eigenvalues} should be less (or equal) than the Hilbert space dimension {self.Hilbert_dim}!")
        
        if self.model=="staggered-Heisenberg" and self.pars["sz"] is not None and input.plot_evecs == True:
            raise NotImplementedError(f"Displaying eigenvectors for {self.model} presently requires calculation of all the sz spin sectors!")

    ######################################################################################

    ######################################################################################
    def load_Hamiltonian_sparse(self,
                                input):
        """
        Creates and stores the matrix elements of the given Hamiltonian.

        Parameters:
        -----------
        All through self

        Returns:
        --------
        (rows, cols, mat_el), where
        rows (list of ints): row index of non-zero matrix elements
        cols (list of ints): column index of non-zero matrix elements
        mat_el (list of floats): value of non-zero matrix elements

        """

        # Empty lists for sparse Hamiltonian
        rows = []
        cols = []
        mat_els = []

        ######################################################################################################################################
        if self.model=="transverse-Ising":
            self.sector = None
            
            bonds = self.get_bonds()

            # Run through all the spin configurations
            for state in range(self.Hilbert_dim):

                # Apply Ising coupling:
                ising_diagonal = 0
                for bond in bonds:

                    # parallel Ising bonds have energy +J, antiparallel Ising bonds have energy -J:
                    if self.get_site_value(state, bond[0]) == self.get_site_value(state, bond[1]):
                        ising_diagonal += self.pars["J"]
                    else:
                        ising_diagonal -= self.pars["J"]
                
                # Store data:    
                rows.append(state)
                cols.append(state)
                mat_els.append(ising_diagonal)

                # Apply transverse field
                for site in range(self.sites):

                    # The states are coupled (and corresponding Hamiltonian element is nonzero) 
                    # only if they can be mapped onto each other via a spin flip,
                    # e.g.: 1110111 <-> 1111111.
                    # This can be encoded with XOR operator (^ in python):
                    # 119 = 1110111 ^ 0001000 = 8 ==> 1111111 = 127

                    flipped_state = state ^ (1 << site) # "1 << site" will put a unique one in the binary representation of the state at the given site.
                    rows.append(flipped_state)
                    cols.append(state)
                    mat_els.append(self.pars["hx"])
        
            # Add empty matrix element in the last row and column (if it's not nonempty)
            # otherwise the sparse matrix diagonalizer will think the dimension is smaller
            if (self.Hilbert_dim - 1) not in rows and (self.Hilbert_dim - 1) not in cols:
                rows.append(self.Hilbert_dim - 1)
                cols.append(self.Hilbert_dim - 1)
                mat_els.append(0)  
        ######################################################################################################################################



        ######################################################################################################################################
        elif self.model=="staggered-Heisenberg":

            if self.pars["sz"] is not None: # Only calculate things for one sz-sector:
                sz_list = [int(self.pars["sz"])]
                self.sector = self.pars["sz"]
            else:   # Calculate all sz-sectors:
                sz_list = range(-self.sites//2, self.sites // 2 + self.sites % 2 + 1)
                self.sector = None
            #print(sz_list)

            # Generate basis states in lexicographic order:
            self.basis_states = []
            for sz in sz_list:  

                # check if sz is valid
                assert (sz <= (self.sites // 2 + self.sites % 2)) and (sz >= -self.sites//2)

                self.basis_states = np.concatenate((self.basis_states,self.generate_basis_states_lex(sz)))

                if input.verbose==True:
                    print("basis states:", self.basis_states)

            # Assemble Hamiltonian action per sz-sector:
            for sz in sz_list:
            
                if input.verbose == True:
                    print(f"Working on sz={sz} sector...")

                # Define chain lattice
                bonds = self.get_bonds()

                # Run through all spin configurations with fixed total sz
                for state in self.basis_states:

                    # Apply diagonal Ising bonds
                    diagonal = 0
                    for bond in bonds:
                        if self.get_site_value(state, bond[0]) == self.get_site_value(state, bond[1]):
                            diagonal += self.pars["J"]/4
                        else:
                            diagonal -= self.pars["J"]/4

                    # Apply diagonal staggered Sz field
                    for site in range(0, self.sites, 2):
                        diagonal += self.pars["hs"]*(2*self.get_site_value(state, site) - 1)
                        diagonal -= self.pars["hs"]*(2*self.get_site_value(state, site+1) - 1)

                    rows.append(state)
                    cols.append(state)
                    mat_els.append(diagonal)

                    if input.verbose==True:
                        print("basis state:", state)

                    # Apply exchange interaction
                    for bond in bonds:
                        if input.verbose==True:
                            print("bond:", bond)
                        flipmask = (1 << bond[0]) | (1 << bond[1])  # This gives two ones at the positions where the spins should be flipped
                        if self.get_site_value(state, bond[0]) != self.get_site_value(state, bond[1]):
                            new_state = state ^ flipmask
                            if input.verbose==True:
                                print("new state:", new_state)
                            #new_state_index = basis_states.index(new_state)

                            rows.append(state)
                            cols.append(new_state)
                            mat_els.append(self.pars["J"]/2)

            # Add empty matrix element in the last row and column (if it's not nonempty)
            # otherwise the sparse matrix diagonalizer will think the dimension is smaller
            if self.pars["sz"] is None:
                if (self.Hilbert_dim - 1) not in rows and (self.Hilbert_dim - 1) not in cols:
                    rows.append(self.Hilbert_dim - 1)
                    cols.append(self.Hilbert_dim - 1)
                    mat_els.append(0)
            else:
                if (self.sector_dim - 1) not in rows and (self.sector_dim - 1) not in cols: 
                    rows.append(self.sector_dim - 1)
                    cols.append(self.sector_dim - 1)
                    mat_els.append(0)
        ######################################################################################################################################



        ######################################################################################################################################
        elif self.model=="Hubbard":
            if self.pars["N"] is not None and self.pars["sz"] is not None: # Only calculate things for one N_up and N_down-sector:

                N = self.pars["N"]
                sz = self.pars["sz"]
                Nup = int(N/2.0 + sz)       # (Nup - Ndown) = 2sz
                Ndown = int(N/2.0 - sz)     # Nup + Ndown = N
                Nup_list = [Nup]
                Ndown_list = [Ndown]
                print("Nup_list", Nup_list)
                print("Ndown_list", Ndown_list)
  
                self.Nup_sector_dim = utils.binomial(self.sites, Nup)
                self.Ndown_sector_dim = utils.binomial(self.sites, Ndown)
                self.Nup_sector = Nup
                self.Ndown_sector = Ndown
                self.sector_dim = self.Nup_sector_dim*self.Ndown_sector_dim
                self.sector = (Nup, Ndown)

            else:   # Calculate all N-particle sectors:
                Nup_list = range(0, self.sites, 1)
                Ndown_list = range(0, self.sites, 1)
                self.sector = None
                self.sector_dim = self.Hilbert_dim
                self.Nup_sector_dim = None
                self.Ndown_sector_dim = None
                self.Nup_sector = None
                self.Ndown_sector = None

                raise NotImplementedError()
            
            # Generate basis states in lexicographic order:
            self.basis_states_up = []
            self.basis_states_down = []
            for Nup in Nup_list:
                # check if Nup is valid
                assert (Nup <= self.sites) and (Nup >= 0)
                # Append basis states for current spin up sector:
                self.basis_states_up += self.generate_basis_states_lex(Nup)
                if input.verbose==True:
                    print("basis states spin up:")
                    for state in self.basis_states_up:
                        print("state:", bin(state), "lexicographic index:", state, "sector index:", utils.lexRank(np.binary_repr(state, width=self.sites))[0])
            for Ndown in Ndown_list:  
                # check if Ndown is valid
                assert (Ndown <= self.sites) and (Ndown >= 0)
                # Append basis states for current sector:
                self.basis_states_down += self.generate_basis_states_lex(Ndown)
                if input.verbose==True:
                    print("basis states spin down:")
                    for state in self.basis_states_down:
                        print("state:", bin(state), "lexicographic index:", state, "sector index:", utils.lexRank(np.binary_repr(state, width=self.sites))[0])
  
            # Assemble Hamiltonian action per N-particle sector:
            for Nup in Nup_list:
                for Ndown in Ndown_list:
            
                    if input.verbose == True:
                        print(f"Working on (Nup,Ndown)=({Nup},{Ndown}) sector...")
                    
                    bonds = self.get_bonds()

                    # Run through all the spin up and spin down configurations:
                    for state_up in self.basis_states_up:
                        for state_down in self.basis_states_down:

                            # Preparing indices for state of spin ups, state of spin downs, and tensor product:
                            state_up_idx, _ = utils.lexRank(np.binary_repr(state_up, width=self.sites))
                            state_down_idx, _ = utils.lexRank(np.binary_repr(state_down, width=self.sites))
                            tot_states_up = utils.binomial(self.sites, Nup)
                            tensor_state_idx = state_down_idx*tot_states_up + state_up_idx
                
                            ############################################
                            # on-site potential:
                            ############################################
                            if input.verbose==True:
                                print("Assembling on-site potential part...")

                            # Count the nonzero spin-ups and spin-downs,
                            # multiply w/ chemical potential
                            mu = self.pars["mu"]*(state_up.bit_count() + state_down.bit_count())
                            ############################################

                            ############################################
                            # on-site interaction:
                            ############################################
                            if input.verbose==True:
                                print("Assembling nn interaction part...")
                                
                            # Count all common 1's in state_up and state_down,
                            # corresponding to double occupancy, then multiply w/ U:
                            os_int = self.pars["U"]*(state_up & state_down).bit_count()
                            ############################################

                            if self.Nup_sector is not None and self.Ndown_sector is not None: # Only calculate things for one N-sector:
                        
                                rows.append(tensor_state_idx)
                                cols.append(tensor_state_idx)
                                mat_els.append(mu + os_int)

                            else:   # Calculate all N-particle sectors:
                                raise NotImplementedError()

                            ############################################
                            # hopping:
                            ############################################
                            if input.verbose==True:
                                print("Assembling hopping part...")

                            for bond in bonds:
                                if input.verbose==True:
                                    print("bond:", bond)
                        
                                flipmask = (1 << bond[0]) | (1 << bond[1])  # This gives two ones at the positions where the hopping takes place
                                
                                # Hopping on up-sector:
                                if self.get_site_value(state_up, bond[0]) != self.get_site_value(state_up, bond[1]):
                                    new_state_up = state_up ^ flipmask    # Flip the values of the two sites affected by the hopping
                                    if input.verbose==True:
                                        print("new state up:", new_state_up)

                                    if self.Nup_sector is not None and self.Ndown_sector is not None: # Only calculate things for one N-sector:
                                        
                                        # Get ordered lexicographic index for new states after hopping and corresponding index for the tensor product:
                                        new_state_up_idx, _ = utils.lexRank(np.binary_repr(new_state_up, width=self.sites))
                                        new_tensor_state_idx = state_down_idx*tot_states_up + new_state_up_idx

                                        rows.append(tensor_state_idx)
                                        cols.append(new_tensor_state_idx)
                                        mat_els.append(self.pars["t"])

                                # Hopping on down-sector:
                                if self.get_site_value(state_down, bond[0]) != self.get_site_value(state_down, bond[1]):
                                    new_state_down = state_down ^ flipmask    # Flip the values of the two sites affected by the hopping
                                    if input.verbose==True:
                                        print("new state down:", new_state_down)

                                    if self.Nup_sector is not None and self.Ndown_sector is not None: # Only calculate things for one N-sector:
                                        
                                        # Get ordered lexicographic index for new states after hopping and corresponding index for the tensor product:
                                        new_state_down_idx, _ = utils.lexRank(np.binary_repr(new_state_down, width=self.sites))
                                        new_tensor_state_idx = new_state_down_idx*tot_states_up + state_up_idx

                                        rows.append(tensor_state_idx)
                                        cols.append(new_tensor_state_idx)
                                        mat_els.append(self.pars["t"])

                                    else:   # Calculate all N-particle sectors:
                                        raise NotImplementedError()

            # Add empty matrix element in the last row and column (if it's not nonempty)
            # otherwise the sparse matrix diagonalizer will think the dimension is smaller
            if self.pars["N"] is None and self.pars["sz"] is None:
                if (self.Hilbert_dim - 1) not in rows and (self.Hilbert_dim - 1) not in cols:
                    rows.append(self.Hilbert_dim - 1)
                    cols.append(self.Hilbert_dim - 1)
                    mat_els.append(0)
            else:
                if (self.Nup_sector_dim*self.Ndown_sector_dim - 1) not in rows and (self.Nup_sector_dim*self.Ndown_sector_dim - 1) not in cols: 
                    rows.append(self.Nup_sector_dim*self.Ndown_sector_dim - 1)
                    cols.append(self.Nup_sector_dim*self.Ndown_sector_dim - 1)
                    mat_els.append(0)
        ######################################################################################################################################


        ######################################################################################################################################
        elif self.model=="dipolar-Aubry-Andre":

            if self.pars["N"] is not None: # Only calculate things for one N-sector:
                N_list = [int(self.pars["N"])]
                self.sector_dim = utils.binomial(self.sites, int(self.pars["N"]))
                self.sector = int(self.pars["N"])
            else:   # Calculate all N-particle sectors:
                N_list = range(0, self.sites, 1)
                self.sector_dim = self.Hilbert_dim
                self.sector = None

            # Generate basis states in lexicographic order:
            self.basis_states = []
            for N in N_list:

                # check if N is valid
                assert (N <= self.sites) and (N >= 0)

                # Append basis states for current sector:
                self.basis_states += self.generate_basis_states_lex(N)

                if input.verbose==True:
                    print("basis states:")
                    for state in self.basis_states:
                        print("state:", bin(state), "lexicographic index:", state, "sector index:", utils.lexRank(np.binary_repr(state, width=self.sites))[0])
                
            # Assemble Hamiltonian action per N-particle sector:
            for N in N_list:
            
                if input.verbose == True:
                    print(f"Working on N={N} sector...")
                    
                bonds = self.get_bonds()

                # Run through all the fermionic configurations:
                for state in self.basis_states:
                
                    ############################################
                    # on-site potential:
                    ############################################
                    if input.verbose==True:
                        print("Assembling on-site quasiperiodic potential part...")

                    pot=0
                    for site in range(self.sites):
                        if input.verbose==True:
                            print("site:", site)
                        
                        # check whether current site is occupied or empty in current state.
                        # If it's occupied (=1), add the on-site potential for that site:
                        if self.get_site_value(state, site):
                            pot += self.pars["Delta"]*np.cos(2*np.pi*self.pars["beta"]*(site+1) + self.pars["phi"])
                    ############################################


                    ############################################
                    # interactions:
                    ############################################
                    if input.verbose==True:
                        print("Assembling nn interaction part...")

                    eta = self.pars["eta"]

                    bond_dict = {}
                    for d in range(1,len(eta)+1):
                        bond_dict["bond_"+str(d)] = [(site, site+d) for site in range(self.sites-d)]
                    # TODO: generalize this to get_bonds() function

                    
                    for key in bond_dict:
                        bonds = bond_dict[key]
                        d = int(key[-1])
                        
                        inter=0
                        for bond in bonds:
                            if input.verbose==True:
                                print("bond:", bond)

                            # check whether current site and next site are both occupied.
                            # If they are, add the nearest-neighbor interaction:
                            if self.get_site_value(state, bond[0]) == 1 and self.get_site_value(state, bond[1]) == 1:
                                inter += eta[d-1]
                    ############################################

                    if self.pars["N"] is not None: # Only calculate things for one N-sector:
                        
                        state_idx, _ = utils.lexRank(np.binary_repr(state, width=self.sites))
                        rows.append(state_idx)
                        cols.append(state_idx)
                        mat_els.append(pot + inter)

                    else:   # Calculate all N-particle sectors:
                        state_str = np.binary_repr(state, width=self.sites)
                        _, state_idx = utils.lexRank(state_str)
                        rows.append(state_idx)
                        cols.append(state_idx)
                        mat_els.append(pot + inter)

                    ############################################
                    # hopping:
                    ############################################
                    if input.verbose==True:
                        print("Assembling hopping part...")

                    for bond in bonds:
                        if input.verbose==True:
                            print("bond:", bond)
                        
                        flipmask = (1 << bond[0]) | (1 << bond[1])  # This gives two ones at the positions where the hopping takes place
                        if self.get_site_value(state, bond[0]) != self.get_site_value(state, bond[1]):
                            new_state = state ^ flipmask    # Flip the values of the two sites affected by the hopping
                            if input.verbose==True:
                                print("new state:", new_state)

                            if self.pars["N"] is not None: # Only calculate things for one N-sector:
                                state_idx, _ = utils.lexRank(np.binary_repr(state, width=self.sites))
                                new_state_idx, _ = utils.lexRank(np.binary_repr(new_state, width=self.sites))

                                rows.append(state_idx)
                                cols.append(new_state_idx)
                                mat_els.append(self.pars["t"])

                            else:   # Calculate all N-particle sectors:
                                _, state_idx = utils.lexRank(np.binary_repr(state, width=self.sites))
                                _, new_state_idx = utils.lexRank(np.binary_repr(new_state, width=self.sites))
                            
                                rows.append(state_idx)
                                cols.append(new_state_idx)
                                mat_els.append(self.pars["t"])

            # Add empty matrix element in the last row and column (if it's not nonempty)
            # otherwise the sparse matrix diagonalizer will think the dimension is smaller
            if self.pars["N"] is None:
                if (self.Hilbert_dim - 1) not in rows and (self.Hilbert_dim - 1) not in cols:
                    rows.append(self.Hilbert_dim - 1)
                    cols.append(self.Hilbert_dim - 1)
                    mat_els.append(0)
            else:
                if (self.sector_dim - 1) not in rows and (self.sector_dim - 1) not in cols: 
                    rows.append(self.sector_dim - 1)
                    cols.append(self.sector_dim - 1)
                    mat_els.append(0)
        
                    ############################################

        
        if input.verbose == True:
            print("rows:", rows)
            print("cols:", cols)
            print("matrix elements:", mat_els)

        return rows, cols, mat_els

    ######################################################################################


    ######################################################################################
    def get_site_value(self, state, site):
        """
        Gets the spin value (spins) or occupation (fermions) at a given site.

        Notes:
        ------
        * The position of the site in the binary representation if from the RIGHT.
        
        * The site indices start from ZERO.
        
        e.g. value of site 3 in |10100101> is 0.
        e.g. value of site 2 in |10100101> is 1.


        """ 
        
        # >> is bitwise right shift operators e.g. 14 >> 1 means 14=00001110 --> 00000111=7
        return (state >> site) & 1
    ######################################################################################


    ######################################################################################
    def get_bonds(self):
            
        # Define chain lattice
        if self.PBC:
            bonds = [(site, (site+1)%self.sites) for site in range(self.sites)]
        else:
            bonds = [(site, site+1) for site in range(self.sites-1)]

        return bonds
    ######################################################################################


    ######################################################################################
    # Functions to create lexicographic basis
    def first_state_lex(self, L, sz):
        """ 
        Returns first state of Hilbert space in lexicographic order for fermionic systems.

        Parameters:
        -----------
        L, int: number of sites.
        sz, int: total spin sz (spins) or total number of particles (fermions).

        Notes:
        ------
        * The function works for both fermions and spin 1/2's, with the mapping:
          - spin up --> occupied site (1)
          - spin down --> empty site (0)
          - total spin sz --> total number of particles N

        """
        if self.stats == "spin-0.5":
            n = L//2 + sz
        elif self.stats == "spinless-fermions" or self.stats == "spinful-fermions":
            n = sz
        else:
            raise IOError("Lexicographic order is only defined for spin 1/2's and fermions at present!")
        return (1 << n) - 1
    ######################################################################################

    ######################################################################################
    def next_state_lex(self, state):
        """
        Returns the next state of Hilbert space for spin-1/2's or fermions in lexicographic order.

        Notes:
        -----
        This function implements a nice trick for spin 1/2 and fermions only,
        see http://graphics.stanford.edu/~seander/bithacks.html
        #NextBitPermutation for details.

        """

        t = (state | (state - 1)) + 1
        return t | ((((t & -t) // (state & -state)) >> 1) - 1)
    ######################################################################################

    ######################################################################################
    def last_state_lex(self, L, sz):
        """
        Returns the last state of the Hilbert space in lexicographic order.

        Notes:
        ------
        * The function works for both fermions and spin 1/2's, with the mapping:
          - spin up --> occupied site (1)
          - spin down --> empty site (0)
          - total spin sz --> total number of particles N

        """
        if self.stats == "spin-0.5":
            n = L//2 + sz
        elif self.stats == "spinless-fermions" or self.stats == "spinful-fermions":
            n = sz
        else:
            raise IOError("Lexicographic order is only defined for spin 1/2's and fermions at present!")
        return ((1 << n) - 1) << (L - n)
    ######################################################################################

    

    ######################################################################################
    def generate_basis_states_lex(self, sz):
        """
        Returns a lexicographic list of all basis state state of the Hilbert space.

        Notes:
        ------
        * The function works for both fermions and spin 1/2's, with the mapping:
          - spin up --> occupied site (1)
          - spin down --> empty site (0)
          - total spin sz --> total number of particles N

        """

        # Create list of states with fixed N
        basis_states = []
        state = self.first_state_lex(self.sites, sz)
        basis_states.append(state)
        end_state = self.last_state_lex(self.sites, sz)
        while state < end_state:
            state = self.next_state_lex(state)
            basis_states.append(state)
        #basis_states.append(end_state)

        return basis_states
    ######################################################################################


    ######################################################################################
    def get_parameters(self,
                       input):
        
        if self.model == "transverse-Ising":
            J = input.Ham_par1
            hx = input.Ham_par2
            pars = {"J": J,
                         "hx": hx}
            
        elif self.model == "staggered-Heisenberg":
            J = input.Ham_par1
            hs = input.Ham_par2
            sz = input.Ham_par3
            self.pars = {"J": J,
                         "hs": hs,
                         "sz": sz}
        
        elif self.model == "dipolar-Aubry-Andre":
            N = input.Ham_par1
            t = input.Ham_par2
            Delta = input.Ham_par3
            beta = input.Ham_par4
            phi = input.Ham_par5
            eta = input.Ham_par6

            pars = {"N": N,
                         "t": t,
                         "Delta": Delta,
                         "beta": beta,
                         "phi": phi,
                         "eta": eta}
            
        elif self.model == "Hubbard":
            sz = input.Ham_par1
            N = input.Ham_par2
            mu = input.Ham_par3
            t = input.Ham_par4
            U = input.Ham_par5

            pars = {"sz": sz,
                         "N": N,
                         "mu": mu,
                         "t": t,
                         "U": U}

        # Sort dictionary:  (needed for saving/loading files properly)
        par_keys = list(pars.keys())
        par_keys.sort()
        sorted_pars = {i: pars[i] for i in par_keys}

        self.pars = sorted_pars

        return

    ######################################################################################





