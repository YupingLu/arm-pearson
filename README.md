# Explanation of steps and codes

This is a simple explanation of our analysis using pearson correlation and how to execute the codes. Three types of pearson correlation are calculated. 1) met correlation without qc_tbrg_precip_total_corr 2) met correlation with qc_tbrg_precip_total_corr 3) met correlation with qc_tbrg_precip_total_corr and one day lag

1. Calculate the year-round pearson correlations of all instruments from 1993 to 2017
```
  sgpmet_pearson.py: python sgpmet_pearson.py path instrument year
  # Run sgpmet_pearson.py in batch
  sgpmet_pearson.sh: nohup ./sgpmet_pearson.sh > foo.out 2> foo.err < /dev/null &
  # Pearson correlation files are stored in year.pc.csv
```
2. Calculate the seasonal pearson correlations of all instruments from 1993 to 2017
```
  sgpmet_pearson_season.py: python sgpmet_pearson_season.py path instrument year
  # Run sgpmet_pearson_season.py in batch
  sgpmet_pearson_season.sh: nohup ./sgpmet_pearson_season.sh > foo.out 2> foo.err < /dev/null &
  # Pearson correlation files are stored in season.pc.csv
```
3. Use violin plot to visualize the year-round pearson correlations
```
  csvplot.py: python csvplot.py
  csvplot.1.py: python csvplot.1.py
  csvplot.2.py: python csvplot.2.py
  # Output files are stored in figures
```
4. Use violin plot to visualize the seaonal pearson correlations
```
  csvplot.season.py: python csvplot.season.py
  csvplot.season.1.py: python csvplot.season.1.py    
  csvplot.season.2.py: python csvplot.season.2.py  
  # Output files are stored in figures
```
5. Read all instruments data averaged by day for plotly
```
  # Script to get netcdf data for 1 inst 1 year.
  netcdf_inst_1_year.py: python netcdf_inst_1_year.py path instrument year
  # Script to get netcdf data for 1 inst from 1993 to 2017.
  netcdf_inst_all_year.py: python netcdf_inst_all_year.py path instrument begin_year end_year
  # Run netcdf_inst_all_year.py in batch
  netcdf_inst_all_year.sh: nohup ./netcdf_inst_all_year.sh > foo.out 2> foo.err < /dev/null &
  # Output files are stored in netcdf_year_viz
```
6. Use modified z scores method to calculate the outliers
```
  outliers_iqr_year.py: python outliers_iqr_season.py
  # Output files are stored in outliers/modified_z_score_season
  outliers_iqr_season.py: python outliers_iqr_year.py
  # Output files are stored in outliers/modified_z_score_year
```
7. Use plotly to visualize all instruments data
```
  # Input data is from step 5
  # Script to plot netcdf data from netcdf_inst_*_year.py
  netcdf_plot.py: python netcdf_plot.py
  # Script to plot netcdf data from netcdf_inst_*_year.py in batch
  netcdf_plot_batch.py: python netcdf_plot_batch.py
  # Output files are stored in plotly/netcdf_plot
```
8. Use plotly to visualize all instruments data with outliers(season)
```
  # Input data is from step 5 and step 6
  # Script to plot netcdf data with seasonal outliers from netcdf_inst_*_year.py in batch
  netcdf_plot_season_outlier.py: python netcdf_plot_season_outlier.py
  # Output files are stored in plotly/netcdf_plot_modified_z_score_outlier
```                                     
Reference Paper
---------------
Y. Lu, J. Kumar, N. Collier, B. Krishna and M. A. Langston, "Detecting Outliers in Streaming Time Series Data from ARM Distributed Sensors," 2018 IEEE International Conference on Data Mining Workshops (ICDMW), Singapore, Singapore, 2018, pp. 779-786, doi: 10.1109/ICDMW.2018.00117.                 
