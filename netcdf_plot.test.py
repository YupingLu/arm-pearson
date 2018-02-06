#!/usr/bin/env python3
# Script to read netcdf data for 1 inst 1 year and visualize it
# Data is contracted to day scale
# Usage : python netcdf_plot.test.py path instrument_name year
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Feb 06 2018

# Load libs
import sys
import argparse
import netCDF4
import numpy as np
import datetime
import fnmatch
import os
import plotly
import plotly.graph_objs as go

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
            tm                     = f.variables['time']
            atmos_pressure         = f.variables['atmos_pressure']
            temp_mean              = f.variables['temp_mean']
            rh_mean                = f.variables['rh_mean']
            vapor_pressure_mean    = f.variables['vapor_pressure_mean']
            wspd_arith_mean        = f.variables['wspd_arith_mean']
            tbrg_precip_total_corr    = f.variables['tbrg_precip_total_corr']
            qc_atmos_pressure      = f.variables['qc_atmos_pressure']
            qc_temp_mean           = f.variables['qc_temp_mean']
            qc_rh_mean             = f.variables['qc_rh_mean']
            qc_vapor_pressure_mean = f.variables['qc_vapor_pressure_mean']
            qc_wspd_arith_mean     = f.variables['qc_wspd_arith_mean']
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

def getDates(year, span):
    x = []
    start = datetime.datetime(year, 1, 1, 0, 0)
    for i in range(span.days):
        x.append(start + datetime.timedelta(i))
    return x

# Main
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="data file path")
    parser.add_argument("inst", metavar="instrument", help="the instrument name")
    parser.add_argument("year", type=int, help="the year to calculate")
    args = parser.parse_args()
    print("Begin: ", args.inst, " ", args.year, " ", file=sys.stderr)
    span = total_days(args.year)
    
    atmos_pressure, temp_mean, rh_mean, vapor_pressure_mean, wspd_arith_mean, \
     tbrg_precip_total_corr = read_netcdf(args.path, args.year, args.inst, span)
    x = getDates(args.year, span)

    # Create traces
    trace0 = go.Scatter(
        x = x,
        y = atmos_pressure,
        mode = 'lines+markers',
        name = 'atmos_pressure'
    )

    trace1 = go.Scatter(
        x = x,
        y = temp_mean,
        mode = 'lines+markers',
        name = 'temp_mean'
    )

    trace2 = go.Scatter(
        x = x,
        y = rh_mean,
        mode = 'lines+markers',
        name = 'rh_mean'
    )

    trace3 = go.Scatter(
        x = x,
        y = vapor_pressure_mean,
        mode = 'lines+markers',
        name = 'vapor_pressure_mean'
    )

    trace4 = go.Scatter(
        x = x,
        y = wspd_arith_mean,
        mode = 'lines+markers',
        name = 'wspd_arith_mean'
    )

    trace5 = go.Scatter(
        x = x,
        y = tbrg_precip_total_corr,
        mode = 'lines+markers',
        name = 'tbrg_precip_total_corr'
    )

    plotly.offline.plot({
        "data": [trace0, trace1, trace2, trace3, trace4, trace5],
        "layout": go.Layout(title=args.inst + " " + str(args.year))
    })

    print("Done", file=sys.stderr)
    return 0

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)



