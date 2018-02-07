#!/usr/bin/env python3
# Script to get netcdf data for 1 inst from 1993 to 2017.
# Data is contracted to day scale
# Usage : python netcdf_inst_all_year.py path instrument_name begin_year end_year
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Feb 07 2018

# Load libs
import sys
import argparse
import netCDF4
import numpy as np
import datetime
import fnmatch
import os

# Calculate the days between the given time span
def total_days(year):
    start = datetime.date(year-1, 12, 31)
    end = datetime.date(year, 12, 31)
    return end - start

# Read netcdf files and return the variable value averaged by a day
def read_netcdf(path, year, inst, span):
    tmp_atmos_pressure         = [None] * span.days
    tmp_temp_mean              = [None] * span.days
    tmp_rh_mean                = [None] * span.days
    tmp_vapor_pressure_mean    = [None] * span.days
    tmp_wspd_arith_mean        = [None] * span.days
    tmp_tbrg_precip_total_corr = [None] * span.days
    atmos_pressure_cnt         = [0] * span.days
    temp_mean_cnt              = [0] * span.days 
    rh_mean_cnt                = [0] * span.days 
    vapor_pressure_mean_cnt    = [0] * span.days 
    wspd_arith_mean_cnt        = [0] * span.days 
    tbrg_precip_total_corr_cnt = [0] * span.days
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
            for i in range(len(tm)):
                index = int((dates[i] - datetime.datetime(year, 1, 1, 0, 0)).days)
                if qc_atmos_pressure[i] == 0:
                    if tmp_atmos_pressure[index] == None:
                        tmp_atmos_pressure[index] = atmos_pressure[i]
                    else:
                        tmp_atmos_pressure[index] += atmos_pressure[i]
                    atmos_pressure_cnt[index] += 1 

                if qc_temp_mean[i] == 0:
                    if tmp_temp_mean[index] == None:
                        tmp_temp_mean[index] = temp_mean[i]
                    else:
                        tmp_temp_mean[index] += temp_mean[i]
                    temp_mean_cnt[index] += 1 

                if qc_rh_mean[i] == 0:
                    if tmp_rh_mean[index] == None:
                        tmp_rh_mean[index] = rh_mean[i]
                    else:
                        tmp_rh_mean[index] += rh_mean[i]
                    rh_mean_cnt[index] += 1 

                if qc_vapor_pressure_mean[i] == 0:
                    if tmp_vapor_pressure_mean[index] == None:
                        tmp_vapor_pressure_mean[index] = vapor_pressure_mean[i]
                    else:
                        tmp_vapor_pressure_mean[index] += vapor_pressure_mean[i]
                    vapor_pressure_mean_cnt[index] += 1 

                if qc_wspd_arith_mean[i] == 0:
                    if tmp_wspd_arith_mean[index] == None:
                        tmp_wspd_arith_mean[index] = wspd_arith_mean[i]
                    else:
                        tmp_wspd_arith_mean[index] += wspd_arith_mean[i]
                    wspd_arith_mean_cnt[index] += 1

                if qc_tbrg_precip_total_corr[i] == 0:
                    if tmp_tbrg_precip_total_corr[index] == None:
                        tmp_tbrg_precip_total_corr[index] = tbrg_precip_total_corr[i]
                    else:
                        tmp_tbrg_precip_total_corr[index] += tbrg_precip_total_corr[i]
                    tbrg_precip_total_corr_cnt[index] += 1 

            f.close()

    for i in range(span.days):
        if tmp_atmos_pressure[i] != None:
            tmp_atmos_pressure[i] /= atmos_pressure_cnt[i]
        if tmp_temp_mean[i] != None:
            tmp_temp_mean[i] /= temp_mean_cnt[i]
        if tmp_rh_mean[i] != None:
            tmp_rh_mean[i] /= rh_mean_cnt[i]
        if tmp_vapor_pressure_mean[i] != None:
            tmp_vapor_pressure_mean[i] /= vapor_pressure_mean_cnt[i]
        if tmp_wspd_arith_mean[i] != None:
            tmp_wspd_arith_mean[i] /= wspd_arith_mean_cnt[i]
        if tmp_tbrg_precip_total_corr[i] != None:
            tmp_tbrg_precip_total_corr[i] /= tbrg_precip_total_corr_cnt[i]

    return tmp_atmos_pressure, tmp_temp_mean, tmp_rh_mean, tmp_vapor_pressure_mean, \
    tmp_wspd_arith_mean, tmp_tbrg_precip_total_corr

# Get the whole dates
def getDates(byear, eyear):
    x = []
    start = datetime.date(byear-1, 12, 31)
    end = datetime.date(eyear, 12, 31)
    span = (end - start).days
    begin = datetime.datetime(byear, 1, 1, 0, 0)
    for i in range(span):
        x.append(begin + datetime.timedelta(i))
    return x

# Main
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="data file path")
    parser.add_argument("inst", metavar="instrument", help="the instrument name")
    parser.add_argument("byear", type=int, help="the begin year to calculate")
    parser.add_argument("eyear", type=int, help="the end year to calculate")
    args = parser.parse_args()
    print("Begin: ", args.inst, " ", args.byear, " ", args.eyear, " ", file=sys.stderr)
    
    atmos_pressure         = []
    temp_mean              = []
    rh_mean                = []
    vapor_pressure_mean    = []
    wspd_arith_mean        = []
    tbrg_precip_total_corr = []

    # extend each data for each year to the global vars
    for year in range(args.byear, args.eyear+1):
        t_span = total_days(year)
        t_atmos_pressure, t_temp_mean, t_rh_mean, t_vapor_pressure_mean, t_wspd_arith_mean, \
         t_tbrg_precip_total_corr = read_netcdf(args.path, year, args.inst, t_span)

        atmos_pressure.extend(t_atmos_pressure)
        temp_mean.extend(t_temp_mean)
        rh_mean.extend(t_rh_mean)
        vapor_pressure_mean.extend(t_vapor_pressure_mean)
        wspd_arith_mean.extend(t_wspd_arith_mean)
        tbrg_precip_total_corr.extend(t_tbrg_precip_total_corr)
    
    x = getDates(args.byear, args.eyear)

    # Save results to inst_year.csv
    cdf = []
    cdf.append(x)
    cdf.append(atmos_pressure)
    cdf.append(temp_mean)
    cdf.append(rh_mean)
    cdf.append(vapor_pressure_mean)
    cdf.append(wspd_arith_mean)
    cdf.append(tbrg_precip_total_corr)  
    csv_name = ''
    csv_name += args.inst
    csv_name += '_'
    csv_name += str(args.byear)
    csv_name += '_'
    csv_name += str(args.eyear)
    csv_name += '.csv'
    np.savetxt(csv_name, np.transpose(cdf), delimiter=",", comments="", fmt='%s', \
            header="date, atmos_pressure, temp_mean, rh_mean, vapor_pressure_mean, wspd_arith_mean, tbrg_precip_total_corr")

    print("Done", file=sys.stderr)
    return 0

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
