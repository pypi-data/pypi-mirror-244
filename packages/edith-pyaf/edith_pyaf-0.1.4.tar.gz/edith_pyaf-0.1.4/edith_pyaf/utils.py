#!/usr/bin/env python
############################################################################################
##### This file contains utility routines.
############################################################################################

####################################
###########  IMPORTS   #############
####################################
from __future__ import division
from __future__ import print_function
import numpy as np
import scipy as sp
import itertools as it
import os
####################################


################################
######     SUBROUTINES    ######
################################
######################################################################################
def spin_dim(spin, sites):
    """
    Returns the Hilbert space dimension of the spin problem with the given spin size.

    """
    spin_size = len(np.arange(-spin,spin+1),1)
    dim = spin_size**sites

    return dim

######################################################################################


######################################################################################
def get_full_Hamiltonian(H_sparse):
    """
    Builds full Hamiltonian matrix from sparse representation.

    Parameters:
    ----------
    H_sparse, instance of class Hamiltonian: the Hamiltonian object.
    
    """

    # Get data from object:
    rows = H_sparse.rows
    cols = H_sparse.cols
    mat_els = H_sparse.mat_els
    dim = np.amax(rows)+1

    # Check whether columns = rows:
    assert len(cols) == len(rows)

    # Initialize array:
    Ham = np.zeros(shape=(dim,dim))

    # Loop over all non-zero elements and save them into the full array:
    for i in range(len(rows)):
        Ham[rows[i],cols[i]] = mat_els[i]

    return Ham
######################################################################################

######################################################################################
def get_parameters_from_dict(pars):
    
    par_keys=[]
    par_vals=[]
    
    for par in pars:
        par_keys.append(par)
        par_vals.append(pars[par])

    return par_keys, par_vals
######################################################################################


######################################################################################
def calculate_overlap(state1, state2):
    """
    """
    
    return np.vdot(state1, state2)
######################################################################################

######################################################################################
def convert_state_from_str_to_arr(state_str):
    """
    
    Notes:
    ------

    At present, only states that are not written as a superposition are accepted, e.g.:

    "01100100110"
    "20401032001"
    etc.
    
    """

    l = len(state_str)
    state = np.zeros(l)

    for c, idx in enumerate(state_str):
        state[idx] = int(c)

    # normalize:
    state /= np.sum(np.abs(state)**2)

    return state
######################################################################################

######################################################################################
def convert_state_from_bin_to_vec(state_str, basis_dim, sector):
    """
    
    Notes:
    ------

    At present, only states that are not written as a superposition are accepted, e.g.:

    "01100100110"
    "20401032001"
    etc.
    
    """

    if sector is not None:
        rank, _ = lexRank(state_str)   # determine index (rank) in local sector
    
    elif sector is None:
        _, rank = lexRank(state_str)   # determine index (rank) in full Hilbert space
    
    vec = np.zeros(basis_dim)     # initialize vector
    vec[rank] = 1               # fill vector at position corresponding to the rank
        
    return vec
######################################################################################

######################################################################################
def get_state_population_spinless(Ham, state, **kwargs):
    """
    Get the population at each site for the given state for spinless fermions or spin 1/2's.

    Notes:
    ------
    This is equivalent to performing <psi| n_i |psi> for every particle number operator at each site i.
    
    e.g. N=2 |psi> = [1.2, 0.1, -0.1, 0.5] means
             |psi> = 1.2 |00> + 0.1 |01> - 0.1 |10> + 0.5 |11>

             n1 |psi> = 0.1 |01> + 0.5 |11>   -->  <n1> = <psi| n1 |psi> = |0.1|^2 + |0.5|^2
             n2 |psi> = -0.1 |01> + 0.5 |11>  -->  <n2> = <psi| n2 |psi> = |-0.1|^2 + |0.5|^2

             --> total spin profile is [<n1>, <n2>] = [0.26, 0.26].

    """
    # TODO: This was originally thought for the full Hilbert space, but has to be modified 
    # to allow for states that only reside on a sector of the Hilbert space


    stats = Ham.stats 

    
    if Ham.sector_dim==None:    # state of the full Hamiltonian
        # TODO: rename variables here, they are confusing...

        d = len(state)      # Hilbert space dimension
        L = int(np.log2(d)) # sites

        # Initialize the amplitudes:
        evec = np.zeros(L, dtype=np.complex_)

        # Loop over all states in the Hilbert space, extract the eigenvector weight,
        # and multiply the corresponding sites with the weight:
        for i in range(d):
            bin = np.binary_repr(i, width=L)
            #print("binary ", bin)
            weight = np.abs(state[i])**2
            for idx, c in enumerate(bin):
                #print(c)
                if stats == "spin-0.5":
                    evec[idx] += (int(c)-0.5)*weight    # spins
                elif stats == "fermions":
                    evec[idx] += int(c)*weight    # fermions


    else:   # fixed particle number sector N, smaller dimension of full Hilbert space

        N = int(Ham.sector)
        # Get basis for sector:
        sector_basis = Ham.generate_basis_states_lex(N)

        # Initialize the amplitudes:
        evec = np.zeros(Ham.sites, dtype=np.complex_)

        for b in sector_basis:

            bin = np.binary_repr(b, width=Ham.sites)
            idx_b, _ = lexRank(bin)   # index of basis state in the given sector
            weight = np.abs(state[idx_b])**2     # weight that the state has in the basis state b

            for idx, c in enumerate(bin):   # Loop over every element (site) of the basis state b
                #print(c)
                if stats == "spin-0.5":
                    evec[idx] += (int(c)-0.5)*weight    # spins
                elif stats == "spinless-fermions":
                    evec[idx] += int(c)*weight    # fermions

    return evec

