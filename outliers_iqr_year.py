#!/usr/bin/env python3
# Script to output outliers of pearson correlations of sgpmet data
# Usage : python outliers_iqr_year.py
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
    def __init__(self, year, inst, pc):
        self.year = year  # year
        self.inst = inst  # instrument name
        self.pc = pc    # pearson correlation value
    def __repr__(self):
        return repr((self.year, self.inst, self.pc))

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
    pattern += '????.0'
    pattern += '.csv'
    for csvf in os.listdir(path):
        if fnmatch.fnmatch(csvf, pattern):
            strlen = len(csvf)
            year = csvf[-10:-6]
            strlen -= 10
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
            x1.append(X(int(year), inst, float(atmos_pressure[2])))
            x2.append(X(int(year), inst, float(atmos_pressure[3])))
            x3.append(X(int(year), inst, float(temp_mean[3])))
            x4.append(X(int(year), inst, float(atmos_pressure[4])))
            x5.append(X(int(year), inst, float(temp_mean[4])))
            x6.append(X(int(year), inst, float(rh_mean[4])))
            x7.append(X(int(year), inst, float(atmos_pressure[5])))
            x8.append(X(int(year), inst, float(temp_mean[5])))
            x9.append(X(int(year), inst, float(rh_mean[5])))
            x10.append(X(int(year), inst, float(vapor_pressure_mean[5])))
    return x1, x2, x3, x4, x5, x6, x7, x8, x9, x10

# IQR method
def outliers_iqr(x, varname):
    res = []
    pc = []
    for i in x:
        pc.append(i.pc)
    quartile_1, quartile_3 = np.percentile(pc, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)
    for i in x:
        if (i.pc > upper_bound) | (i.pc < lower_bound):
            res.append(i)
    np.savetxt(varname, sorted(res, key=lambda x: x.year), delimiter=",", comments="", fmt='%s')

# Main
def main(argv):
    path = "/Users/yupinglu/github/arm/year.pc.csv"
    inst = "E"

    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = readCSVFile(path, inst)

    outliers_iqr(x1, "x1")
    outliers_iqr(x2, "x2")
    outliers_iqr(x3, "x3")
    outliers_iqr(x4, "x4")
    outliers_iqr(x5, "x5")
    outliers_iqr(x6, "x6")
    outliers_iqr(x7, "x7")
    outliers_iqr(x8, "x8")
    outliers_iqr(x9, "x9")
    outliers_iqr(x10, "x10")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
