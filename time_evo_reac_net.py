# This script plots the physical quantities of the Rpro output at 
# a given time or evolves the time (animation)

# The output files of the Rpro calc is copied over to the directory 
# /Abon

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

ID_merger = "0132511"

directory = "Abon/"
file_aa = directory + "aa" + ID_merger
file_pf = directory + "pf_" + file_aa


# The 0 element is the variable name, 1,2,3 is final ab. different normalizations,
# therefore the time starts at col_start:
col_start = 3
N_data = 767

# The upper part of the data file:
data_matrix1 = np.genfromtxt(file_aa,skip_header=11,usecols=range(1,N_data))

# Time evolution (including double data points):
T9     = data_matrix1[0,col_start:]
Nn     = data_matrix1[1,col_start:]
Sum_m1 = data_matrix1[2,col_start:]
Time   = data_matrix1[3,col_start:]
ncap   = data_matrix1[4,col_start:]

# Different normalizations of the final evolution (arrays with 3 values):
T9_norm     = data_matrix1[0,0:col_start]
Nn_norm     = data_matrix1[1,0:col_start]
Sum_m1_norm = data_matrix1[2,0:col_start]
Time_norm   = data_matrix1[3,0:col_start]
ncap_norm   = data_matrix1[4,0:col_start]

#-----
# The lower part of the data file with 2 more columns than the upper, 
# since A and Solar is included
data_matrix2 = np.genfromtxt(file_aa,skip_header=17,usecols=range(0,N_data+2)) 

A_array         = data_matrix2[:,0]
solar_mass_frac = data_matrix2[:,1]
# Different normalizations for each A, shape=(359, 3) 
mass_frac_norms = data_matrix2[:,2:5] # mass_frac_norms[A,time_col]
# The time evolved mass fraction (including double data points)
mass_frac_data  = data_matrix2[:,5:-1] # mass_frac_data[A,time_col]


#-----
# Now, sort away the "double" data points










