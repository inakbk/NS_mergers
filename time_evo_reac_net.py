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
N_data = 768

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
# The lower part of the data file with 1 more column than the upper, 
# since A and Solar is included
data_matrix2 = np.genfromtxt(file_aa,skip_header=17,usecols=range(0,N_data+1)) 

A_array         = data_matrix2[:,0]
solar_mass_frac = data_matrix2[:,1]
# Different normalizations for each A, shape=(359, 3) 
mass_frac_norms = data_matrix2[:,2:5] # mass_frac_norms[A,time_col]
# The time evolved mass fraction (including double data points)
mass_frac_data  = data_matrix2[:,5:-1] # mass_frac_data[A,time_col]


#-----
# Now, when we plot we dont want the "double" data points,
# we use numpy's slicing array[start:stop:step]

# First test to see that the upper part of the data has the same values
# in the double datapoint (true for all except for Sum_m1)

#print T9[0:-2:2] - T9[1:-1:2]
#print Nn[0:-2:2] - Nn[1:-1:2]
#print Sum_m1[0:-2:2] - Sum_m1[1:-1:2] #!!!
#print Time[0:-2:2] - Time[1:-1:2]
#print ncap[0:-2:2] - ncap[1:-1:2]
#-----

# Remove double data points before plot:

T9     = T9[0:-2:2]
Nn     = Nn[0:-2:2]
Sum_m1 = Sum_m1[0:-2:2] # !!!
Time   = Time[0:-2:2]
ncap   = ncap[0:-2:2]

mass_frac_fin = mass_frac_data[:,1:-1:2]
mass_frac_evo = mass_frac_data[:,0:-2:2]

#-----
# PLOT EVERYTHING HERE


#plt.loglog(Time,mass_frac_fin[100,:])

#plt.show()




