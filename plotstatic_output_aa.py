# This script plots the physical quantities of the Rpro output (aa file) at 
# a given time does NOT create animation

# The output files of the Rpro calc has to be copied over to the directory 
# /Abon

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

ID_list = ["0120851", "0125759", "0132511", "0161047", "0308245", "0332105"]
ID_trajectory = ID_list[1]

directory = "Abon/"
file_aa = directory + "aa" + ID_trajectory

# The 0 element is the variable name, 1,2,3 is final ab. different normalizations,
# therefore the time starts at col_start:
col_start = 3
N_data = len(np.genfromtxt(file_aa,skip_header=11,max_rows=1)) - 1 

#---------------------------------------------------------------------
# The upper part of the data file:
data_matrix1 = np.genfromtxt(file_aa,skip_header=11,usecols=range(1,N_data))

# Time evolution (without double data points):
T9     = data_matrix1[0,col_start:-2:2] #using slicing
Nn     = data_matrix1[1,col_start:-2:2]
Sum_m1 = data_matrix1[2,col_start:-2:2]
Time   = data_matrix1[3,col_start:-2:2]
ncap   = data_matrix1[4,col_start:-2:2]

# The last datapoint is lost when use slicing (since len(Time) is odd).
# Adding the last datapoint (which also is the same as the lines before col_start)
T9     = np.append(T9    ,data_matrix1[0,-1]) 
Nn     = np.append(Nn    ,data_matrix1[1,-1])
Sum_m1 = np.append(Sum_m1,data_matrix1[2,-1])
Time   = np.append(Time  ,data_matrix1[3,-1])
ncap   = np.append(ncap  ,data_matrix1[4,-1])

#---------------------------------------------------------------------
# The lower part of the data file with 1 more column than the upper, 
# since A and Solar is included.
# Do not load the time evolution of the abundance.
data_matrix2 = np.genfromtxt(file_aa,skip_header=17,usecols=range(0,5)) 

A_array         = data_matrix2[:,0]
solar_mass_frac = data_matrix2[:,1]

# Different normalizations for final abundance, sum(solar_mass_frac)=1:
# norm_col = 2 : Normalised to same as 3 below? so difficult to tell...
# norm_col = 3 : Normalised to  somewhere close to A=75, the 1st r-process peak
# norm_col = 4 : Normalised to sum(mass_frac_fin)=1 (same as last col. of time evo)
norm_col = 4
mass_frac_fin = data_matrix2[:,norm_col]

#---------------------------------------------------------------------
# Plotting the time evolution of physical quantities

fig1, ax1 = plt.subplots(2,2, sharex=True)

ax1[0,0].loglog(Time, T9,'b')
ax1[0,0].axhline(y=1, color='gray', linestyle='--',alpha=0.5)
ax1[0,1].loglog(Time, Nn,'r')
ax1[0,1].axhline(y=1e20, color='gray', linestyle='--',alpha=0.5)
ax1[1,0].semilogx(Time, ncap,'g')
ax1[1,1].loglog(Time,abs(Sum_m1),'k')

ax1[0,1].set_title('ID_trajectory: %s' %ID_trajectory)
ax1[1,0].set_xlabel('Time [s]')
ax1[1,1].set_xlabel('Time [s]')
ax1[0,0].set_ylabel(r'Temperature $T_9$ [$10^9$ K]')
ax1[0,1].set_ylabel(r'Neutron density $N_n$ [cm$^{-3}$]')
ax1[1,0].set_ylabel(r'$n_{cap}$')
ax1[1,1].set_ylabel(r'abs(SUM - 1)')
plt.tight_layout()

#---------------------------------------------------------------------
# Plotting final abundance in one single plot
fig2, ax2 = plt.subplots()

ax2.semilogy(A_array,mass_frac_fin,'bo--', fillstyle='none', label='Final abundance')
ax2.semilogy(A_array,solar_mass_frac, 'r*', fillstyle='none', label='Solar abundance distribution')

ax2.axis([50,250,1e-6, np.max([np.max(mass_frac_fin),np.max(mass_frac_fin)]) + 0.2])
ax2.set_title('ID_trajectory: %s' %ID_trajectory)
ax2.set_xlabel('Mass number, A')
ax2.set_ylabel('Abundance')
ax2.legend()


#plt.close()

plt.tight_layout()
plt.show()

















