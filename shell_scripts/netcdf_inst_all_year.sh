#!/bin/bash

# Shell script to run netcdf_inst_all_year.py in batch
# Usage : nohup ./netcdf_inst_all_year.sh > foo.out 2> foo.err < /dev/null &
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Feb 07 2018

array=(1 3 4 5 6 7 8 9 11 13 15 20 21 24 25 27 31 32 33 34 35 36 37 38 39 40 41)

for number in ${array[@]}
do
    path="/data/archive/sgp/sgpmetE"$number".b1"
    inst="E"$number
    python3 netcdf_inst_all_year.py $path $inst 1993 2017
done


