# This script plots the physical quantities of the Rpro output (pf file) at 
# a given time or evolves the time (animation)

# The output files of the Rpro calc has to be copied over to the directory 
# /Abon

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

ID_merger = "0132511"

directory = "Abon/"
file_pf = directory + "pf_" + "aa" + ID_merger

# The file is structured as one parameter per column and the time evolves
# for each row. The parameters are found in the column:
#parameter_names = np.genfromtxt(file_pf,skip_header=10,max_rows=1,dtype='str')
#print parameter_names
#print len(parameter_names) # = 31 parameters


# Access the matrix as: data_matrix[time_row][prameter_col]
data_matrix = np.genfromtxt(file_pf,skip_header=11)

lsod = data_matrix[:,0]
time = data_matrix[:,1]
dt   = data_matrix[:,2]
T9   = data_matrix[:,3]
rho  = data_matrix[:,4]
Nn   = data_matrix[:,5]
Xn   = data_matrix[:,6]
#..
Ye   = data_matrix[:,9]
#..
Qtot = data_matrix[:,12]
Qng  = data_matrix[:,13]
Qgn  = data_matrix[:,14]
Qplus= data_matrix[:,15]
Qbeta= data_matrix[:,16]
Qfis = data_matrix[:,17]
Qalp = data_matrix[:,18]
#..
r    = data_matrix[:,-2]
v    = data_matrix[:,-1]

plt.loglog(time,Qplus)

plt.show()



