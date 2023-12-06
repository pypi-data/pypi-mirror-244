#!/usr/bin/env python
############################################################################################
##### This module contains functions to fit data.
############################################################################################

####################################
###########  IMPORTS   #############
####################################
from __future__ import division
from __future__ import print_function
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
####################################


################################
######     SUBROUTINES    ######
################################

#############################################################################
def extrapolate_2d_data(method, data, t_arr, t_extra):
    """
    Extrapolate 2d data (matrix-like).

    Parameters:
    -----------
    method, str: describes which extrapolation method to use.

    data, 3d array of dims [Nx,Ny,Nt]: the data to fit and extrapolate.
    
    t_arr, 1d array of length Nt: the independent variable.

    t_extra, array: the values of the parameter at which the extrapolation should be calculated.


    """

    Ny = np.shape(data)[0]
    Nx = np.shape(data)[1]
    Nt = np.shape(data)[2]


    # Reshape the data to 2D (N*M, T) for interpolation
    reshaped_data = data.reshape(Nx*Ny,Nt)

    # Create interpolation functions for each row in reshaped_data
    if method=="linear":
        interp_functions = [interp1d(t_arr, row, kind='linear', fill_value="extrapolate") for row in reshaped_data]
    elif method=="cubic":
        interp_functions = [interp1d(t_arr, row, kind='cubic', fill_value="extrapolate") for row in reshaped_data]
    elif method=="quintic":    
        interp_functions = [interp1d(t_arr, row, kind='quintic', fill_value="extrapolate") for row in reshaped_data]

    # Extrapolate each row to the new value:
    extrapolated_data_rows = np.array([interp(t_extra) for interp in interp_functions])

    # Reshape the extrapolated data back to 3D
    extrapolated_data = extrapolated_data_rows.reshape(Ny, Nx, len(t_extra))

    return extrapolated_data
#############################################################################









#############################################################################
def test_extrapolation(method, data, t_arr, t_extra, chosen_t):
    """
    This assumes t_extra is just one value.
    """

    Ny = np.shape(data)[0]
    Nx = np.shape(data)[1]
    print("Ny:", Ny)
    print("Nx:", Nx)
    print("data:")
    for t in range(len(t_arr)):
        print(data[:,:,t])
    extrapolated_data = extrapolate_2d_data(method, data, t_arr, [t_extra])


    # Using dictionaries to dynamically create plots:
    n_plots = len(chosen_t) + 1
    dict = {}
    for j in range(n_plots):
        dict["string{0}".format(j)] = "ax"
    
    print(dict)

    X, Y = np.meshgrid(np.linspace(0.0, 1.0, Nx), np.linspace(0.0, 1.0, Ny))
    fig = plt.figure(figsize=(12,8))
    for idx, t in enumerate(chosen_t):

        dict["string{0}".format(idx)] = fig.add_subplot(1, n_plots, idx+1)
        plot = dict["string{0}".format(idx)].pcolormesh(X, Y, data[:,:,t], cmap="inferno", shading="auto")
        plt.colorbar(plot)
        dict["string{0}".format(idx)].set_title(f"t={t_arr[t]}")
    dict["string{0}".format(len(chosen_t))] = fig.add_subplot(1, n_plots, n_plots)
    plot = dict["string{0}".format(len(chosen_t))].pcolormesh(X, Y, extrapolated_data[:,:,0], cmap="inferno", shading="auto")
    dict["string{0}".format(len(chosen_t))].set_title(f"t={t_extra} (extrapolated)")
    plt.colorbar(plot)
    plt.tight_layout()
    plt.show()
    plt.close()

#############################################################################
    

#############################################################################
def generate_test_data():
    """
    
    """

    Nx = 30
    Ny = 31
    Nt = 50

    x_arr = np.linspace(0.0, 1.0, Nx)
    y_arr = np.linspace(0.0, 1.0, Ny)
    t_arr = np.linspace(0.0, 1.0, Nt)


    data = np.zeros(shape=(Ny, Nx, Nt))

    for x_idx, x in enumerate(x_arr):
        for y_idx, y in enumerate(y_arr):
            for t_idx, t in enumerate(t_arr):
                data[y_idx,x_idx,t_idx] = x**2*t-np.sqrt(y)*t**3

    return data, t_arr

#############################################################################