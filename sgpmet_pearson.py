#!/usr/bin/env python3
# Tool to calculate the pearson correlations on sgpmet data
# Three correlations are calculated:
# 1) met correlation without qc_tbrg_precip_total_corr
# 2) met correlation with qc_tbrg_precip_total_corr
# 3) met correlation with qc_tbrg_precip_total_corr and one day lag
# Usage : python sgpmet_pearson instrument_name year
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Dec 25 2017

# Load libs
import sys
import argparse
import netCDF4
import numpy as np
import datetime
from os import listdir
from os.path import isfile, join

# Met Pearson Correlation
class MetPearson:
    '''Class to store the related variables and computed correlation matrices'''
    # Assgin sgpmet vars with specific length
    def __init__(self, span):
        self.span                      = span
        self.atmos_pressure            = [None] * (span.days) * 1440 
        self.temp_mean                 = [None] * (span.days) * 1440 
        self.rh_mean                   = [None] * (span.days) * 1440 
        self.vapor_pressure_mean       = [None] * (span.days) * 1440 
        self.wspd_arith_mean           = [None] * (span.days) * 1440 
        self.tbrg_precip_total_corr    = [None] * (span.days) * 1440
        self.qc_atmos_pressure         = [None] * (span.days) * 1440
        self.qc_temp_mean              = [None] * (span.days) * 1440
        self.qc_rh_mean                = [None] * (span.days) * 1440
        self.qc_vapor_pressure_mean    = [None] * (span.days) * 1440
        self.qc_wspd_arith_mean        = [None] * (span.days) * 1440
        self.qc_tbrg_precip_total_corr = [None] * (span.days) * 1440

# Calculate the days between the given time span
def total_days(year):
    start = datetime.date(year-1, 12, 31)
    end = datetime.date(year, 12, 31)
    return end - start

# Normalize sgpmet variables
def norm_var(met_var, sgpmet):
    try:
        sgpmet.append((met_var - met_var.min()) / (met_var.max() - met_var.min()))
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

# Calculate the correlation matrix
def get_pearson(met_pearson):
    tmp_atmos_pressure            = [None] * (met_pearson.span.days) * 1440 
    tmp_temp_mean                 = [None] * (met_pearson.span.days) * 1440 
    tmp_rh_mean                   = [None] * (met_pearson.span.days) * 1440 
    tmp_vapor_pressure_mean       = [None] * (met_pearson.span.days) * 1440 
    tmp_wspd_arith_mean           = [None] * (met_pearson.span.days) * 1440 

    for i in range(len(tmp_atmos_pressure)):
        if met_pearson.qc_atmos_pressure[i] == 0 and met_pearson.qc_temp_mean[i] == 0 \
        and met_pearson.qc_rh_mean[i] == 0 and met_pearson.qc_vapor_pressure_mean[i] == 0 \
        and met_pearson.qc_wspd_arith_mean[i] == 0:
            tmp_atmos_pressure[i]      = met_pearson.atmos_pressure[i]
            tmp_temp_mean[i]           = met_pearson.temp_mean[i]
            tmp_rh_mean[i]             = met_pearson.rh_mean[i]
            tmp_vapor_pressure_mean[i] = met_pearson.vapor_pressure_mean[i]
            tmp_wspd_arith_mean[i]     = met_pearson.wspd_arith_mean[i] 

    sgpmet = []
    # Filter empty values
    np_atmos_pressure      = np.asarray([x for x in tmp_atmos_pressure if x is not None])
    np_temp_mean           = np.asarray([x for x in tmp_temp_mean if x is not None])
    np_rh_mean             = np.asarray([x for x in tmp_rh_mean if x is not None])
    np_vapor_pressure_mean = np.asarray([x for x in tmp_vapor_pressure_mean if x is not None])
    np_wspd_arith_mean     = np.asarray([x for x in tmp_wspd_arith_mean if x is not None])
    # Normalize sgpmet variables
    norm_var(np_atmos_pressure, sgpmet)
    norm_var(np_temp_mean, sgpmet)
    norm_var(np_rh_mean, sgpmet)
    norm_var(np_vapor_pressure_mean, sgpmet)
    norm_var(np_wspd_arith_mean, sgpmet)
    # Calculate pearson correlations between sgpmet variables
    met_pearson.mat = np.corrcoef(sgpmet)

