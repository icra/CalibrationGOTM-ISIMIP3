#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 09:20:29 2023

@author: daniel
"""

import pandas as pd
import xarray as xr
import numpy as np
import os
import math
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

pwd = os.getcwd()
lake_name = os.path.basename(pwd)

lake_ds = xr.load_dataset('outputxr.nc')
time_np = lake_ds['time'].values
z_np = lake_ds['z'].values
#
start_time ='1881-01-01'
end_time = '2021-12-31'
start_decade = np.where(time_np==np.datetime64(start_time))
end_decade = np.where(time_np==np.datetime64(end_time))
time_all = np.arange(np.datetime64(start_time), np.datetime64(end_time)+1)

variable_name='temp'
#lake_np_surf = lake_ds.sel(z=z_np[-1])[variable_name].valuesç
#mean value of the first 3 depths
lake_np_surf = np.mean(lake_ds.sel(z=z_np[-11:])[variable_name].values, axis=1)
#lake_np_bott = lake_ds.sel(z=z_np[0])[variable_name].values
#mean value of the last 3 depths
lake_np_bott = np.mean(lake_ds.sel(z=z_np[0:11])[variable_name].values, axis=1)

df_surf = {'date': time_all, 'stemp': lake_np_surf.squeeze()}
df_surf = pd.DataFrame(df_surf)

df_bott = {'date': time_all, 'btemp': lake_np_bott.squeeze()}
df_bott = pd.DataFrame(df_bott)

#Observed data:
temp_obs = pd.read_csv('temp_daily.csv')
temp_obs = pd.DataFrame(temp_obs)
temp_obs['date'] = pd.to_datetime(temp_obs['TIMESTAMP'], format='%Y%m%d')
surf_rows = temp_obs[(temp_obs['DEPTH'] >= 0) & (temp_obs['DEPTH'] <= 5)][['date', 'DEPTH','WTEMP']]
surf_rows = surf_rows.groupby('date')['WTEMP'].mean().reset_index()

with open('gotm.yaml', 'r') as file:
    lines = file.readlines()
z_bott = int(lines[5].split(':')[1].strip())

bott_rows = temp_obs[(temp_obs['DEPTH'] <= z_bott) & (temp_obs['DEPTH'] >= (z_bott-5))][['date', 'DEPTH','WTEMP']]
bott_rows = bott_rows.groupby('date')['WTEMP'].mean().reset_index()

#plots
#plt.plot(time_all[range_plot],lake_np_surf.squeeze()[range_plot])
#plt.plot(time_all[range_plot],lake_np_bott.squeeze()[range_plot])
#plt.scatter(surf_rows['date'][0:11], surf_rows['WTEMP'][0:11])
#plt.show()

#plt.plot(time_all[range_plot],lake_np_surf.squeeze()[range_plot])
#plt.plot(time_all[range_plot],lake_np_bott.squeeze()[range_plot])
#plt.scatter(surf_rows['date'][0:11], surf_rows['WTEMP'][0:11])
#plt.scatter(bott_rows['date'][0:11], bott_rows['WTEMP'][0:11])


#stats:
surf_merged = pd.merge(surf_rows, df_surf, on='date', how='inner')
bott_merged = pd.merge(bott_rows, df_bott, on='date', how='inner')

# Assuming you have your merged DataFrame as 'merged_df'

#SURFACE
# Extract the 'WTEMP' and 'stemp' columns
observed = surf_merged['stemp']
simulated = surf_merged['WTEMP']

try:
    # Calculate NSE (Nash-Sutcliffe Efficiency)
    nse = 1 - (np.sum((observed - simulated) ** 2) / np.sum((observed - np.mean(observed)) ** 2))

    # Calculate KGE (Kling-Gupta Efficiency)
    mean_observed = np.mean(observed)
    mean_simulated = np.mean(simulated)
    std_observed = np.std(observed)
    std_simulated = np.std(simulated)

    kge = 1 - np.sqrt((r2_score(observed, simulated) - 1) ** 2 + (std_simulated / std_observed - 1) ** 2 + (mean_simulated / mean_observed - 1) ** 2)

    # Calculate RMSE (Root Mean Square Error)
    rmse = np.sqrt(mean_squared_error(observed, simulated))

    # Calculate R2 (R-squared)
    r2 = r2_score(observed, simulated)

    print(f'NSE: {nse:.4f}')
    print(f'KGE: {kge:.4f}')
    print(f'RMSE: {rmse:.4f}')
    print(f'R2: {r2:.4f}')
    
    stats_df = pd.DataFrame({'NSE': [nse], 'KGE': [kge], 'RMSE': [rmse], 'R2': [r2]})

except Exception as e:    
    stats_df = pd.DataFrame({'NSE': ['NaN'], 'KGE': ['NaN'], 'RMSE': ['NaN'], 'R2': ['NaN']})

stats_df.to_csv('statistics.csv', index=False)

text_message = f'NSE: {nse:.2f}\nKGE: {kge:.2f}\nRMSE: {rmse:.2f}\nR2: {r2:.2f}'

# Define linear regression parameters
m = 1
b = 0

# Generate points for the linear regression line
regression_x = np.array(range(math.floor(min(surf_merged['stemp'])), math.ceil(max(surf_merged['stemp']))))
regression_y = m * regression_x + b


plt.scatter(surf_merged['stemp'], surf_merged['WTEMP'])
plt.xlabel('Observed')
plt.ylabel('Simulated')
#plt.title(lake_name)
plt.text(0.8, 0.1, text_message, transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.7))
# Plot the linear regression line
plt.plot(regression_x, regression_y, label='Linear Regression', linestyle='--', color='red')
plt.savefig('Surf_Obs-Sim.pdf')
plt.show()

#BOTTOM
# Extract the 'WTEMP' and 'stemp' columns
observed = bott_merged['btemp']
simulated = bott_merged['WTEMP']

try:
    # Calculate NSE (Nash-Sutcliffe Efficiency)
    nse = 1 - (np.sum((observed - simulated) ** 2) / np.sum((observed - np.mean(observed)) ** 2))

    # Calculate KGE (Kling-Gupta Efficiency)
    mean_observed = np.mean(observed)
    mean_simulated = np.mean(simulated)
    std_observed = np.std(observed)
    std_simulated = np.std(simulated)

    kge = 1 - np.sqrt((r2_score(observed, simulated) - 1) ** 2 + (std_simulated / std_observed - 1) ** 2 + (mean_simulated / mean_observed - 1) ** 2)

    # Calculate RMSE (Root Mean Square Error)
    rmse = np.sqrt(mean_squared_error(observed, simulated))

    # Calculate R2 (R-squared)
    r2 = r2_score(observed, simulated)

    print(f'NSE: {nse:.4f}')
    print(f'KGE: {kge:.4f}')
    print(f'RMSE: {rmse:.4f}')
    print(f'R2: {r2:.4f}')

    stats_df = pd.DataFrame({'NSE': [nse], 'KGE': [kge], 'RMSE': [rmse], 'R2': [r2]})

    text_message = f'NSE: {nse:.2f}\nKGE: {kge:.2f}\nRMSE: {rmse:.2f}\nR2: {r2:.2f}'

    # Define linear regression parameters
    m = 1
    b = 0

    # Generate points for the linear regression line
    regression_x = np.array(range(math.floor(min(bott_merged['btemp'])), math.ceil(max(bott_merged['btemp']))))
    regression_y = m * regression_x + b

    plt.scatter(bott_merged['btemp'], bott_merged['WTEMP'])
    plt.xlabel('Observed')
    plt.ylabel('Simulated')
    #plt.title(lake)
    plt.text(0.8, 0.1, text_message, transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.7))
    # Plot the linear regression line
    plt.plot(regression_x, regression_y, label='Linear Regression', linestyle='--', color='red')
    plt.savefig('Bott_Obs-Sim.pdf')

except Exception as e:
    stats_df = pd.DataFrame({'NSE': ['NaN'], 'KGE': ['NaN'], 'RMSE': ['NaN'], 'R2': ['NaN']})

stats_df.to_csv('statistics_bott.csv', index=False)

