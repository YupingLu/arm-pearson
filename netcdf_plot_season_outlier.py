#!/usr/bin/env python3
# Script to plot netcdf data with seasonal outliers from netcdf_inst_*_year.py in batch
# Usage : python netcdf_plot_season_outlier.py
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Feb 16 2018

# Load libs
import sys
import csv
import plotly
import plotly.graph_objs as go
import datetime
import fnmatch
import os

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
def getFill(start, span):
    x = []
    y = []
    x.extend(getDates(start, span))
    for i in range(len(x)):
        y.append(10)
    return x, y

def readOutlier(file, target):
    dx = []
    dy = []
    with open(file) as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            year = int(row[0].strip()[1:])
            inst = row[1].strip()[1:-1]
            #pc = float(row[2].strip())
            season = int(row[3].strip()[1:-2])
            if inst == target:
                if season == 0:
                    start, span = spring_days(year)
                    x, y = getFill(start, span)
                    dx.extend(x)
                    dy.extend(y)
                elif season == 1:
                    start, span = summer_days(year)
                    x, y = getFill(start, span)
                    dx.extend(x)
                    dy.extend(y)
                elif season == 2:
                    start, span = fall_days(year)
                    x, y = getFill(start, span)
                    dx.extend(x)
                    dy.extend(y)
                elif season == 3:
                    start, span = winter_days(year)
                    x, y = getFill(start, span)
                    dx.extend(x)
                    dy.extend(y)
    return dx, dy