# Calculate the correlation matrix with qc_tbrg_precip_total_corr
def get_pearson_corr(met_pearson):
    tmp_atmos_pressure         = [None] * (met_pearson.span.days) * 1440 
    tmp_temp_mean              = [None] * (met_pearson.span.days) * 1440 
    tmp_rh_mean                = [None] * (met_pearson.span.days) * 1440 
    tmp_vapor_pressure_mean    = [None] * (met_pearson.span.days) * 1440 
    tmp_wspd_arith_mean        = [None] * (met_pearson.span.days) * 1440 
    tmp_tbrg_precip_total_corr = [None] * (met_pearson.span.days) * 1440

    for i in range(len(tmp_atmos_pressure)):
        if met_pearson.qc_atmos_pressure[i] == 0 and met_pearson.qc_temp_mean[i] == 0 \
        and met_pearson.qc_rh_mean[i] == 0 and met_pearson.qc_vapor_pressure_mean[i] == 0 \
        and met_pearson.qc_wspd_arith_mean[i] == 0 and met_pearson.qc_tbrg_precip_total_corr[i] == 0 \
        and met_pearson.tbrg_precip_total_corr[i] != 0:
            tmp_atmos_pressure[i]         = met_pearson.atmos_pressure[i]
            tmp_temp_mean[i]              = met_pearson.temp_mean[i]
            tmp_rh_mean[i]                = met_pearson.rh_mean[i]
            tmp_vapor_pressure_mean[i]    = met_pearson.vapor_pressure_mean[i]
            tmp_wspd_arith_mean[i]        = met_pearson.wspd_arith_mean[i] 
            tmp_tbrg_precip_total_corr[i] = met_pearson.tbrg_precip_total_corr[i]

    sgpmet = []
    # Filter empty values
    np_atmos_pressure         = np.asarray([x for x in tmp_atmos_pressure if x is not None])
    np_temp_mean              = np.asarray([x for x in tmp_temp_mean if x is not None])
    np_rh_mean                = np.asarray([x for x in tmp_rh_mean if x is not None])
    np_vapor_pressure_mean    = np.asarray([x for x in tmp_vapor_pressure_mean if x is not None])
    np_wspd_arith_mean        = np.asarray([x for x in tmp_wspd_arith_mean if x is not None])
    np_tbrg_precip_total_corr = np.asarray([x for x in tmp_tbrg_precip_total_corr if x is not None])
    # Normalize sgpmet variables
    norm_var(np_atmos_pressure, sgpmet)
    norm_var(np_temp_mean, sgpmet)
    norm_var(np_rh_mean, sgpmet)
    norm_var(np_vapor_pressure_mean, sgpmet)
    norm_var(np_wspd_arith_mean, sgpmet)
    norm_var(np_tbrg_precip_total_corr, sgpmet)
    # Calculate pearson correlations between sgpmet variables
    met_pearson.mat1 = np.corrcoef(sgpmet)