######################################################################################

######################################################################################
def get_state_population_spinful(state, Ham, **kwargs):
    """
    Get the population at each site for the given state for spinful fermions.

    Notes:
    ------
    Given state |psi> written in tensor basis:
    1) loop over its elements with index k; the elements are coefficients multiplying the tensor basis: 
        e.g. for Nup=1, Ndown=1, sites=2:
            |psi> = c1*(|01>x|01>) + c2*(|01>x|10>) + c3*(|10>x|01>) + c4*(|10>x|10>)
        where the first ket is for spin up and the second ket is for spin down,
        and |psi> is saved as a vector (c1, c2, c3, c4). This is the input.

    2) from index k of tensor product, get lexicographic indices of spin up and spin down components,
       i.e. k = i*Nsup + j, where Ns_up is the *number* of total states with Nup up spins in the given
       number of sites [ Nsup = (sites choose Nup)]. This is given by

       i = k // Nsup (integer division)
       j = k % Nsup (remainder)

       Note that i and j are indices of the basis states *ordered wrt the lexicographic convention per sector*.

    3) Now we know which indices i,j to use for a given k, but we still need to get the corresponding
       basis vectors in the spin-up and spin-down bases. Because writing the inverse function of lexRank
       would be complicated, we can instead re-generate the basis states for each spin sector together with
       their rank, and sort the states according to their rank. That way, indices i and j from 2) will point 
       to the right states. This step can be done at the very beginning, before starting the k-loop.

    4) Get the binary representation of each state of each spin component (e.g. 13 = 8 + 4 + 1 = |1101>). 
       Then loop over each site in the binary string and sum the spin weight (squared) at every site.
       e.g. for Nup=1, Ndown=1, sites=2 (see point 1) above):

       vec_up = (tot weight at site 1, tot weight at site 2) = (|c1|^2*1 + |c2|^2*1 + |c3|^2*0 + |c4|^2*0, |c1|^2*0 + |c2|^2*0 + |c3|^2*1 + |c4|^2*1)
       vec_down = (tot weight at site 1, tot weight at site 2) = (|c1|^2*1 + |c2|^2*0 + |c3|^2*1 + |c4|^2*0, |c1|^2*0 + |c2|^2*1 + |c3|^2*0 + |c4|^2*1)

    Recall that the sites are counted from the RIGHT, 
    e.g. |123> means there are 3 particles on site 1, 2 particles on site 2, and 1 particle on site 3.

    """

    if Ham.Nup_sector_dim==None and Ham.Ndown_sector_dim==None:    # state of the full Hamiltonian
        raise NotImplementedError()

    else:   # given particle number sectors Nup and Ndown, smaller dimension of full Hilbert space

        Nup = Ham.Nup_sector
        Ndown = Ham.Ndown_sector

        # Get lexicographically ordered basis for each sector:
        sector_basis_up = Ham.generate_basis_states_lex(Nup)
        lex_idx_up = []
        for state_up in sector_basis_up:
            lex_idx_up.append(lexRank(np.binary_repr(state_up, width=Ham.sites))[0])
        sector_basis_up = [x for x, _ in sorted(zip(sector_basis_up,lex_idx_up))] 
        
        sector_basis_down = Ham.generate_basis_states_lex(Ndown)
        lex_idx_down = []
        for state_down in sector_basis_down:
            lex_idx_down.append(lexRank(np.binary_repr(state_down, width=Ham.sites))[0])
        sector_basis_down = [x for x, _ in sorted(zip(sector_basis_down,lex_idx_down))] 

        print(f"sector_basis_up: {sector_basis_up}")
        print(f"sector_basis_down: {sector_basis_down}")

        # Now the two bases for up and down basis states are ordered according to 
        # their lexicographic index for the sector. We can then access the correct state
        # by sector_basis_down[idx], where idx comes directly from decoupling the tensor index
        # into spin up index and spin down index.

        tot_states_up = binomial(Ham.sites, Nup)

        # Initialize the amplitudes:
        vec_up = np.zeros(Ham.sites)
        vec_down = np.zeros(Ham.sites)

        for idx, c in enumerate(state): #idx is the index of the tensor product state, c is its coefficient
            
            # Get the lexicographic index of the state of each spin component
            idx_down = idx // tot_states_up       
            idx_up = idx % tot_states_up

            #print(f"idx_up: {idx_up}")
            #print(f"idx_down: {idx_down}")

            # Get the corresponding state:
            state_up = sector_basis_up[idx_up]
            state_down = sector_basis_down[idx_down]

            #print(state_up)
            #print(state_down)
            
            # Rewrite the state in binary format: (e.g. 13 = 8 + 4 + 1 = |1101>)
            bin_up = np.binary_repr(state_up, width=Ham.sites)
            bin_down = np.binary_repr(state_down, width=Ham.sites)

            # Extract the value of the basis vector at each site and add it to
            # the vector representation for both spin up and spin down:
            for idx in range(Ham.sites):      
                vec_up[idx] += np.abs(c)**2*int(bin_up[idx])    
                vec_down[idx] += np.abs(c)**2*int(bin_down[idx])    

    return vec_up, vec_down

