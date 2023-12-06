#!/usr/bin/env python
#####################################
#########   IMPORTS   ############
#####################################
import main as m
import ast
#####################################

print("input_filename in input2:", m.input_filename)

############################################################################################
def load_input_parameters(input_filename, target_parameter_name, p_type):

    with open(input_filename) as file:
        for line in file:
            # Remove leading and trailing whitespaces
            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Ignore comments (text after #)
            line = line.split('#')[0].strip()

            # Split the line into parameter and value using '=' as a delimiter
            parts = line.split('=')

            # Ensure that the line contains '=' and has a valid parameter and value
            if len(parts) == 2:
                parameter_name = parts[0].strip()
                parameter_value = ast.literal_eval(parts[1].strip())
            
                if parameter_name==target_parameter_name:
                    #print(parameter_name, ":", parameter_value)
                    
                    if p_type=="str":
                        return str(parameter_value)
                    elif p_type=="float":
                        if type(parameter_value)==list:
                            return [parameter_value[i] for i in range(len(parameter_value))]
                        else:
                            return float(parameter_value)
                    elif p_type=="int":
                        return int(parameter_value)
                    elif p_type=="bool":
                        return parameter_value
############################################################################################


#####################################
#########   PARAMETERS   ############
############################################################################################
# Hamiltonian parameters (the meaning of each parameter depends on which Hamiltonian you are implementing)
########################################################################
stats = load_input_parameters(m.input_filename, target_parameter_name="stats", p_type="str")
model = load_input_parameters(m.input_filename, target_parameter_name="model", p_type="str")
sites = load_input_parameters(m.input_filename, target_parameter_name="sites", p_type="int")
PBC = load_input_parameters(m.input_filename, target_parameter_name="PBC", p_type="bool")
sparse = load_input_parameters(m.input_filename, target_parameter_name="sparse", p_type="bool")
Ham_par1 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par1", p_type="float")
Ham_par2 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par2", p_type="float")
Ham_par3 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par3", p_type="float")
Ham_par4 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par4", p_type="float")
Ham_par5 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par5", p_type="float")
Ham_par6 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par6", p_type="float")
Ham_par7 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par7", p_type="float")
Ham_par8 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par8", p_type="float")
Ham_par9 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par9", p_type="float")
Ham_par10 = load_input_parameters(m.input_filename, target_parameter_name="Ham_par10", p_type="float")
########################################################################
# Parameters for diagonalization
########################################################################
n_lowest_eigenvalues = load_input_parameters(m.input_filename, "n_lowest_eigenvalues", p_type="int")
maxiter_Arnoldi = load_input_parameters(m.input_filename, "maxiter_Arnoldi", p_type="int")      # maximal number of iteration steps in the Arnoldi method for finding eigenvalues
save_evals = load_input_parameters(m.input_filename, "save_evals", p_type="bool")
compute_evecs = load_input_parameters(m.input_filename, "compute_evecs", p_type="bool")
save_evecs = load_input_parameters(m.input_filename, "save_evecs", p_type="bool")
########################################################################
# Parameters for observable calculations
########################################################################
IPR = load_input_parameters(m.input_filename, target_parameter_name="IPR", p_type="bool")
########################################################################
# Parameters for dynamics
########################################################################
dynamics = load_input_parameters(m.input_filename, target_parameter_name="dynamics", p_type="bool")         # Flag for calculating time evolution from initial state
initial_state = load_input_parameters(m.input_filename, target_parameter_name="initial_state", p_type="str")
final_time = load_input_parameters(m.input_filename, target_parameter_name="final_time", p_type="float")
dt = load_input_parameters(m.input_filename, target_parameter_name="dt", p_type="float")
########################################################################
# Parameters for output
########################################################################
print_gs_energy = load_input_parameters(m.input_filename, target_parameter_name="print_gs_energy", p_type="bool")
print_es_energies = load_input_parameters(m.input_filename, target_parameter_name="print_es_energies", p_type="bool")
print_gs = load_input_parameters(m.input_filename, target_parameter_name="print_gs", p_type="bool")
print_es = load_input_parameters(m.input_filename, target_parameter_name="print_es", p_type="bool")
########################################################################
# Parameters for visualization
########################################################################
plot_Hamiltonian = load_input_parameters(m.input_filename, target_parameter_name="plot_Hamiltonian", p_type="bool")
plot_evals = load_input_parameters(m.input_filename, target_parameter_name="plot_evals", p_type="bool")
plot_evecs = load_input_parameters(m.input_filename, target_parameter_name="plot_evecs", p_type="bool")
plot_dynamics = load_input_parameters(m.input_filename, target_parameter_name="plot_dynamics", p_type="bool")
movie_dynamics = load_input_parameters(m.input_filename, target_parameter_name="movie_dynamics", p_type="bool")
########################################################################
# Other parameters
########################################################################
verbose = load_input_parameters(m.input_filename, target_parameter_name="verbose", p_type="bool")
########################################################################