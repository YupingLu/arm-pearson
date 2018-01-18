#!/usr/bin/env python3
# Tool to calculate the seasonal pearson correlations on sgpmet data
# Twelve correlations are calculated:
# 1) spring met correlation without qc_tbrg_precip_total_corr
# 2) spring met correlation with qc_tbrg_precip_total_corr
# 3) spring met correlation with qc_tbrg_precip_total_corr and one day lag
# 4) summer met correlation without qc_tbrg_precip_total_corr
# 5) summer met correlation with qc_tbrg_precip_total_corr
# 6) summer met correlation with qc_tbrg_precip_total_corr and one day lag
# 7) fall met correlation without qc_tbrg_precip_total_corr
# 8) fall met correlation with qc_tbrg_precip_total_corr
# 9) fall met correlation with qc_tbrg_precip_total_corr and one day lag
# 10) winter met correlation without qc_tbrg_precip_total_corr
# 11) winter met correlation with qc_tbrg_precip_total_corr
# 12) winter met correlation with qc_tbrg_precip_total_corr and one day lag
# Usage : python sgpmet_pearson_season instrument_name year
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Jan 18 2018

# Load libs
import sys
import argparse
import netCDF4
import numpy as np
import datetime
import fnmatch
import os

# Met Pearson Correlation
class MetPearson:
    '''Class to store the related variables and computed correlation matrices'''
    # Assgin sgpmet vars with specific length
    def __init__(self, span, seg):
        self.span                      = span
        self.seg                       = seg
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
        self.mat                       = []
        self.mat1                      = []
        self.mat2                      = []

# Calculate the days between the given time span
def total_days(year):
    start = datetime.date(year-1, 12, 31)
    end = datetime.date(year, 12, 31)
    return end - start

# Calculate the start and end of each season
def season_days(year):
    seg = []
    seg.append((datetime.date(year, 3, 31) - datetime.date(year-1, 12, 31)).days * 1440)
    seg.append((datetime.date(year, 6, 30) - datetime.date(year, 3, 31)).days * 1440)
    seg.append((datetime.date(year, 9, 30) - datetime.date(year, 6, 30)).days * 1440)
    return seg

