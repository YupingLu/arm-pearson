#!/usr/bin/env python3
# Script to plot sgpmet data
# Usage : python netcdf_plot.py path instrument_name year variable
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Jan 30 2018

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

# Read netcdf files and return the correlation matrices
def read_netcdf(path, year, inst, var, span):
    temp = [None] * span.days * 1440

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
            tm    = f.variables['time']
            temp1 = f.variables[var]
            # Convert numeric values of time in the specified units and calendar to datetime objects
            dates = netCDF4.num2date(tm[:], units=tm.units)
            # Read data into different sgpmet vars with filter applied
            for i in range(len(temp1)):
                index = int((dates[i] - datetime.datetime(year, 1, 1, 0, 0)).total_seconds() / 60)
                temp[index] = temp1[i]
            f.close()
    return temp
# Main
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="data file path")
    parser.add_argument("inst", metavar="instrument", help="the instrument name")
    parser.add_argument("year", type=int, help="the year to calculate")
    parser.add_argument("var", metavar="variable", help="the variable name")
    args = parser.parse_args()
    print("Begin: ", args.inst, " ", args.year, " ", args.var, file=sys.stderr)
    span = total_days(args.year)
    
    data = read_netcdf(args.path, args.year, args.inst, args.var, span)
    x = list(range(span.days * 1440))

    # Create traces
    trace0 = go.Scatter(
        x = x,
        y = data,
        mode = 'lines+markers',
        name = args.var
    )

    plotly.offline.plot({
        "data": [trace0],
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



