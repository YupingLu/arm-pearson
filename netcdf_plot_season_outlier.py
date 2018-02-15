#!/usr/bin/env python3
# Script to plot netcdf data with seasonal outliers from netcdf_inst_*_year.py
# Usage : python netcdf_plot_season_outlier.py
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Feb 13 2018

# Load libs
import sys
import csv
import plotly
import plotly.graph_objs as go
import datetime

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

# Calculate the days between the given time span
def spring_days(year):
    start = datetime.date(year-1, 12, 31)
    end = datetime.date(year, 3, 31)
    return start, end - start

def summer_days(year):
    start = datetime.date(year, 3, 31)
    end = datetime.date(year, 6, 30)
    return start, end - start

def fall_days(year):
    start = datetime.date(year, 6, 30)
    end = datetime.date(year, 9, 30)
    return start, end - start

def winter_days(year):
    start = datetime.date(year, 9, 30)
    end = datetime.date(year, 12, 31)
    return start, end - start

# Get the whole dates
def getDates(start, span):
    x = []
    for i in range(span.days):
        x.append(start + datetime.timedelta(i+1))
    return x

# Get x and y to fill
def getFill():
    x = []
    y = []
    #start, span = winter_days(1999)
    #x.extend(getDates(start, span))
    start1, span1 = spring_days(2002)
    x.extend(getDates(start1, span1))
    #start2, span2 = winter_days(2009)
    #x.extend(getDates(start2, span2))

    for i in range(len(x)):
        y.append(10)

    return x, y

# Main
def main(argv):
    path = 'E1_1993_2017.csv'
    inst = 'E1'
    year = '1993-2017'
    cdf = CDF() 
    readCSVFile(path, cdf)
    dx, dy = getFill()

    # Create traces
    '''
    trace0 = go.Scatter(
        x = cdf.date,
        y = cdf.atmos_pressure,
        mode = 'lines+markers',
        name = 'atmos_pressure'
    )'''
    trace1 = go.Scatter(
        x = cdf.date,
        y = cdf.temp_mean,
        mode = 'lines+markers',
        name = 'temp_mean'
    )
    '''
    trace2 = go.Scatter(
        x = cdf.date,
        y = cdf.rh_mean,
        mode = 'lines+markers',
        name = 'rh_mean'
    )'''
    trace3 = go.Scatter(
        x = cdf.date,
        y = cdf.vapor_pressure_mean,
        mode = 'lines+markers',
        name = 'vapor_pressure_mean'
    )
    '''
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
    )'''
    trace6 = go.Scatter(
        x = dx,
        y = dy,
        fill='tozeroy',
        mode= 'none',
        name = 'x5: temp_mean & vapor_pressure_mean'
    )
 
    plotly.offline.plot({
        "data": [trace1, trace3, trace6],
        "layout": go.Layout(title=inst + " " + year)
    })


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
