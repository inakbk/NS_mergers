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
file_pf = directory + "pf_" + "aa" + ID_trajectory

# The 0 element is the variable name, 1,2,3 is final ab. different normalizations,
# therefore the time starts at col_start:
col_start = 3
N_data = len(np.genfromtxt(file_aa,skip_header=11,max_rows=1)) - 1 

#---------------------------------------------------------------------
""" #SAME as what can load from pf file (below)
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
"""

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
# Access the matrix as: data_matrix[time_row][prameter_col]
data_matrix = np.genfromtxt(file_pf,skip_header=11)

lsod      = data_matrix[:,0]
Time      = data_matrix[:,1]
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


#-----------------------------------------------------------------------------------------------------
# Plotting the time evolution of physical quantities

#----- T9, Nn, Ye, S -----
"""
fig1, ax1 = plt.subplots(2,2, sharex=True)

ax1[0,0].loglog(Time, T9,'b')
ax1[0,0].axhline(y=1, color='gray', linestyle='--',alpha=0.5)
ax1[0,0].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax1[0,1].loglog(Time, Nn,'r')
ax1[0,1].axhline(y=1e20, color='gray', linestyle='--',alpha=0.5)
ax1[0,1].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax1[1,0].semilogx(Time, Ye,'g')
ax1[1,0].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax1[1,1].semilogx(Time, S,'k')
ax1[1,1].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)

ax1[0,1].set_title(r'ID_trajectory: %s' %ID_trajectory)
ax1[1,0].set_xlabel(r'Time [s]')
ax1[1,1].set_xlabel(r'Time [s]')
ax1[0,0].set_ylabel(r'Temperature $T_9$ [$10^9$ K]')
ax1[0,1].set_ylabel(r'Neutron density $N_n$ [cm$^{-3}$]')
ax1[1,0].set_ylabel(r'Electron fraction $Y_e$')
ax1[1,1].set_ylabel(r'Entropy $S$ [erg/g/K]')
plt.tight_layout()

#----- P, r, v/c, rho -----
fig2, ax2 = plt.subplots(2,2, sharex=True)

ax2[0,0].loglog(Time, P,'b')
ax2[0,0].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax2[0,1].loglog(Time, r,'r')
ax2[0,1].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax2[1,0].semilogx(Time, v/2.998e+10,'g')
ax2[1,0].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax2[1,1].loglog(Time, rho,'k')
ax2[1,1].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)

ax2[0,1].set_title(r'ID_trajectory: %s' %ID_trajectory)
ax2[1,0].set_xlabel(r'Time [s]')
ax2[1,1].set_xlabel(r'Time [s]')
ax2[0,0].set_ylabel(r'Pressure $P$ [erg/cm$^{3}$]')
ax2[0,1].set_ylabel(r'Radius $r$ [cm]')
ax2[1,0].set_ylabel(r'Velocity $v/c$')
ax2[1,1].set_ylabel(r'Density $\rho$ [g/cm$^{3}$]')
plt.tight_layout()
"""

#----- Qs, <A>,... -----
fig3, ax3 = plt.subplots(2,2, sharex=True)

ax3[0,0].loglog(Time, np.abs(Qgn),'b', label=r'abs($Q_{\gamma,n}$)')
ax3[0,0].loglog(Time, Qng,'c--', label=r'$Q_{n,\gamma}$')
ax3[0,0].loglog(Time, Qbeta,'m', label=r'$Q_{\beta}$')
ax3[0,0].loglog(Time, Qfission,'r', label=r'$Q_{fission}$')
ax3[0,0].loglog(Time, Qalpha,'y', label=r'$Q_{\alpha}$')
ax3[0,0].loglog(Time, Qtot,'k--', label=r'$Q_{tot}$')
ax3[0,0].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax3[0,0].legend()
ax3[0,1].semilogx(Time, A_avr,'r', label=r'$\langle A\rangle$')
ax3[0,1].semilogx(Time, Amax,'c', label=r'$A_{max}$')
ax3[0,1].semilogx(Time, Z_avr,'m', label=r'$\langle Z\rangle$')
ax3[0,1].semilogx(Time, Zmax,'y', label=r'$Z_{max}$')
ax3[0,1].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax3[0,1].legend()
ax3[1,0].loglog(Time, np.abs(Qng_gn),'k')
ax3[1,0].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax3[1,1].loglog(Time, lsod,'g')
ax3[1,1].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)

ax3[0,1].set_title(r'ID_trajectory: %s' %ID_trajectory)
ax3[1,0].set_xlabel(r'Time [s]')
ax3[1,1].set_xlabel(r'Time [s]')
ax3[0,0].set_ylabel(r'$Q$ [erg/..]')
ax3[0,1].set_ylabel(r'#')
ax3[1,0].set_ylabel(r'abs($Q_{n,\gamma}+Q_{\gamma,n}$)')
ax3[1,1].set_ylabel(r'lsod')

plt.tight_layout()

#----- T9, Nn, ncap, Sa0 -----
"""
fig4, ax4 = plt.subplots(2,2, sharex=True)

ax4[0,0].loglog(Time, Xn,'b', label=r'Xn')
ax4[0,0].loglog(Time, Xp,'c', label=r'Xp')
ax4[0,0].loglog(Time, Xa,'m', label=r'Xa')
ax4[0,0].loglog(Time, Xheavy,'y', label=r'Xheavy')
ax4[0,0].axhline(y=1, color='gray', linestyle='--',alpha=0.5)
ax4[0,0].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax4[0,0].legend()
ax4[0,1].semilogx(Time, Yh_p,'r', label=r'Yh(i>p)')
ax4[0,1].semilogx(Time, Yh_C,'m', label=r'Yh(i>12C)')
ax4[0,1].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax4[0,1].legend()
ax4[1,0].semilogx(Time, ncap,'g')
ax4[1,0].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)
ax4[1,1].semilogx(Time, Sa0,'k')
ax4[1,1].axvline(x=1e-1, color='gray', linestyle='--',alpha=0.5)

ax4[0,1].set_title('ID_trajectory: %s' %ID_trajectory)
ax4[1,0].set_xlabel('Time [s]')
ax4[1,1].set_xlabel('Time [s]')
ax4[0,0].set_ylabel(r'Xn, Xp, Xa, Xheavy')
ax4[0,1].set_ylabel(r'Yh ')
ax4[1,0].set_ylabel(r'$n_{cap}$')
ax4[1,1].set_ylabel(r'Astrophys.factor $S_a^0$ [MeV]')
plt.tight_layout()


#-----------------------------------------------------------------------------------------------------
# Final abundance in one single plot
fig2, ax2 = plt.subplots()

ax2.semilogy(A_array,mass_frac_fin,'bo--', fillstyle='none', label='Final abundance')
ax2.semilogy(A_array,solar_mass_frac, 'r*', fillstyle='none', label='Solar abundance distribution')

ax2.axis([50,250,1e-6, np.max([np.max(mass_frac_fin),np.max(mass_frac_fin)]) + 0.2])
ax2.set_title('ID_trajectory: %s' %ID_trajectory)
ax2.set_xlabel('Mass number, A')
ax2.set_ylabel('Abundance')
ax2.legend()
"""

plt.tight_layout()
plt.show()

