# Normalize sgpmet variables
def norm_var(met_var, sgpmet, name):
    try:
        sgpmet.append((met_var - met_var.min()) / (met_var.max() - met_var.min()))
    except Exception as e:
        print(name, ": Zero Values", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

# Calculate Pearson Correlation
def pearson(tmp_atmos_pressure, tmp_temp_mean, tmp_rh_mean, \
                tmp_vapor_pressure_mean, tmp_wspd_arith_mean):
    sgpmet = []
    # Filter empty values
    np_atmos_pressure      = np.asarray([x for x in tmp_atmos_pressure if x is not None])
    np_temp_mean           = np.asarray([x for x in tmp_temp_mean if x is not None])
    np_rh_mean             = np.asarray([x for x in tmp_rh_mean if x is not None])
    np_vapor_pressure_mean = np.asarray([x for x in tmp_vapor_pressure_mean if x is not None])
    np_wspd_arith_mean     = np.asarray([x for x in tmp_wspd_arith_mean if x is not None])
    # Normalize sgpmet variables
    norm_var(np_atmos_pressure, sgpmet, "atmos_pressure")
    norm_var(np_temp_mean, sgpmet, "temp_mean")
    norm_var(np_rh_mean, sgpmet, "rh_mean")
    norm_var(np_vapor_pressure_mean, sgpmet, "vapor_pressure_mean")
    norm_var(np_wspd_arith_mean, sgpmet, "wspd_arith_mean")
    # Calculate pearson correlations between sgpmet variables
    return np.corrcoef(sgpmet)

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
    # Divide the year data into four seasons
    s1 = 0
    s2 = met_pearson.seg[0]
    s3 = met_pearson.seg[1]
    s4 = met_pearson.seg[2]
    met_pearson.mat.append(pearson(tmp_atmos_pressure[s1:s2], tmp_temp_mean[s1:s2], tmp_rh_mean[s1:s2], \
                                    tmp_vapor_pressure_mean[s1:s2], tmp_wspd_arith_mean[s1:s2]))
    met_pearson.mat.append(pearson(tmp_atmos_pressure[s2:s3], tmp_temp_mean[s2:s3], tmp_rh_mean[s2:s3], \
                                    tmp_vapor_pressure_mean[s2:s3], tmp_wspd_arith_mean[s2:s3]))
    met_pearson.mat.append(pearson(tmp_atmos_pressure[s3:s4], tmp_temp_mean[s3:s4], tmp_rh_mean[s3:s4], \
                                    tmp_vapor_pressure_mean[s3:s4], tmp_wspd_arith_mean[s3:s4]))
    met_pearson.mat.append(pearson(tmp_atmos_pressure[s4:], tmp_temp_mean[s4:], tmp_rh_mean[s4:], \
                                    tmp_vapor_pressure_mean[s4:], tmp_wspd_arith_mean[s4:]))

# Calculate Pearson Correlation
def pearson_corr(tmp_atmos_pressure, tmp_temp_mean, tmp_rh_mean, tmp_vapor_pressure_mean, \
                tmp_wspd_arith_mean, np_tbrg_precip_total_corr):
    sgpmet = []
    # Filter empty values
    np_atmos_pressure         = np.asarray([x for x in tmp_atmos_pressure if x is not None])
    np_temp_mean              = np.asarray([x for x in tmp_temp_mean if x is not None])
    np_rh_mean                = np.asarray([x for x in tmp_rh_mean if x is not None])
    np_vapor_pressure_mean    = np.asarray([x for x in tmp_vapor_pressure_mean if x is not None])
    np_wspd_arith_mean        = np.asarray([x for x in tmp_wspd_arith_mean if x is not None])
    np_tbrg_precip_total_corr = np.asarray([x for x in tmp_tbrg_precip_total_corr if x is not None])
    # Normalize sgpmet variables
    norm_var(np_atmos_pressure, sgpmet, "atmos_pressure")
    norm_var(np_temp_mean, sgpmet, "temp_mean")
    norm_var(np_rh_mean, sgpmet, "rh_mean")
    norm_var(np_vapor_pressure_mean, sgpmet, "vapor_pressure_mean")
    norm_var(np_wspd_arith_mean, sgpmet, "wspd_arith_mean")
    norm_var(np_tbrg_precip_total_corr, sgpmet, "tbrg_precip_total_corr")
    # Calculate pearson correlations between sgpmet variables
    return np.corrcoef(sgpmet)

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
    # Divide the year data into four seasons
    s1 = 0
    s2 = met_pearson.seg[0]
    s3 = met_pearson.seg[1]
    s4 = met_pearson.seg[2]
    met_pearson.mat1.append(pearson_corr(tmp_atmos_pressure[s1:s2], tmp_temp_mean[s1:s2], tmp_rh_mean[s1:s2], \
                tmp_vapor_pressure_mean[s1:s2], tmp_wspd_arith_mean[s1:s2], tmp_tbrg_precip_total_corr[s1:s2]))
    met_pearson.mat1.append(pearson_corr(tmp_atmos_pressure[s2:s3], tmp_temp_mean[s2:s3], tmp_rh_mean[s2:s3], \
                tmp_vapor_pressure_mean[s2:s3], tmp_wspd_arith_mean[s2:s3], tmp_tbrg_precip_total_corr[s2:s3]))
    met_pearson.mat1.append(pearson_corr(tmp_atmos_pressure[s3:s4], tmp_temp_mean[s3:s4], tmp_rh_mean[s3:s4], \
                tmp_vapor_pressure_mean[s3:s4], tmp_wspd_arith_mean[s3:s4], tmp_tbrg_precip_total_corr[s3:s4]))
    met_pearson.mat1.append(pearson_corr(tmp_atmos_pressure[s4:], tmp_temp_mean[s4:], tmp_rh_mean[s4:], \
                tmp_vapor_pressure_mean[s4:], tmp_wspd_arith_mean[s4:], tmp_tbrg_precip_total_corr[s4:]))

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
    # Divide the year data into four seasons
    s1 = 0
    s2 = met_pearson.seg[0]
    s3 = met_pearson.seg[1]
    s4 = met_pearson.seg[2]
    met_pearson.mat2.append(pearson_corr(tmp_atmos_pressure[s1:s2], tmp_temp_mean[s1:s2], tmp_rh_mean[s1:s2], \
                tmp_vapor_pressure_mean[s1:s2], tmp_wspd_arith_mean[s1:s2], tmp_tbrg_precip_total_corr[s1:s2]))
    met_pearson.mat2.append(pearson_corr(tmp_atmos_pressure[s2:s3], tmp_temp_mean[s2:s3], tmp_rh_mean[s2:s3], \
                tmp_vapor_pressure_mean[s2:s3], tmp_wspd_arith_mean[s2:s3], tmp_tbrg_precip_total_corr[s2:s3]))
    met_pearson.mat2.append(pearson_corr(tmp_atmos_pressure[s3:s4], tmp_temp_mean[s3:s4], tmp_rh_mean[s3:s4], \
                tmp_vapor_pressure_mean[s3:s4], tmp_wspd_arith_mean[s3:s4], tmp_tbrg_precip_total_corr[s3:s4]))
    met_pearson.mat2.append(pearson_corr(tmp_atmos_pressure[s4:], tmp_temp_mean[s4:], tmp_rh_mean[s4:], \
                tmp_vapor_pressure_mean[s4:], tmp_wspd_arith_mean[s4:], tmp_tbrg_precip_total_corr[s4:]))

# Read netcdf files and return the correlation matrices
def read_netcdf(path, year, inst, met_pearson):
    pattern = 'sgpmet'
    pattern += inst
    pattern += '.??.'
    pattern += str(year)
    pattern += '*'
    pattern += '.cdf'

    for cdf in os.listdir(path):
        if fnmatch.fnmatch(cdf, pattern):
            f = netCDF4.Dataset(os.path.join(path,cdf))
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
    parser.add_argument("path", help="data file path")
    parser.add_argument("inst", metavar="instrument", help="the instrument name")
    parser.add_argument("year", type=int, help="the year to calculate")
    args = parser.parse_args()
    print("Begin: ", args.inst, " ", args.year, file=sys.stderr)
    span = total_days(args.year)
    seg = season_days(args.year)
    met_pearson = MetPearson(span, seg)
    read_netcdf(args.path, args.year, args.inst, met_pearson)

    # Instrument_name_year.csv
    for i in range(4):
        # Save mat0
        csv_name = ''
        csv_name += args.inst
        csv_name += str(args.year)
        csv_name += '.'
        csv_name += str(i)
        csv_name += '.0.csv'
        np.savetxt(csv_name, met_pearson.mat[i], delimiter=",", comments="", fmt='%1.6f', \
                header="atmos_pressure, temp_mean, rh_mean, vapor_pressure_mean, wspd_arith_mean")
        # Save mat1
        csv_name = ''
        csv_name += args.inst
        csv_name += str(args.year)
        csv_name += '.'
        csv_name += str(i)
        csv_name += '.1.csv'
        np.savetxt(csv_name, met_pearson.mat1, delimiter=",", comments="", fmt='%1.6f', \
            header="atmos_pressure, temp_mean, rh_mean, vapor_pressure_mean, wspd_arith_mean, tbrg_precip_total_corr")
        # Save mat2
        csv_name = ''
        csv_name += args.inst
        csv_name += str(args.year)
        csv_name += '.'
        csv_name += str(i)
        csv_name += '.2.csv'
        np.savetxt(csv_name, met_pearson.mat2, delimiter=",", comments="", fmt='%1.6f', \
            header="atmos_pressure, temp_mean, rh_mean, vapor_pressure_mean, wspd_arith_mean, tbrg_precip_total_corr")
    
    print("Done", file=sys.stderr)
    return 0

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
