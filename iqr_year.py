#!/usr/bin/env python3
# Script to output outliers of pearson correlations of sgpmet data
# Usage : python iqr_year.py
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Jan 29 2018

# Load libs
import sys
import numpy as np
#import matplotlib.pyplot as plt
import csv
import fnmatch
import os

# Class to store the correlations
class X:
    def __init__(self):
        self.pc = [] # pearson correlation value
        self.year = [] # year
        self.inst = [] # instrument name

# Read CSV file
def readCSVFile(path, inst, x1, x2, x3, x4, x5, x6, x7, \
    x8, x9, x10):
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
            x1.pc.append(atmos_pressure[2])
            x1.year.append(year)
            x1.inst.append(inst)
            x2.pc.append(atmos_pressure[3])
            x2.year.append(year)
            x2.inst.append(inst)
            x3.pc.append(temp_mean[3])
            x3.year.append(year)
            x3.inst.append(inst)
            x4.pc.append(atmos_pressure[4])
            x4.year.append(year)
            x4.inst.append(inst)
            x5.pc.append(temp_mean[4])
            x5.year.append(year)
            x5.inst.append(inst)
            x6.pc.append(rh_mean[4])
            x6.year.append(year)
            x6.inst.append(inst)
            x7.pc.append(atmos_pressure[5])
            x7.year.append(year)
            x7.inst.append(inst)
            x8.pc.append(temp_mean[5])
            x8.year.append(year)
            x8.inst.append(inst)
            x9.pc.append(rh_mean[5])
            x9.year.append(year)
            x9.inst.append(inst)
            x10.pc.append(vapor_pressure_mean[5])
            x10.year.append(year)
            x10.inst.append(inst)

# IQR method
def outliers_iqr(x, varname):
    cnt = 0
    quartile_1, quartile_3 = np.percentile(x.pc, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)
    for i in range(len(x.pc)):
        if (x.pc[i] > upper_bound) | (x.pc[i] < lower_bound):
            print(x.inst[i], x.year[i], x.pc[i])
            cnt += 1
    if cnt > 0:
        print("-----", varname, " -----done")
        print()

# Main
def main(argv):
    x1 = X()
    x2 = X()
    x3 = X()
    x4 = X()
    x5 = X()
    x6 = X()
    x7 = X()
    x8 = X()
    x9 = X()
    x10 = X()
    path = "/Users/ylk/Documents/GitHub/arm/csv.files"
    inst = "E"

    readCSVFile(path, inst, x1, x2, x3, x4, x5, x6, x7, \
    x8, x9, x10)
    # convert data into np array
    x1.pc = np.array(x1.pc).astype(np.float)
    x2.pc = np.array(x2.pc).astype(np.float)
    x3.pc = np.array(x3.pc).astype(np.float)
    x4.pc = np.array(x4.pc).astype(np.float)
    x5.pc = np.array(x5.pc).astype(np.float)
    x6.pc = np.array(x6.pc).astype(np.float)
    x7.pc = np.array(x7.pc).astype(np.float)
    x8.pc = np.array(x8.pc).astype(np.float)
    x9.pc = np.array(x9.pc).astype(np.float)
    x10.pc = np.array(x10.pc).astype(np.float)

    outliers_iqr(x1, "x1: atmos_pressure & temp_mean")
    outliers_iqr(x2, "x2: atmos_pressure & rh_mean")
    outliers_iqr(x3, "x3: temp_mean & rh_mean")
    outliers_iqr(x4, "x4: atmos_pressure & vapor_pressure_mean")
    outliers_iqr(x5, "x5: temp_mean & vapor_pressure_mean")
    outliers_iqr(x6, "x6: rh_mean & vapor_pressure_mean")
    outliers_iqr(x7, "x7: atmos_pressure & wspd_arith_mean")
    outliers_iqr(x8, "x8: temp_mean & wspd_arith_mean")
    outliers_iqr(x9, "x9: rh_mean & wspd_arith_mean")
    outliers_iqr(x10, "x10: vapor_pressure_mean & wspd_arith_mean")

'''
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(16, 6))
    all_data = []
    all_data.append(x1.pc)
    all_data.append(x2.pc)
    all_data.append(x3.pc)
    all_data.append(x4.pc)
    all_data.append(x5.pc)
    all_data.append(x6.pc)
    all_data.append(x7.pc)
    all_data.append(x8.pc)
    all_data.append(x9.pc)
    all_data.append(x10.pc)

    # plot violin plot
    axes.violinplot(all_data, showmeans=False, showmedians=True)
    axes.set_title('Violin plot: 5 variables from sgpmet')

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
             xticklabels=['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'])
    plt.legend(['x1: atmos_pressure & temp_mean', \
        'x2: atmos_pressure & rh_mean', \
        'x3: temp_mean & rh_mean', \
        'x4: atmos_pressure & vapor_pressure_mean', \
        'x5: temp_mean & vapor_pressure_mean', \
        'x6: rh_mean & vapor_pressure_mean', \
        'x7: atmos_pressure & wspd_arith_mean', \
        'x8: temp_mean & wspd_arith_mean', \
        'x9: rh_mean & wspd_arith_mean', \
        'x10: vapor_pressure_mean & wspd_arith_mean'], \
        loc='center left', bbox_to_anchor=(1.05, 0.5))
    plt.show()

    print("Done", file=sys.stderr)
    return 0
'''
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
