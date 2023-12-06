#!/usr/bin/env python
############################################################################################
##### This module implements symmetry transformations.
############################################################################################


####################################
###########  IMPORTS   #############
####################################
from itertools import permutations, combinations
import itertools
import numpy as np
####################################

def generate_binaries(N, M):
    binary_digits = ['0'] * (N - M) + ['1'] * M
    binary_permutations = set(permutations(binary_digits))
    sorted_binaries = sorted([''.join(permutation) for permutation in binary_permutations])
    return sorted_binaries

def map_to_integers(N, M):
    binary_strings = generate_binaries(N, M)
    integer_mapping = {binary_string: index for index, binary_string in enumerate(binary_strings)}
    return integer_mapping


def nested_loops():
      
    parameters = ["eta", "Delta", "N"]
    start_values = {"eta": -2, "Delta": 0.0, "N": 4}
    end_values = {"eta": 2, "Delta": 10.0, "N": 8}
    n_points = {"eta": 11, "Delta": 11, "N": 3}

    
    par_lists = {}
    args = []
    for par in parameters:
        if par=="Delta" or par=="N":
            par_lists[par] = np.linspace(start_values[par], end_values[par], n_points[par])
        elif par=="eta":
            par_lists[par] = 10**(np.linspace(start_values[par], end_values[par], n_points[par]))

        args.append(par_lists[par])

    shape = tuple(n_points[parameters[i]] for i in range(len(parameters)))
    print(shape)
    IPR_arr = np.zeros(shape=shape)
    
    for idx, combination in enumerated_product(*args):

    # Generating output string and dictionary for current parameter selection 
    # (merged with static parameters)
        print(idx,combination)

        shape = tuple(n_points[parameters[i]] for i in range(len(parameters)))     
        IPR_arr[idx]=np.sum(idx)
        
    print(IPR_arr)

    return


######################################################################################
def enumerated_product(*args):
    yield from zip(itertools.product(*(range(len(x)) for x in args)), itertools.product(*args))
######################################################################################









##############################################################
def main():
    # Example: Mapping binaries with N=4 and M=2 to integers
    N = 5
    M = 3
    result = map_to_integers(N, M)
    print(result)

    nested_loops()


##############################################################




if __name__=="__main__":
      main()

      for ns in ["101", "011", "110"]:

        
         
        print(ns,
            np.sum(
                [int(alpha)*2**(idx) for idx, alpha in enumerate(ns)]
                )
            )
        
        #########

