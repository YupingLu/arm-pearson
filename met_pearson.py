#!/usr/bin/env python3
# Test code to calculate the pearson correlations on sgpmetE11 2016 data
# Most of the values of tbrg_precip_total is 0, so this var is not included in this version
# Nov 29 2017

'''
met1
[[ 1.         -0.44541473  0.10547848 -0.34833079 -0.3446093 ]
 [-0.44541473  1.         -0.3950509   0.81267319  0.24606413]
 [ 0.10547848 -0.3950509   1.          0.14684473 -0.42979376]
 [-0.34833079  0.81267319  0.14684473  1.          0.01064697]
 [-0.3446093   0.24606413 -0.42979376  0.01064697  1.        ]]
 '''

# Load libs
import netCDF4
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas
from os import listdir
from os.path import isfile, join

# Calculate the days between the given time span
start = datetime.date(2016, 1, 1)
end = datetime.date(2016, 12, 31)
span = end - start

# Assgin sgpmetE11 vars with specific length
sgpmetE11_atmos_pressure     = [None] * (span.days+1) * 1440 # qc_atmos_pressure
sgpmetE11_temp_mean          = [None] * (span.days+1) * 1440 # qc_temp_mean 
sgpmetE11_rh_mean            = [None] * (span.days+1) * 1440 # qc_rh_mean 
sgpmetE11_vapor_pressure_mean= [None] * (span.days+1) * 1440 # qc_vapor_pressure_mean
sgpmetE11_wspd_arith_mean    = [None] * (span.days+1) * 1440 # qc_wspd_arith_mean
#sgpmetE11_tbrg_precip_total  = [None] * (span.days+1) * 1440 # qc_tbrg_precip_total

sgpmetE11 = []
names = ['atmos_pressure', 'temp_mean', 'rh_mean', 'vapor_pressure_mean', 'wspd_arith_mean']
# names = ['atmos_pressure', 'temp_mean', 'rh_mean', 'vapor_pressure_mean', 'wspd_arith_mean', 'tbrg_precip_total']

# Read netcdf files
path = "/Users/yupinglu/OneDrive/project/ARM/data/sgpmetE11"
# path = "/Users/ylk/OneDrive/project/ARM/data/sgpmetE11"
netcdfs = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".cdf")]

for cdf in netcdfs:
    f = netCDF4.Dataset(join(path,cdf))
    # Read variables
    tm                    = f.variables['time']
    atmos_pressure        = f.variables['atmos_pressure']
    temp_mean             = f.variables['temp_mean']
    rh_mean               = f.variables['rh_mean']
    vapor_pressure_mean   = f.variables['vapor_pressure_mean']
    wspd_arith_mean       = f.variables['wspd_arith_mean']
#    tbrg_precip_total     = f.variables['tbrg_precip_total']
    qc_atmos_pressure     = f.variables['qc_atmos_pressure']
    qc_temp_mean          = f.variables['qc_temp_mean']
    qc_rh_mean            = f.variables['qc_rh_mean']
    qc_vapor_pressure_mean= f.variables['qc_vapor_pressure_mean']
    qc_wspd_arith_mean    = f.variables['qc_wspd_arith_mean']
#    qc_tbrg_precip_total  = f.variables['qc_tbrg_precip_total']
    # Convert numeric values of time in the specified units and calendar to datetime objects
    dates = netCDF4.num2date(tm[:], units=tm.units)
    # Read data into different sgpmetE11 vars with filter applied
    for i in range(len(atmos_pressure)):
        if qc_atmos_pressure[i] == 0 and qc_temp_mean[i] == 0 \
        and qc_rh_mean[i] == 0 and qc_vapor_pressure_mean[i] == 0 \
        and qc_wspd_arith_mean[i] == 0:
        #and qc_wspd_arith_mean[i] == 0 and qc_tbrg_precip_total[i] == 0:
            index = int((dates[i] - datetime.datetime(2016, 1, 1, 0, 0)).total_seconds() / 60)
            sgpmetE11_atmos_pressure[index]     = atmos_pressure[i]
            sgpmetE11_temp_mean[index]          = temp_mean[i]
            sgpmetE11_rh_mean[index]            = rh_mean[i]
            sgpmetE11_vapor_pressure_mean[index]= vapor_pressure_mean[i]
            sgpmetE11_wspd_arith_mean[index]    = wspd_arith_mean[i] 
        #    sgpmetE11_tbrg_precip_total[index]  = tbrg_precip_total[i]
    f.close()

# Filter empty values
np_atmos_pressure     = np.asarray([x for x in sgpmetE11_atmos_pressure if x is not None])
np_temp_mean          = np.asarray([x for x in sgpmetE11_temp_mean if x is not None])
np_rh_mean            = np.asarray([x for x in sgpmetE11_rh_mean if x is not None])
np_vapor_pressure_mean= np.asarray([x for x in sgpmetE11_vapor_pressure_mean if x is not None])
np_wspd_arith_mean    = np.asarray([x for x in sgpmetE11_wspd_arith_mean if x is not None])
#np_tbrg_precip_total  = np.asarray([x for x in sgpmetE11_tbrg_precip_total if x is not None])

# Normalize sgpmetE11 vars
if (np_atmos_pressure.max() - np_atmos_pressure.min()) != 0:
    sgpmetE11.append((np_atmos_pressure - np_atmos_pressure.min())                \
        / (np_atmos_pressure.max() - np_atmos_pressure.min()))
else:
    print("atmos_pressure: invalid value encountered in true_divide", file=sys.stderr)

if (np_temp_mean.max() - np_temp_mean.min()) != 0:
    sgpmetE11.append((np_temp_mean - np_temp_mean.min())                          \
        / (np_temp_mean.max() - np_temp_mean.min()))
else:
    print("temp_mean: invalid value encountered in true_divide", file=sys.stderr)

if (np_rh_mean.max() - np_rh_mean.min()) != 0:
    sgpmetE11.append((np_rh_mean - np_rh_mean.min())                              \
        / (np_rh_mean.max() - np_rh_mean.min()))
else:
    print("rh_mean: invalid value encountered in true_divide", file=sys.stderr)

if (np_vapor_pressure_mean.max() - np_vapor_pressure_mean.min()) != 0:
    sgpmetE11.append((np_vapor_pressure_mean - np_vapor_pressure_mean.min())      \
        / (np_vapor_pressure_mean.max() - np_vapor_pressure_mean.min()))
else:
    print("vapor_pressure_mean: invalid value encountered in true_divide", file=sys.stderr)

if (np_wspd_arith_mean.max() - np_wspd_arith_mean.min()) != 0:
    sgpmetE11.append((np_wspd_arith_mean - np_wspd_arith_mean.min())              \
        / (np_wspd_arith_mean.max() - np_wspd_arith_mean.min()))
else:
    print("wspd_arith_mean: invalid value encountered in true_divide", file=sys.stderr)

#if (np_tbrg_precip_total.max() - np_tbrg_precip_total.min()) != 0:
#    sgpmetE11.append((np_tbrg_precip_total - np_tbrg_precip_total.min())          \
#        / (np_tbrg_precip_total.max() - np_tbrg_precip_total.min()))
#else:
#    print("tbrg_precip_total: invalid value encountered in true_divide", file=sys.stderr)

# Calculate pearson correlations between sgpmetE11 vars
mat = np.corrcoef(sgpmetE11)
print(mat)

# Pick another color that is obvious to tell the difference
# Plot correlation matrix
fig= plt.figure()
ax = fig.add_subplot(111)
cax= ax.matshow(mat, vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,mat.shape[0],1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_yticklabels(names)
plt.show()
