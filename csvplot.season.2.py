#!/usr/bin/env python3
# Script to plot seasonal pearson correlations of sgpmet data
# Usage : python csvplot.season.2.py
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Jan 24 2018

# Load libs
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
import fnmatch
import os

# Class to store the correlations
class X:
    def __init__(self):
        self.x1 = []
        self.x2 = []
        self.x3 = []
        self.x4 = []
        self.x5 = []
        self.x6 = []
        self.x7 = []
        self.x8 = []
        self.x9 = []
        self.x10 = []
        self.x11 = []
        self.x12 = []
        self.x13 = []
        self.x14 = []
        self.x15 = []

# Read CSV file
def readCSVFile(path, inst, x):
    pattern = inst
    pattern += '*'
    pattern += '????.'
    pattern += '0'  ###season
    pattern += '.2.csv'
    for csvf in os.listdir(path):
        if fnmatch.fnmatch(csvf, pattern):
            atmos_pressure      = []
            temp_mean           = []
            rh_mean             = []
            vapor_pressure_mean = []
            wspd_arith_mean     = []

            with open(os.path.join(path, csvf)) as f:
                csvReader = csv.reader(f)
                for row in csvReader:
                    atmos_pressure.append(row[0])
                    temp_mean.append(row[1])
                    rh_mean.append(row[2])
                    vapor_pressure_mean.append(row[3])
                    wspd_arith_mean.append(row[4])

            if atmos_pressure[2] != 'nan':
                x.x1.append(atmos_pressure[2])
            if atmos_pressure[3] != 'nan':
                x.x2.append(atmos_pressure[3])
            if temp_mean[3] != 'nan':
                x.x3.append(temp_mean[3])
            if atmos_pressure[4] != 'nan':
                x.x4.append(atmos_pressure[4])
            if temp_mean[4] != 'nan':
                x.x5.append(temp_mean[4])
            if rh_mean[4] != 'nan':
                x.x6.append(rh_mean[4])
            if atmos_pressure[5] != 'nan':
                x.x7.append(atmos_pressure[5])
            if temp_mean[5] != 'nan':
                x.x8.append(temp_mean[5])
            if rh_mean[5] != 'nan':
                x.x9.append(rh_mean[5])
            if vapor_pressure_mean[5] != 'nan':
                x.x10.append(vapor_pressure_mean[5])
            if atmos_pressure[6] != 'nan':
                x.x11.append(atmos_pressure[6])
            if temp_mean[6] != 'nan':
                x.x12.append(temp_mean[6])
            if rh_mean[6] != 'nan':
                x.x13.append(rh_mean[6])
            if vapor_pressure_mean[6] != 'nan':
                x.x14.append(vapor_pressure_mean[6])
            if wspd_arith_mean[6] != 'nan':
                x.x15.append(wspd_arith_mean[6])

# Main
def main(argv):
    x = X()
    path = "/Users/ylk/Documents/GitHub/arm/csv.files"
    inst = "E"
    readCSVFile(path, inst, x)

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(16, 6))
    all_data = []
    all_data.append(np.array(x.x1).astype(np.float))
    all_data.append(np.array(x.x2).astype(np.float))
    all_data.append(np.array(x.x3).astype(np.float))
    all_data.append(np.array(x.x4).astype(np.float))
    all_data.append(np.array(x.x5).astype(np.float))
    all_data.append(np.array(x.x6).astype(np.float))
    all_data.append(np.array(x.x7).astype(np.float))
    all_data.append(np.array(x.x8).astype(np.float))
    all_data.append(np.array(x.x9).astype(np.float))
    all_data.append(np.array(x.x10).astype(np.float))
    all_data.append(np.array(x.x11).astype(np.float))
    all_data.append(np.array(x.x12).astype(np.float))
    all_data.append(np.array(x.x13).astype(np.float))
    all_data.append(np.array(x.x14).astype(np.float))
    all_data.append(np.array(x.x15).astype(np.float))

    # plot violin plot
    axes.violinplot(all_data, showmeans=False, showmedians=True)
    axes.set_title('Violin plot: 6 variables from sgpmet with one day lag')

    # adding horizontal grid lines
    axes.yaxis.grid(True)
    axes.set_xticks([y + 1 for y in range(len(all_data))])
    axes.set_xlabel('Pearson Correlation')
    axes.set_ylabel('Threshold')

    # Shrink current axis by 25%
    box = axes.get_position()
    axes.set_position([box.x0, box.y0, box.width * 0.75, box.height])

    # add x-tick labels
    plt.setp(axes, xticks=[y + 1 for y in range(len(all_data))],
             xticklabels=['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', \
             'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15'])
    plt.legend(['x1: atmos_pressure & temp_mean', \
        'x2: atmos_pressure & rh_mean', \
        'x3: temp_mean & rh_mean', \
        'x4: atmos_pressure & vapor_pressure_mean', \
        'x5: temp_mean & vapor_pressure_mean', \
        'x6: rh_mean & vapor_pressure_mean', \
        'x7: atmos_pressure & wspd_arith_mean', \
        'x8: temp_mean & wspd_arith_mean', \
        'x9: rh_mean & wspd_arith_mean', \
        'x10: vapor_pressure_mean & wspd_arith_mean', \
        'x11: atmos_pressure & tbrg_precip_total_corr', \
        'x12: temp_mean & tbrg_precip_total_corr', \
        'x13: rh_mean & tbrg_precip_total_corr', \
        'x14: vapor_pressure_mean & tbrg_precip_total_corr', \
        'x15: wspd_arith_mean & tbrg_precip_total_corr'], \
        loc='center left', bbox_to_anchor=(1.05, 0.5))
    plt.show()

    print("Done", file=sys.stderr)
    return 0

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
