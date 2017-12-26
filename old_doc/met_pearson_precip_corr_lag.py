#!/usr/bin/env python3
# Test code to calculate the pearson correlations on sgpmetE11 2016 data
# Nov 29 2017

'''
met4 with precip_corr one day lag
[[ 1.         -0.34481061  0.26271951 -0.24105371 -0.32935386 -0.13252701]
 [-0.34481061  1.         -0.31812254  0.7955031  -0.16430328  0.22782522]
 [ 0.26271951 -0.31812254  1.          0.26061945 -0.20327143 -0.12360976]
 [-0.24105371  0.7955031   0.26061945  1.         -0.2534877   0.17495389]
 [-0.32935386 -0.16430328 -0.20327143 -0.2534877   1.         -0.00563535]
 [-0.13252701  0.22782522 -0.12360976  0.17495389 -0.00563535  1.        ]]
 '''

# Load libs
import netCDF4
import numpy as np
import datetime
#import matplotlib.pyplot as plt
#import pandas
from os import listdir
from os.path import isfile, join

# Calculate the days between the given time span
start = datetime.date(2017, 1, 1)
end = datetime.date(2017, 12, 31)
span = end - start

# Assgin sgpmetE11 vars with specific length
sgpmetE11_atmos_pressure            = [None] * (span.days+1) * 1440 # qc_atmos_pressure
sgpmetE11_temp_mean                 = [None] * (span.days+1) * 1440 # qc_temp_mean 
sgpmetE11_rh_mean                   = [None] * (span.days+1) * 1440 # qc_rh_mean 
sgpmetE11_vapor_pressure_mean       = [None] * (span.days+1) * 1440 # qc_vapor_pressure_mean
sgpmetE11_wspd_arith_mean           = [None] * (span.days+1) * 1440 # qc_wspd_arith_mean
sgpmetE11_tbrg_precip_total_corr    = [None] * (span.days+1) * 1440 # qc_tbrg_precip_total_corr
sgpmetE11_qc_atmos_pressure         = [None] * (span.days+1) * 1440 # qc_atmos_pressure
sgpmetE11_qc_temp_mean              = [None] * (span.days+1) * 1440 # qc_temp_mean 
sgpmetE11_qc_rh_mean                = [None] * (span.days+1) * 1440 # qc_rh_mean 
sgpmetE11_qc_vapor_pressure_mean    = [None] * (span.days+1) * 1440 # qc_vapor_pressure_mean
sgpmetE11_qc_wspd_arith_mean        = [None] * (span.days+1) * 1440 # qc_wspd_arith_mean
sgpmetE11_qc_tbrg_precip_total_corr = [None] * (span.days+1) * 1440 # qc_tbrg_precip_total_corr

sgpmetE11 = []
names = ['atmos_pressure', 'temp_mean', 'rh_mean', 'vapor_pressure_mean', 'wspd_arith_mean', 'tbrg_precip_total_corr']

# Read netcdf files
path = "/Users/yupinglu/OneDrive/project/ARM/data/sample_data"
# path = "/Users/ylk/OneDrive/project/ARM/data/sgpmetE11"
netcdfs = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".cdf")]

for cdf in netcdfs:
    f = netCDF4.Dataset(join(path,cdf))
    # Read variables
    tm                        = f.variables['time']
    atmos_pressure            = f.variables['atmos_pressure']
    temp_mean                 = f.variables['temp_mean']
    rh_mean                   = f.variables['rh_mean']
    vapor_pressure_mean       = f.variables['vapor_pressure_mean']
    wspd_arith_mean           = f.variables['wspd_arith_mean']
    tbrg_precip_total_corr    = f.variables['tbrg_precip_total_corr']
    qc_atmos_pressure         = f.variables['qc_atmos_pressure']
    qc_temp_mean              = f.variables['qc_temp_mean']
    qc_rh_mean                = f.variables['qc_rh_mean']
    qc_vapor_pressure_mean    = f.variables['qc_vapor_pressure_mean']
    qc_wspd_arith_mean        = f.variables['qc_wspd_arith_mean']
    qc_tbrg_precip_total_corr = f.variables['qc_tbrg_precip_total_corr']
    # Convert numeric values of time in the specified units and calendar to datetime objects
    dates = netCDF4.num2date(tm[:], units=tm.units)
    # Read data into different sgpmetE11 vars with filter applied
    for i in range(len(atmos_pressure)):
        index = int((dates[i] - datetime.datetime(2017, 1, 1, 0, 0)).total_seconds() / 60)
        sgpmetE11_atmos_pressure[index]            = atmos_pressure[i]
        sgpmetE11_temp_mean[index]                 = temp_mean[i]
        sgpmetE11_rh_mean[index]                   = rh_mean[i]
        sgpmetE11_vapor_pressure_mean[index]       = vapor_pressure_mean[i]
        sgpmetE11_wspd_arith_mean[index]           = wspd_arith_mean[i] 
        sgpmetE11_tbrg_precip_total_corr[index]    = tbrg_precip_total_corr[i]
        sgpmetE11_qc_atmos_pressure[index]         = qc_atmos_pressure[i]
        sgpmetE11_qc_temp_mean[index]              = qc_temp_mean[i]
        sgpmetE11_qc_rh_mean[index]                = qc_rh_mean[i]
        sgpmetE11_qc_vapor_pressure_mean[index]    = qc_vapor_pressure_mean[i]
        sgpmetE11_qc_wspd_arith_mean[index]        = qc_wspd_arith_mean[i] 
        sgpmetE11_qc_tbrg_precip_total_corr[index] = qc_tbrg_precip_total_corr[i]
    f.close()

