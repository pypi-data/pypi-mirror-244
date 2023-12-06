#!/usr/bin/env python
##########################################################################################
# This python program initializes the input file.
###########################################################################################

####################################
###########  IMPORTS   #############
####################################
import shutil
import os
####################################

def copy_template_file():
      package_directory = os.path.dirname(__file__)
      templates_directory = os.path.join(package_directory, 'templates')
      template_path = os.path.join(templates_directory, 'input.dat')
    
      if not os.path.exists(templates_directory):
            print(f"Error: The 'templates' directory does not exist in {package_directory}.")
            return

      current_dir = os.getcwd()
      destination_path = os.path.join(current_dir, 'input.dat')

      shutil.copy(template_path, destination_path)
      print(f"Template input file copied to: {destination_path}")


if __name__ == "__main__":
    copy_template_file()