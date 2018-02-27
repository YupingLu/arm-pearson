#!/usr/bin/env python3
# Script to output outliers of pearson correlations of sgpmet data
# Usage : python outliers_iqr_season.py
# File path is hard coded, remember to change it.
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Feb 12 2018

# Load libs
import sys
import numpy as np
#import matplotlib.pyplot as plt
import csv
import fnmatch
import os

# Class to store the correlations
class X:
    def __init__(self, year, inst, pc, season):
        self.year = year  # year
        self.inst = inst  # instrument name
        self.pc = pc    # pearson correlation value
        self.season = season
    def __repr__(self):
        return repr((self.year, self.inst, self.pc, self.season))

# Read CSV file
def readCSVFile(path, inst):
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    x6 = []
    x7 = []
    x8 = []
    x9 = []
    x10 = []
    pattern = inst
    pattern += '*'
    pattern += '????.'
    pattern += '?'  ###season
    pattern += '.0.csv'
    for csvf in os.listdir(path):
        if fnmatch.fnmatch(csvf, pattern):
            strlen = len(csvf)
            season = csvf[-7:-6]
            year = csvf[-12:-8]
            strlen -= 12
            inst = csvf[0:strlen] 
            atmos_pressure      = []
            temp_mean           = []
            rh_mean             = []
            vapor_pressure_mean = []
            with open(os.path.join(path, csvf)) as f:
                csvReader = csv.reader(f)
                for row in csvReader:
                    atmos_pressure.append(row[0])
                    temp_mean.append(row[1])
                    rh_mean.append(row[2])
                    vapor_pressure_mean.append(row[3])

            if atmos_pressure[2] != 'nan':
                x1.append(X(int(year), inst, float(atmos_pressure[2]), season))
            if atmos_pressure[3] != 'nan':
                x2.append(X(int(year), inst, float(atmos_pressure[3]), season))
            if temp_mean[3] != 'nan':
                x3.append(X(int(year), inst, float(temp_mean[3]), season))
            if atmos_pressure[4] != 'nan':
                x4.append(X(int(year), inst, float(atmos_pressure[4]), season))
            if temp_mean[4] != 'nan':
                x5.append(X(int(year), inst, float(temp_mean[4]), season))
            if rh_mean[4] != 'nan':
                x6.append(X(int(year), inst, float(rh_mean[4]), season))
            if atmos_pressure[5] != 'nan':
                x7.append(X(int(year), inst, float(atmos_pressure[5]), season))
            if temp_mean[5] != 'nan':
                x8.append(X(int(year), inst, float(temp_mean[5]), season))
            if rh_mean[5] != 'nan':
                x9.append(X(int(year), inst, float(rh_mean[5]), season))
            if vapor_pressure_mean[5] != 'nan':
                x10.append(X(int(year), inst, float(vapor_pressure_mean[5]), season))
    return x1, x2, x3, x4, x5, x6, x7, x8, x9, x10

# Modified Z score method
def outliers_modified_z_score(x, varname):
    threshold = 3.5
    tmp_season = ['0', '1', '2', '3']
    res = []
    for t in tmp_season:
        pc = []
        for i in x:
            if i.season == t:
                pc.append(i.pc)
        median = np.median(pc)
        median_absolute_deviation = np.median([np.abs(y - median) for y in pc])
        if median_absolute_deviation != 0:
            for i in x:
                if i.season == t:
                    modified_z_scores = 0.6745 * (i.pc - median) / median_absolute_deviation
                    if np.abs(modified_z_scores) > threshold:
                        res.append(i)
    np.savetxt(varname, sorted(res, key=lambda x: x.year), delimiter=",", comments="", fmt='%s')

# IQR method
def outliers_iqr(x, varname):
    tmp_season = ['0', '1', '2', '3']
    res = []
    for t in tmp_season:
        pc = []
        for i in x:
            if i.season == t:
                pc.append(i.pc)
        quartile_1, quartile_3 = np.percentile(pc, [25, 75])
        iqr = quartile_3 - quartile_1
        lower_bound = quartile_1 - (iqr * 1.5)
        upper_bound = quartile_3 + (iqr * 1.5)
        for i in x:
            if i.season == t:
                if (i.pc > upper_bound) | (i.pc < lower_bound):
                    res.append(i)
    np.savetxt(varname, sorted(res, key=lambda x: x.year), delimiter=",", comments="", fmt='%s')

# Main
def main(argv):
    path = "/Users/ylk/Documents/GitHub/arm/season.pc.csv"
    inst = "E"

    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = readCSVFile(path, inst)
    
    outliers_modified_z_score(x1, "x1")
    outliers_modified_z_score(x2, "x2")
    outliers_modified_z_score(x3, "x3")
    outliers_modified_z_score(x4, "x4")
    outliers_modified_z_score(x5, "x5")
    outliers_modified_z_score(x6, "x6")
    outliers_modified_z_score(x7, "x7")
    outliers_modified_z_score(x8, "x8")
    outliers_modified_z_score(x9, "x9")
    outliers_modified_z_score(x10, "x10")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