# Filter empty values and handle one day lag
sgpmetE11_atmos_pressure            = sgpmetE11_atmos_pressure[:len(sgpmetE11_atmos_pressure)-1440]
sgpmetE11_temp_mean                 = sgpmetE11_temp_mean[:len(sgpmetE11_temp_mean)-1440]
sgpmetE11_rh_mean                   = sgpmetE11_rh_mean[:len(sgpmetE11_rh_mean)-1440]
sgpmetE11_vapor_pressure_mean       = sgpmetE11_vapor_pressure_mean[:len(sgpmetE11_vapor_pressure_mean)-1440]
sgpmetE11_wspd_arith_mean           = sgpmetE11_wspd_arith_mean[:len(sgpmetE11_wspd_arith_mean)-1440]
sgpmetE11_qc_atmos_pressure         = sgpmetE11_qc_atmos_pressure[:len(sgpmetE11_qc_atmos_pressure)-1440]
sgpmetE11_qc_temp_mean              = sgpmetE11_qc_temp_mean[:len(sgpmetE11_qc_temp_mean)-1440]
sgpmetE11_qc_rh_mean                = sgpmetE11_qc_rh_mean[:len(sgpmetE11_qc_rh_mean)-1440]
sgpmetE11_qc_vapor_pressure_mean    = sgpmetE11_qc_vapor_pressure_mean[:len(sgpmetE11_qc_vapor_pressure_mean)-1440]
sgpmetE11_qc_wspd_arith_mean        = sgpmetE11_qc_wspd_arith_mean[:len(sgpmetE11_qc_wspd_arith_mean)-1440]
sgpmetE11_tbrg_precip_total_corr    = sgpmetE11_tbrg_precip_total_corr[1440:]
sgpmetE11_qc_tbrg_precip_total_corr = sgpmetE11_qc_tbrg_precip_total_corr[1440:]

for i in range(len(sgpmetE11_tbrg_precip_total_corr)):
    if sgpmetE11_qc_atmos_pressure[i] != 0 or sgpmetE11_qc_temp_mean[i] != 0 \
    or sgpmetE11_qc_rh_mean[i] != 0 or sgpmetE11_qc_vapor_pressure_mean[i] != 0 \
    or sgpmetE11_qc_wspd_arith_mean[i] != 0 or sgpmetE11_qc_tbrg_precip_total_corr[i] != 0 \
    or sgpmetE11_tbrg_precip_total_corr[i] == 0:
        sgpmetE11_atmos_pressure[i]         = None
        sgpmetE11_temp_mean[i]              = None
        sgpmetE11_rh_mean[i]                = None
        sgpmetE11_vapor_pressure_mean[i]    = None
        sgpmetE11_wspd_arith_mean[i]        = None
        sgpmetE11_tbrg_precip_total_corr[i] = None

np_atmos_pressure         = np.asarray([x for x in sgpmetE11_atmos_pressure if x is not None])
np_temp_mean              = np.asarray([x for x in sgpmetE11_temp_mean if x is not None])
np_rh_mean                = np.asarray([x for x in sgpmetE11_rh_mean if x is not None])
np_vapor_pressure_mean    = np.asarray([x for x in sgpmetE11_vapor_pressure_mean if x is not None])
np_wspd_arith_mean        = np.asarray([x for x in sgpmetE11_wspd_arith_mean if x is not None])
np_tbrg_precip_total_corr = np.asarray([x for x in sgpmetE11_tbrg_precip_total_corr if x is not None])

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

if (np_tbrg_precip_total_corr.max() - np_tbrg_precip_total_corr.min()) != 0:
    sgpmetE11.append((np_tbrg_precip_total_corr - np_tbrg_precip_total_corr.min())          \
        / (np_tbrg_precip_total_corr.max() - np_tbrg_precip_total_corr.min()))
else:
    print("tbrg_precip_total_corr: invalid value encountered in true_divide", file=sys.stderr)

# Calculate pearson correlations between sgpmetE11 vars
mat = np.corrcoef(sgpmetE11)
print(mat)

# Pick another color that is obvious to tell the difference
# Plot correlation matrix
#fig= plt.figure()
#ax = fig.add_subplot(111)
#cax= ax.matshow(mat, vmin=-1, vmax=1)
#fig.colorbar(cax)
#ticks = np.arange(0,mat.shape[0],1)
#ax.set_xticks(ticks)
#ax.set_yticks(ticks)
#ax.set_yticklabels(names)
#plt.show()

'''
[[ 1.         -0.57047323 -0.33150279 -0.51431958 -0.51142508  0.00670031]
 [-0.57047323  1.         -0.23464512  0.08683744  0.70886996  0.21494305]
 [-0.33150279 -0.23464512  1.          0.94587296 -0.48804501 -0.42986727]
 [-0.51431958  0.08683744  0.94587296  1.         -0.26041174 -0.37324093]
 [-0.51142508  0.70886996 -0.48804501 -0.26041174  1.          0.37000441]
 [ 0.00670031  0.21494305 -0.42986727 -0.37324093  0.37000441  1.        ]]
'''