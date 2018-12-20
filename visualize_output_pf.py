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

#---------------------------------------------------------------------
# Access the matrix as: data_matrix[time_row][prameter_col]
data_matrix = np.genfromtxt(file_pf,skip_header=11)

lsod      = data_matrix[:,0]
time      = data_matrix[:,1]
dt        = data_matrix[:,2]
T9        = data_matrix[:,3]
rho       = data_matrix[:,4]
Nn        = data_matrix[:,5]
Xn        = data_matrix[:,6]
Xp        = data_matrix[:,7]
Xa        = data_matrix[:,8]
Ye        = data_matrix[:,9]
Yh_p      = data_matrix[:,10]
Yh_C      = data_matrix[:,11]
Qtot      = data_matrix[:,12]
Qng       = data_matrix[:,13]
Qgn       = data_matrix[:,14]
Qng_gn    = data_matrix[:,15]
Qbeta     = data_matrix[:,16]
Qfission  = data_matrix[:,17]
Qalpha    = data_matrix[:,18]
Sa0       = data_matrix[:,19]
Xheavy    = data_matrix[:,20]
one_mXtot = data_matrix[:,21]
ncap      = data_matrix[:,22]
ncap      = data_matrix[:,22]
Z_avr     = data_matrix[:,23]
A_avr     = data_matrix[:,24]
Amax      = data_matrix[:,25]
Zmax      = data_matrix[:,26]
S         = data_matrix[:,27]
P         = data_matrix[:,28]
r         = data_matrix[:,29]
v         = data_matrix[:,30]

#---------------------------------------------------------------------
def simple_plot(x,y,leg_name,x_name,y_name,xscale='linear',yscale='linear'):
    fig1, ax1 = plt.subplots()

    ax1.plot(x,y, 'b*--', fillstyle='none', label='%s' %leg_name)
    ax1.set_xlabel('%s' %x_name)
    ax1.set_ylabel('%s' %y_name)
    ax1.legend()

    ax1.set_xscale('%s' %xscale)
    ax1.set_yscale('%s' %yscale)

    plt.tight_layout()
    plt.show()


#---------------------------------------------------------------------

#simple_plot(x=time,y=v,leg_name='',x_name='time',y_name='v',xscale='log')

simple_plot(x=time,y=v,leg_name='',x_name='time',y_name='',xscale='log')