# Plot CSV file
def plotCSVFile(path, outlier_path):
    pattern = '*'
    pattern += '_1993_2017.csv'
    for csvf in os.listdir(path):
        if fnmatch.fnmatch(csvf, pattern):
            inst = csvf[:-14]
            year = '1993-2017'
            cdf = CDF() 
            readCSVFile(os.path.join(path, csvf), cdf)
            # Create traces
            #'x1: atmos_pressure & temp_mean'
            dx, dy = readOutlier(os.path.join(outlier_path, 'x1'), inst)
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
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x1: atmos_pressure & temp_mean'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x1.html', show_link = False, auto_open = False)
            #'x2: atmos_pressure & rh_mean'
            dx, dy = readOutlier(os.path.join(outlier_path, 'x2'), inst)
            trace0 = go.Scatter(
                x = cdf.date,
                y = cdf.atmos_pressure,
                mode = 'lines+markers',
                name = 'atmos_pressure'
            )
            trace1 = go.Scatter(
                x = cdf.date,
                y = cdf.rh_mean,
                mode = 'lines+markers',
                name = 'rh_mean'
            )
            trace2 = go.Scatter(
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x2: atmos_pressure & rh_mean'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x2.html', show_link = False, auto_open = False)
            #'x3: temp_mean & rh_mean'
            dx, dy = readOutlier(os.path.join(outlier_path, 'x3'), inst)
            trace0 = go.Scatter(
                x = cdf.date,
                y = cdf.temp_mean,
                mode = 'lines+markers',
                name = 'temp_mean'
            )
            trace1 = go.Scatter(
                x = cdf.date,
                y = cdf.rh_mean,
                mode = 'lines+markers',
                name = 'rh_mean'
            )
            trace2 = go.Scatter(
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x3: temp_mean & rh_mea'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x3.html', show_link = False, auto_open = False)
            #'x4: atmos_pressure & vapor_pressure_mean'
            dx, dy = readOutlier(os.path.join(outlier_path, 'x4'), inst)
            trace0 = go.Scatter(
                x = cdf.date,
                y = cdf.atmos_pressure,
                mode = 'lines+markers',
                name = 'atmos_pressure'
            )
            trace1 = go.Scatter(
                x = cdf.date,
                y = cdf.vapor_pressure_mean,
                mode = 'lines+markers',
                name = 'vapor_pressure_mean'
            )
            trace2 = go.Scatter(
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x4: atmos_pressure & vapor_pressure_mean'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x4.html', show_link = False, auto_open = False)
            #'x5: temp_mean & vapor_pressure_mean'
            dx, dy = readOutlier(os.path.join(outlier_path, 'x5'), inst)
            trace0 = go.Scatter(
                x = cdf.date,
                y = cdf.temp_mean,
                mode = 'lines+markers',
                name = 'temp_mean'
            )
            trace1 = go.Scatter(
                x = cdf.date,
                y = cdf.vapor_pressure_mean,
                mode = 'lines+markers',
                name = 'vapor_pressure_mean'
            )
            trace2 = go.Scatter(
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x5: temp_mean & vapor_pressure_mean'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x5.html', show_link = False, auto_open = False)
            #'x6: rh_mean & vapor_pressure_mean'
            dx, dy = readOutlier(os.path.join(outlier_path, 'x6'), inst)
            trace0 = go.Scatter(
                x = cdf.date,
                y = cdf.rh_mean,
                mode = 'lines+markers',
                name = 'rh_mean'
            )
            trace1 = go.Scatter(
                x = cdf.date,
                y = cdf.vapor_pressure_mean,
                mode = 'lines+markers',
                name = 'vapor_pressure_mean'
            )
            trace2 = go.Scatter(
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x6: rh_mean & vapor_pressure_mean'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x6.html', show_link = False, auto_open = False)
            #'x7: atmos_pressure & wspd_arith_mean'
            dx, dy = readOutlier(os.path.join(outlier_path, 'x7'), inst)
            trace0 = go.Scatter(
                x = cdf.date,
                y = cdf.atmos_pressure,
                mode = 'lines+markers',
                name = 'atmos_pressure'
            )
            trace1 = go.Scatter(
                x = cdf.date,
                y = cdf.wspd_arith_mean,
                mode = 'lines+markers',
                name = 'wspd_arith_mean'
            )
            trace2 = go.Scatter(
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x7: atmos_pressure & wspd_arith_mean'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x7.html', show_link = False, auto_open = False)
            #'x8: temp_mean & wspd_arith_mean'
            dx, dy = readOutlier(os.path.join(outlier_path, 'x8'), inst)
            trace0 = go.Scatter(
                x = cdf.date,
                y = cdf.temp_mean,
                mode = 'lines+markers',
                name = 'temp_mean'
            )
            trace1 = go.Scatter(
                x = cdf.date,
                y = cdf.wspd_arith_mean,
                mode = 'lines+markers',
                name = 'wspd_arith_mean'
            )
            trace2 = go.Scatter(
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x8: temp_mean & wspd_arith_mean'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x8.html', show_link = False, auto_open = False)
            #'x9: rh_mean & wspd_arith_mean'
            dx, dy = readOutlier(os.path.join(outlier_path, 'x9'), inst)
            trace0 = go.Scatter(
                x = cdf.date,
                y = cdf.rh_mean,
                mode = 'lines+markers',
                name = 'rh_mean'
            )
            trace1 = go.Scatter(
                x = cdf.date,
                y = cdf.wspd_arith_mean,
                mode = 'lines+markers',
                name = 'wspd_arith_mean'
            )
            trace2 = go.Scatter(
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x9: rh_mean & wspd_arith_mean'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x9.html', show_link = False, auto_open = False)
            #'x10: vapor_pressure_mean & wspd_arith_mean' 
            dx, dy = readOutlier(os.path.join(outlier_path, 'x10'), inst)
            trace0 = go.Scatter(
                x = cdf.date,
                y = cdf.vapor_pressure_mean,
                mode = 'lines+markers',
                name = 'vapor_pressure_mean'
            )
            trace1 = go.Scatter(
                x = cdf.date,
                y = cdf.wspd_arith_mean,
                mode = 'lines+markers',
                name = 'wspd_arith_mean'
            )
            trace2 = go.Scatter(
                x = dx,
                y = dy,
                #fill ='tozeroy',
                #mode = 'none',
                mode = 'markers',
                marker = dict(size='16'),
                name = 'x10: vapor_pressure_mean & wspd_arith_mean'
            )
            plotly.offline.plot({
                "data": [trace0, trace1, trace2],
                "layout": go.Layout(title=inst + " " + year)
                
            }, filename =inst+'-'+year+'-x10.html', show_link = False, auto_open = False)

# Main
def main(argv):
    path = '/Users/ylk/Documents/GitHub/arm/netcdf_year_viz'
    outlier_path = '/Users/ylk/Documents/GitHub/arm/outliers/season'
    plotCSVFile(path, outlier_path)
    
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