# Calculate the correlation matrix with qc_tbrg_precip_total_corr and one day lag
def get_pearson_corr_lag(met_pearson):
    tmp_atmos_pressure         = [None] * (met_pearson.span.days-1) * 1440 
    tmp_temp_mean              = [None] * (met_pearson.span.days-1) * 1440 
    tmp_rh_mean                = [None] * (met_pearson.span.days-1) * 1440 
    tmp_vapor_pressure_mean    = [None] * (met_pearson.span.days-1) * 1440 
    tmp_wspd_arith_mean        = [None] * (met_pearson.span.days-1) * 1440 
    tmp_tbrg_precip_total_corr = [None] * (met_pearson.span.days-1) * 1440

    for i in range(len(tmp_atmos_pressure)):
        if met_pearson.qc_atmos_pressure[i] == 0 and met_pearson.qc_temp_mean[i] == 0 \
        and met_pearson.qc_rh_mean[i] == 0 and met_pearson.qc_vapor_pressure_mean[i] == 0 \
        and met_pearson.qc_wspd_arith_mean[i] == 0 and met_pearson.qc_tbrg_precip_total_corr[i+1440] == 0 \
        and met_pearson.tbrg_precip_total_corr[i+1440] != 0:
            tmp_atmos_pressure[i]         = met_pearson.atmos_pressure[i]
            tmp_temp_mean[i]              = met_pearson.temp_mean[i]
            tmp_rh_mean[i]                = met_pearson.rh_mean[i]
            tmp_vapor_pressure_mean[i]    = met_pearson.vapor_pressure_mean[i]
            tmp_wspd_arith_mean[i]        = met_pearson.wspd_arith_mean[i] 
            tmp_tbrg_precip_total_corr[i] = met_pearson.tbrg_precip_total_corr[i+1440]

    sgpmet = []
    # Filter empty values
    np_atmos_pressure         = np.asarray([x for x in tmp_atmos_pressure if x is not None])
    np_temp_mean              = np.asarray([x for x in tmp_temp_mean if x is not None])
    np_rh_mean                = np.asarray([x for x in tmp_rh_mean if x is not None])
    np_vapor_pressure_mean    = np.asarray([x for x in tmp_vapor_pressure_mean if x is not None])
    np_wspd_arith_mean        = np.asarray([x for x in tmp_wspd_arith_mean if x is not None])
    np_tbrg_precip_total_corr = np.asarray([x for x in tmp_tbrg_precip_total_corr if x is not None])
    # Normalize sgpmet variables
    norm_var(np_atmos_pressure, sgpmet)
    norm_var(np_temp_mean, sgpmet)
    norm_var(np_rh_mean, sgpmet)
    norm_var(np_vapor_pressure_mean, sgpmet)
    norm_var(np_wspd_arith_mean, sgpmet)
    norm_var(np_tbrg_precip_total_corr, sgpmet)
    # Calculate pearson correlations between sgpmet variables
    met_pearson.mat2 = np.corrcoef(sgpmet)

# Read netcdf files and return the correlation matrices
def read_netcdf(path, year, met_pearson):
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
        # Read data into different sgpmet vars with filter applied
        for i in range(len(atmos_pressure)):
            index = int((dates[i] - datetime.datetime(year, 1, 1, 0, 0)).total_seconds() / 60)
            met_pearson.atmos_pressure[index]            = atmos_pressure[i]
            met_pearson.temp_mean[index]                 = temp_mean[i]
            met_pearson.rh_mean[index]                   = rh_mean[i]
            met_pearson.vapor_pressure_mean[index]       = vapor_pressure_mean[i]
            met_pearson.wspd_arith_mean[index]           = wspd_arith_mean[i] 
            met_pearson.tbrg_precip_total_corr[index]    = tbrg_precip_total_corr[i]
            met_pearson.qc_atmos_pressure[index]         = qc_atmos_pressure[i]
            met_pearson.qc_temp_mean[index]              = qc_temp_mean[i]
            met_pearson.qc_rh_mean[index]                = qc_rh_mean[i]
            met_pearson.qc_vapor_pressure_mean[index]    = qc_vapor_pressure_mean[i]
            met_pearson.qc_wspd_arith_mean[index]        = qc_wspd_arith_mean[i] 
            met_pearson.qc_tbrg_precip_total_corr[index] = qc_tbrg_precip_total_corr[i]
        f.close()

    get_pearson(met_pearson)
    get_pearson_corr(met_pearson)
    get_pearson_corr_lag(met_pearson)

# Main
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("inst", metavar="instrument", help="the instrument name")
    parser.add_argument("year", type=int, help="the year to calculate")
    args = parser.parse_args()

    span = total_days(args.year)
    met_pearson = MetPearson(span)
    path = "/Users/yupinglu/OneDrive/project/ARM/data/sample_data"

    read_netcdf(path, args.year, met_pearson)

    # Instrument_name_year.csv
    # Save mat
    numpy.savetxt("mat.csv", met_pearson.mat, delimiter=",", comments="", \
                  header="atmos_pressure, temp_mean, rh_mean, \
                  vapor_pressure_mean, wspd_arith_mean")
    # Save mat1
    numpy.savetxt("mat1.csv", met_pearson.mat1, delimiter=",", comments="", \
                  header="atmos_pressure, temp_mean, rh_mean, \
                  vapor_pressure_mean, wspd_arith_mean, tbrg_precip_total_corr")
    # Save mat2
    numpy.savetxt("mat2.csv", met_pearson.mat2, delimiter=",", comments="", \
                  header="atmos_pressure, temp_mean, rh_mean, \
                  vapor_pressure_mean, wspd_arith_mean, tbrg_precip_total_corr")
    return 0

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
