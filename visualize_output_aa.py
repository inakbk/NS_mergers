# This script plots the physical quantities of the Rpro output (aa file) at 
# a given time or evolves the time (animation)

# The output files of the Rpro calc has to be copied over to the directory 
# /Abon

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

ID_trajectory = "0132511"

#---------------------------------------------------------------------
def evolve_time_saveplot(Time,A_array,solar_mass_frac,mass_frac_evo,mass_frac_fin):
    # Loop over abundance and save plots.

    #for i in range(len(Time)):
    for i in range(2):
        fig0, ax = plt.subplots()

        ax.semilogy(A_array,solar_mass_frac,'r*', fillstyle='none',label='Solar abundance distribution')
        ax.semilogy(A_array,mass_frac_evo[:,i],'go--', fillstyle='none',label='Evolution: mass_frac_evo')
        ax.semilogy(A_array,mass_frac_fin[:,i],'bo--', fillstyle='none',label='Evolution: mass_frac_fin')

        ax.axis([0,250,1e-6,1])
        ax.legend(loc='upper right')
        ax.set_title('Trajectory: %s, time: %gs' %(ID_trajectory,Time[i]))
        ax.set_xlabel('Mass number, A')
        ax.set_ylabel('Abundance')

        plt.tight_layout()
        #plt.savefig('Abon/animation_figures/time_evo_{:06d}.png'.format(i+1)) 
        plt.savefig('Abon/time_evo_{:06d}.png'.format(i+1)) 
        plt.close()

    print "Done. All .png files are now found in /Abon/animation_figures/"

def create_animation_from_plots(plotname='test2', name='', play='yes'):
    # Function adapted from MSU project V17

    # Creates an animation / movie from png files in the folder "animation_figures". 
    # The figures must have file names with 7digits counting up with the ending "_test2.png"
    # The movie is played unless keyword play='no' 
    # If there already exist a movie with the same filename in the folder the old movie is 
    # deleted before the new movie is made. When the movie is made all of the png files in 
    # the folder is deleted (this will happen even if there is an error). 

    # This function needs the package ffmpeg installed. If this package is not installed 
    # uncomment the line using this function and look at the plots instead. 

    # ------
    # Parameters

    #   plotname : optional, string
    #           the name following the 7digit number in the filename of the 
    #           png files in the folder  (without .png)
    #   name : optional, string
    #           the name of the mp4 movie (without .mp4)
    #   play : optional, string
    #           if anything but 'yes' is given the movie will not be played by vlc

    # Returns (no return statement)
    # ------

    if name == '':
        vid_filename = 'Abon/animation_figures/movie_%s.mp4' %plotname
    else:
        vid_filename = 'Abon/animation_figures/%s.mp4' %name

    if os.path.isfile(vid_filename):
        os.system( ("rm " + vid_filename) ) 

    os.system("ffmpeg -r 6 -f image2 -start_number 0000002 -i Abon/animation_figures/" + plotname + "%06d.png  -vcodec libx264 -s 1920x1080 " + vid_filename)

    print '\nThe movie should now be in the folder animation_figures. \n'

    if play=='yes':
        os.system("open -a vlc " + vid_filename)
#---------------------------------------------------------------------

directory = "Abon/"
file_aa = directory + "aa" + ID_trajectory

# The 0 element is the variable name, 1,2,3 is final ab. different normalizations,
# therefore the time starts at col_start:
col_start = 3
N_data = 768

#---------------------------------------------------------------------
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

#---------------------------------------------------------------------
# The lower part of the data file with 1 more column than the upper, 
# since A and Solar is included
data_matrix2 = np.genfromtxt(file_aa,skip_header=17,usecols=range(0,N_data+1)) 

A_array         = data_matrix2[:,0]
solar_mass_frac = data_matrix2[:,1]
# Different normalizations for each A, shape=(359, 3) 
mass_frac_norms = data_matrix2[:,2:5] # mass_frac_norms[A,time_col]
# The time evolved mass fraction (including double data points)
mass_frac_data  = data_matrix2[:,5:-1] # mass_frac_data[A,time_col]


#---------------------------------------------------------------------
# Now, when we plot we dont want the "double" data points,
# we use numpy's slicing array[start:stop:step]

# First test to see that the upper part of the data has the same values
# in the double datapoint (true for all except for Sum_m1)

#print T9[0:-2:2] - T9[1:-1:2]
#print Nn[0:-2:2] - Nn[1:-1:2]
#print Sum_m1[0:-2:2] - Sum_m1[1:-1:2] #!!!
#print Time[0:-2:2] - Time[1:-1:2]
#print ncap[0:-2:2] - ncap[1:-1:2]

#---------------------------------------------------------------------
# Remove double data points before plot:

T9     = T9[0:-2:2]
Nn     = Nn[0:-2:2]
Sum_m1 = Sum_m1[0:-2:2] # !!!
Time   = Time[0:-2:2]
ncap   = ncap[0:-2:2]

mass_frac_fin = mass_frac_data[:,1:-1:2]
mass_frac_evo = mass_frac_data[:,0:-2:2]

#---------------------------------------------------------------------
# Plotting the time evolution of physical quantities
fig1, ax1 = plt.subplots(2,2, sharex=True)

ax1[0,0].loglog(Time, T9,'b')
ax1[0,1].loglog(Time, Nn,'r')
ax1[1,0].semilogx(Time, ncap,'g')
ax1[1,1].semilogx(Time,Sum_m1,'k')

ax1[0,1].set_title('Merger: %s' %ID_trajectory)
ax1[1,0].set_xlabel('Time [s]')
ax1[1,1].set_xlabel('Time [s]')
ax1[0,0].set_ylabel(r'Temperature $T_9$ [$10^9$ K]')
ax1[0,1].set_ylabel(r'Neutron density $N_n$ [cm$^{-3}$]')
ax1[1,0].set_ylabel(r'$n_{cap}$')
ax1[1,1].set_ylabel(r'SUM - 1')

# Plotting final abundance in one single plot
fig2, ax2 = plt.subplots()

ax2.semilogy(A_array,mass_frac_norms[:,2],'go--', fillstyle='none', label='Final abundance')
ax2.semilogy(A_array,solar_mass_frac, 'r*', fillstyle='none', label='Solar abundance distribution')
ax2.axis([0,250,1e-6,1])
ax2.set_xlabel('Mass number, A')
ax2.set_ylabel('Abundance')
ax2.legend()

#plt.close()

#plt.tight_layout()
#plt.show()

#---------------------------------------------------------------------
# Plotting all time steps of the abundance:
#evolve_time_saveplot(Time,A_array,solar_mass_frac,mass_frac_evo,mass_frac_fin)

# Make the movie:
#create_animation_from_plots(play='yes', plotname='time_evo_',name='ab_anim_%s' %ID_trajectory)




















