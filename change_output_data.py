"""data.csv
# Time: 2023-06-12 12:11:36.910068
# Project : Calibration
# Experiment : Ar800_90
# Target Name : Ar
# Power (mW) : 50
# Wavelength (nm) : 800
# Pressure (torr) : 1E-5
# Angle (deg) : 0.0
# Note :
# Columns : Time (ns), TDC Count
# Module name : TDC2228A
# Time Resolution (ns) : 0.1518
# Average hit/shot : 0.5570452659132988
# Total Laser shot : 31326
#
8.560000000000000497e+00,0.000000000000000000e+00
8.711800000000000210e+00,0.000000000000000000e+00
8.863599999999999923e+00,0.000000000000000000e+00
9.015399999999999636e+00,0.000000000000000000e+00
9.167200000000001125e+00,0.000000000000000000e+00
"""
# Convert data.csv to data.dat by:
#     Make headers at the bottom of the file
#     convert the second column to int
#     save the file as data.dat

import numpy as np
import os

def read_header(path):
    with open(path) as f:
        lines = f.readlines()
    header_list = []
    for line in lines:
        if line.startswith('#'):
            header_list.append(line)
        else:
            break
    return header_list


# list all (.csv) files in the current director
files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv')]
for f in files:
    # read the file
    data = np.loadtxt(f, delimiter=',')
    # second column to int
    headrs = read_header(f)
    # save the file as .dat
    #Format float to 4 decimal places
    fmt = '%.4f'
    np.savetxt(f[:-4]+'.dat', data, comments='', fmt=fmt, footer="".join(headrs))