######################################################################################


######################################################################################
def binomial(n,k):
    """
    Calculates the binomial coefficient n chooses k.

    """
    if n < 0 or k < 0 or k > n: 
        return 0
    b = 1
    for i in range(k): 
        b = b*(n-i)/(i+1)
    return int(b)
######################################################################################

######################################################################################
def combo_rank(n,S):
    """
    Given a combination S with n equal elements, calculates the corresponding rank (index) 
    in a lexicographic ordering.

    """
    k = len(S)
    if k == 0 or k == n: 
        return 0
    
    j = S[0]
    if k == 1: 
        return j
    
    S = [x-1 for x in S]
    if not j: 
        return combo_rank(n-1,S[1:])
    
    return binomial(n-1,k-1)+combo_rank(n-1,S)
######################################################################################

######################################################################################
def combos_with_reps(X,k):
    """
    Given a list of elements X, calculate all possible combinations of k elements. 

    """
    n = len(X)
    if k < 0 or k > n: 
        return []
    if not k: 
        return [[]]
    if k == n: 
        return [X]
    
    c = [X[:1] + S for S in combos_with_reps(X[1:],k-1)] + combos_with_reps(X[1:],k)

    return c 
######################################################################################

######################################################################################
def combos_without_reps(X,k):
    """
    Given a list of elements X, calculate all possible combinations of k elements. 

    """
    c = combos_with_reps(X,k)
    c.sort()
    cwr =  list((k for k,_ in it.groupby(c)))

    return cwr
######################################################################################


######################################################################################
def fac(n):
    """
    Calculates factorial of n.

    """
    if n == 0 or n == 1:
        return 1
	
    return n * fac(n - 1)
######################################################################################


######################################################################################
def generate_all_binaries(n):
    
    if n==1:
        return ["0", "1"]
    
    else:
        bins = generate_all_binaries(n-1)
        
    new_bins = []   
    for b in bins:
        new_bins.append(b+"0")
        new_bins.append(b+"1")

    return new_bins
######################################################################################



######################################################################################
# Python program to find all the possible combinations of
# k-bit numbers with n-bits set where 1 <= n <= k
 
 
# Function to find all combinations k-bit numbers with
# n-bits set where 1 <= n <= k
def findBitCombinations(k):
    
    # maximum allowed value of k
    assert (k < 16)
    
    # DP lookup table
    DP = [[[] for _ in range(16)] for _ in range(16)]
 
    bins = []
    # DP[k][0] will store all k-bit numbers
    # with 0 bits set (All bits are 0's)
    str = ""
    for len in range(k+1):
        DP[len][0].append(str)
        str += "0"
 
    # fill DP lookup table in bottom-up manner
    # DP[k][n] will store all k-bit numbers
    # with n-bits set
    for len in range(1, k+1):
        for n in range(1, len+1):
            # prefix 0 to all combinations of length len-1
            # with n ones
            for str in DP[len-1][n]:
                DP[len][n].append("0" + str)
 
            # prefix 1 to all combinations of length len-1
            # with n-1 ones
            for str in DP[len-1][n-1]:
                DP[len][n].append("1" + str)
 
    # print all k-bit binary strings with
    # n-bit set
    for n in range(k+1):
        for str in DP[k][n]:
            #print(str, end=" ")
            bins.append(str)
        #print()

    return bins
