#!/usr/bin/env python
#####################################
#########   IMPORTS   ############
#####################################
import ast
#####################################

#print("input_filename in input2:", input_filename)

class Input():
    """
    Methods
    ----------
     

    Parameters
    ----------
    

    Examples
    --------
  
    """

    def __init__(self, 
                 input_filename,
                 **kwargs):
        
        """
        Parameters:
        ----------
        input_filename, str: the path to the input file (usually input.dat).

        """

        #####################################
        #########   PARAMETERS   ############
        ############################################################################################
        # Hamiltonian parameters (the meaning of each parameter depends on which Hamiltonian you are implementing)
        ########################################################################
        self.input_filename = input_filename
        self.stats = self.load_input_parameters(input_filename=input_filename, target_parameter_name="stats", p_type="str")
        self.model = self.load_input_parameters(input_filename=input_filename, target_parameter_name="model", p_type="str")
        self.sites = self.load_input_parameters(input_filename=input_filename, target_parameter_name="sites", p_type="int")
        self.PBC = self.load_input_parameters(input_filename=input_filename, target_parameter_name="PBC", p_type="bool")
        self.sparse = self.load_input_parameters(input_filename=input_filename, target_parameter_name="sparse", p_type="bool")
        self.Ham_par1 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par1", p_type="float")
        self.Ham_par2 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par2", p_type="float")
        self.Ham_par3 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par3", p_type="float")
        self.Ham_par4 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par4", p_type="float")
        self.Ham_par5 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par5", p_type="float")
        self.Ham_par6 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par6", p_type="float")
        self.Ham_par7 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par7", p_type="float")
        self.Ham_par8 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par8", p_type="float")
        self.Ham_par9 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par9", p_type="float")
        self.Ham_par10 = self.load_input_parameters(input_filename=input_filename, target_parameter_name="Ham_par10", p_type="float")
        ########################################################################
        # Parameters for diagonalization
        ########################################################################
        self.n_lowest_eigenvalues = self.load_input_parameters(input_filename=input_filename, target_parameter_name="n_lowest_eigenvalues", p_type="int")
        self.maxiter_Arnoldi = self.load_input_parameters(input_filename=input_filename, target_parameter_name="maxiter_Arnoldi", p_type="int")      # maximal number of iteration steps in the Arnoldi method for finding eigenvalues
        self.save_evals = self.load_input_parameters(input_filename=input_filename, target_parameter_name="save_evals", p_type="bool")
        self.compute_evecs = self.load_input_parameters(input_filename=input_filename, target_parameter_name="compute_evecs", p_type="bool")
        self.save_evecs = self.load_input_parameters(input_filename=input_filename, target_parameter_name="save_evecs", p_type="bool")
        ########################################################################
        # Parameters for observable calculations
        ########################################################################
        self.IPR = self.load_input_parameters(input_filename=input_filename, target_parameter_name="IPR", p_type="bool")
        ########################################################################
        # Parameters for dynamics
        ########################################################################
        self.dynamics = self.load_input_parameters(input_filename=input_filename, target_parameter_name="dynamics", p_type="bool")         # Flag for calculating time evolution from initial state
        self.initial_state = self.load_input_parameters(input_filename=input_filename, target_parameter_name="initial_state", p_type="str")
        self.final_time = self.load_input_parameters(input_filename=input_filename, target_parameter_name="final_time", p_type="float")
        self.dt = self.load_input_parameters(input_filename=input_filename, target_parameter_name="dt", p_type="float")
        ########################################################################
        # Parameters for output
        ########################################################################
        self.print_gs_energy = self.load_input_parameters(input_filename=input_filename, target_parameter_name="print_gs_energy", p_type="bool")
        self.print_es_energies = self.load_input_parameters(input_filename=input_filename, target_parameter_name="print_es_energies", p_type="bool")
        self.print_gs = self.load_input_parameters(input_filename=input_filename, target_parameter_name="print_gs", p_type="bool")
        self.print_es = self.load_input_parameters(input_filename=input_filename, target_parameter_name="print_es", p_type="bool")
        ########################################################################
        # Parameters for visualization
        ########################################################################
        self.plot_Hamiltonian = self.load_input_parameters(input_filename=input_filename, target_parameter_name="plot_Hamiltonian", p_type="bool")
        self.plot_evals = self.load_input_parameters(input_filename=input_filename, target_parameter_name="plot_evals", p_type="bool")
        self.plot_evecs = self.load_input_parameters(input_filename=input_filename, target_parameter_name="plot_evecs", p_type="bool")
        self.plot_dynamics = self.load_input_parameters(input_filename=input_filename, target_parameter_name="plot_dynamics", p_type="bool")
        self.movie_dynamics = self.load_input_parameters(input_filename=input_filename, target_parameter_name="movie_dynamics", p_type="bool")
        ########################################################################
        # Other parameters
        ########################################################################
        self.verbose = self.load_input_parameters(input_filename=input_filename, target_parameter_name="verbose", p_type="bool")
        ########################################################################


    ############################################################################################
    def load_input_parameters(self, 
                              input_filename, 
                              target_parameter_name, 
                              p_type):
        """
        This function loads the input parameters from the input file (usually input.dat) into the instance of the Input class.
        
        """
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


