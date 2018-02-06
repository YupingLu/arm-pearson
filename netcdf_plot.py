#!/usr/bin/env python3
# Script to plot netcdf data from netcdf_inst_*_year.py
# Usage : python netcdf_plot.py
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Feb 6 2018

# Load libs
import sys
import csv
import plotly
import plotly.graph_objs as go

# Class to store the data read from csv
class CDF:
    def __init__(self):
        self.date                   = []
        self.atmos_pressure         = []
        self.temp_mean              = []
        self.rh_mean                = []
        self.vapor_pressure_mean    = []
        self.wspd_arith_mean        = []
        self.tbrg_precip_total_corr = []

# Read CSV file
def readCSVFile(path, cdf):
    with open(path) as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            cdf.date.append(row[0])
            cdf.atmos_pressure.append(row[1])
            cdf.temp_mean.append(row[2])
            cdf.rh_mean.append(row[3])
            cdf.vapor_pressure_mean.append(row[4])
            cdf.wspd_arith_mean.append(row[5])
            cdf.tbrg_precip_total_corr.append(row[6])

# Main
def main(argv):
    path = 'E11_2017.csv'
    inst = 'E11'
    year = '2017'
    cdf = CDF() 
    readCSVFile(path, cdf)

    # Create traces
    trace0 = go.Scatter(
        x = cdf.date,
        y = cdf.atmos_pressure,
        mode = 'lines+markers',
        name = 'atmos_pressure'
    )
    trace1 = go.Scatter(
        x = cdf.date,
        y = cdf.temp_mean,
        mode = 'lines+markers',
        name = 'temp_mean'
    )
    trace2 = go.Scatter(
        x = cdf.date,
        y = cdf.rh_mean,
        mode = 'lines+markers',
        name = 'rh_mean'
    )
    trace3 = go.Scatter(
        x = cdf.date,
        y = cdf.vapor_pressure_mean,
        mode = 'lines+markers',
        name = 'vapor_pressure_mean'
    )
    trace4 = go.Scatter(
        x = cdf.date,
        y = cdf.wspd_arith_mean,
        mode = 'lines+markers',
        name = 'wspd_arith_mean'
    )
    trace5 = go.Scatter(
        x = cdf.date,
        y = cdf.tbrg_precip_total_corr,
        mode = 'lines+markers',
        name = 'tbrg_precip_total_corr'
    )

    plotly.offline.plot({
        "data": [trace0, trace1, trace2, trace3, trace4, trace5],
        "layout": go.Layout(title=inst + " " + year)
    })


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
