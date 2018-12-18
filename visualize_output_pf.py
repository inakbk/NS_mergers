# This script plots the physical quantities of the Rpro output at 
# a given time or evolves the time (animation)

# The output files of the Rpro calc has to be copied over to the directory 
# /Abon

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

ID_merger = "0132511"

directory = "Abon/"
file_aa = directory + "aa" + ID_merger
file_pf = directory + "pf_" + file_aa