#!/bin/bash

# Shell script to run sgpmet_pearson_seaon.py in batch
# Usage : nohup ./sgpmet_pearson_season.sh > foo.out 2> foo.err < /dev/null &
# Author: Yuping Lu yupinglu89@gmail.com
# Date  : Jan 18 2018

array=(1 3 4 5 6 7 8 9 11 13 15 20 21 24 25 27 31 32 33 34 35 36 37 38 39 40 41)

for number in ${array[@]}
do
    path="/data/archive/sgp/sgpmetE"$number".b1"
    inst="E"$number
    for year in {1993..2017}
    do
    	python3 sgpmet_pearson_season.py $path $inst $year
    done
done


