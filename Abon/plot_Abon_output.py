# THIS IS AN EARLY VERSION THE OTHER CODE IS BETTER

# Script to look at the output files of Rpro calculation
# ----
# Plan is to plot:
# -T&rho vs time
# ab vs time (given A)
# solar ab vs time (given A)
# final ab vs A or Z

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

filename = "aa0132511"


#---------------------------------------------------------------------
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
        vid_filename = 'animation_figures/movie_%s.mp4' %plotname
    else:
        vid_filename = 'animation_figures/%s.mp4' %name

    if os.path.isfile(vid_filename):
        os.system( ("rm " + vid_filename) ) 

    os.system("ffmpeg -r 6 -f image2 -start_number 0000002 -i animation_figures/" + plotname + "%06d.png  -vcodec libx264 -s 1920x1080 " + vid_filename)
    #os.system("ffmpeg -start_number 000002 -i col%06d.png video.mp4" )

    print '\nThe movie should now be in the folder animation_figures. \n'

    if play=='yes':
        os.system("open -a vlc " + vid_filename)

    #os.system("rm animation_figures/*.png")
    #print 'All animation_figures/*.png removed  '
#---------------------------------------------------------------------

make_figs = True
make_movie = False

if make_figs:
    T9 =     np.genfromtxt(filename,skip_header=11,max_rows=1)[2:] # the 0 element is the varname, 1 is last column(?), then time start
    Nn =     np.genfromtxt(filename,skip_header=12,max_rows=1)[2:] 
    Sum_m1 = np.genfromtxt(filename,skip_header=13,max_rows=1)[2:] # ?????
    Time =   np.genfromtxt(filename,skip_header=14,max_rows=1)[2:]
    ncap =   np.genfromtxt(filename,skip_header=15,max_rows=1)[2:] 

    N = len(Time)

    A_array =     np.genfromtxt(filename,skip_header=17,usecols=0)
    abund_solar = np.genfromtxt(filename,skip_header=17,usecols=1)
    abund_end   = np.genfromtxt(filename,skip_header=17,usecols=-1)

    #for col in range(2,N):
    for col in range(2,3):
        abund_start = np.genfromtxt(filename,skip_header=17,usecols=col) # WHERE DOES THE TIME START?? Col=4 is same as col=-1...?

        fig1, ax = plt.subplots()

        ax.semilogy(A_array,abund_solar,'s',label='Solar (hvorfor noe 1e-25?')
        ax.semilogy(A_array,abund_end,'*',label='End (last column)')
        ax.semilogy(A_array,abund_start,'o',label='Evolution col=%s' %col)

        ax.axis([0,250,1e-6,1])
        ax.legend(loc='upper right')
        #ax.grid(which='major', linestyle=':', linewidth='0.5', color='grey')
        ax.set_title('%s' %filename)
        ax.set_xlabel('Mass number, A')
        ax.set_ylabel('Abundance or Mass fraction? []')

        plt.tight_layout()
        plt.savefig('animation_figures/col{:06d}.png'.format(col)) 

        #plt.show()
        #plt.close()


    # Two subplots, the axes array is 1-d
    fig2, axarr = plt.subplots(2,2, sharex=True)

    axarr[0,0].loglog(Time, T9,'b')
    axarr[0,1].loglog(Time, Nn,'r')
    axarr[1,0].semilogx(Time, ncap,'g')
    axarr[1,1].semilogx(Time,Sum_m1,'k')

    axarr[0,0].set_title('%s' %filename)
    axarr[1,0].set_xlabel('Time [s]')
    axarr[1,1].set_xlabel('Time [s]')

    axarr[0,0].set_ylabel(r'Temperature $T_9$ [$10^9$ K]')
    axarr[0,1].set_ylabel(r'Neutron density $N_n$ [cm$^{-3}$]')
    axarr[1,0].set_ylabel(r'$n_{cap}$ [??]')
    axarr[1,1].set_ylabel(r'$Sum^{-1}$ [??]')

    # Customize the major grid -->does not work after update python or something
    #axarr[0,0].grid(which='major', linestyle=':', linewidth='0.5', color='grey')
    #axarr[0,1].grid(which='major', linestyle=':', linewidth='0.5', color='grey')
    #axarr[1,0].grid(which='major', linestyle=':', linewidth='0.5', color='grey')
    #axarr[1,1].grid(which='major', linestyle=':', linewidth='0.5', color='grey')

    plt.show()


#---------------------------------------------------------------------

elif make_movie:
    #creating movie, uncoment this line if ffmpeg is not installed:
    create_animation_from_plots(play='yes', plotname='col',name='NS_ab_animation') 