######################################################################################


######################################################################################
#Function to calculate 
#rank of the String.
def lexRank(s, verbose=False):
    """
    Calculates lexicographic rank of a string of 0s and 1s.
     
    Notes:
    ------ 
    This gives both the relative (fixed numbers of 0s and 1s for given length N) and the
    absolute (increasing number of 1s for a given length N) rank, e.g. for N=4:

    | string      | relative | absolute |
    --------------|----------|----------|
    |0000>        |    0     |    0     |
    |0001>        |    0     |    1     |
    |0010>        |    1     |    2     |
    |0100>        |    2     |    3     |
    |1000>        |    3     |    4     |
    |0011>        |    0     |    5     |
    |0101>        |    1     |    6     |
    |0110>        |    2     |    7     |
    |1001>        |    3     |    8     |
    |1010>        |    4     |    9     |
    |1100>        |    5     |    10    |
    |0111>        |    0     |    11    |
    |1011>        |    1     |    12    |
    |1101>        |    2     |    13    |
    |1110>        |    3     |    14    |
    |1111>        |    0     |    15    |
    
    Note that the number of combinations of k 1's in a string of length N is the 
    binomial coefficient, (n chooses k).
    
    """

    # Get string length:
    n = len(s)

    # Get number of 1's:
    n1=0
    for j in s:
        if j=="1":
            n1+=1
    
    # Initialize relative rank to 0.
    rel_rank = 0
    
    # Loop over each element of the string, and check how many elements 
    # TO ITS RIGHT are smaller:
    for i in range(n):
        if verbose==True:
            print(f"Character at position {i}: {s[i]}")
        less_than = 0
        for j in range(i + 1, n):
            if int(s[i]) > int(s[j]): 
                less_than += 1
        if verbose==True:
            print(f"Number of characters with smaller order: {less_than}")

        # Count the number of characters (0's and 1's) to the right of the current element (included):      
        d_count = [0] * 2
        for j in range(i, n):
            d_count[int(s[j])] += 1
        if verbose==True:
            print(f"There are {d_count[0]} 0's and {d_count[1]} 1's from position {i} onwards.")

        # Calculate the total number of permutations of those elements
        # (the 0's permute among themselves, the 1's among themselves).
        # This is needed to avoid overcounting.
        d_fac = 1
        for ele in d_count:
            d_fac *= fac(ele)
        
        # Calculate the number of possible arrangements of the elements to the right
        rel_rank += (fac(n - i - 1) * less_than) // d_fac
        if verbose==True:
            print("\n")

    if verbose==True:
        print(rel_rank)

    abs_rank = 0
    for i in range(n1):
        abs_rank += binomial(n,i)

    abs_rank += rel_rank

    return rel_rank, abs_rank
######################################################################################


######################################################################################
def find_string_from_rank(rank, length):
    result = ''
    total_combinations = 2 ** length

    if rank >= total_combinations:
        return "Rank exceeds the total number of combinations for the given length."

    for i in range(length - 1, -1, -1):
        divisor = 2 ** i
        if rank >= divisor:
            result += '1'
            rank -= divisor
        else:
            result += '0'

    return result

######################################################################################

from math import comb
######################################################################################

def find_string_from_rank2(rank, num_zeros, num_ones):
    total_length = num_zeros + num_ones
    result = []

    for i in range(total_length):
        zeros_remaining = num_zeros
        combinations_without_zero = comb(zeros_remaining + num_ones - 1, num_ones - 1)

        if rank < combinations_without_zero:
            result.append('0')
            num_zeros -= 1
        else:
            result.append('1')
            rank -= combinations_without_zero
            num_ones -= 1

    return ''.join(result)
######################################################################################


######################################################################################
def ground_state_Hubbard_half_filling(t, U, N):
    """
    Evaluates the formula for the ground state energy of the 1D Hubbard model at 
    half filling by Lieb and Wu.

    References:
    -----------
    * E. H. Lieb and F. Y. Wu, 
      Absence of Mott transition in an exact solution of the short-range one-band model in one dimension, 
      Phys. Rev. Lett. 20, 1445 (1968).

    """
    def integrand(x):
        return sp.special.j0(x)*sp.special.j1(x)/(x*(1+np.exp(x*U/(2*t))))
    
    I, err = sp.integrate.quad(integrand,0,100)
    E = -4*t*N*I
    err = -4*t*N*err

    return E, err
######################################################################################

######################################################################################
def enumerated_product(*args):
    yield from zip(it.product(*(range(len(x)) for x in args)), it.product(*args))
######################################################################################

######################################################################################
def check_dir(dir_name):
    """
    Creates the given folder if missing.

    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    return
######################################################################################


