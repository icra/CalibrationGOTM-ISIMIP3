#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os
import multiprocessing
import warnings
import csv

warnings.filterwarnings("ignore")

# Path to the directory containing the folders/lakes
directory = "/home/dmercado/calibration_local_lakes/lakes_cal"

column_names = ["Date", "Hour", "Depth", "Temp"]

def closest_value_to(lst, target):
    lst_lst = lst.tolist()
    if min(abs(lst - (target))) <= 1:
        closest = lst_lst.index(min(lst_lst, key=lambda x: abs(x - target)))
    else:
        return 'nan'
    
    return closest

def process_folder(folder):
    print('Starts ' + folder)
    folder_path = os.path.join(directory, folder)
    file_path_table = os.path.join(folder_path, "table.csv")
    file_path_tempobs = os.path.join(folder_path, "temp_all.obs")
    temp_obs = pd.read_csv(file_path_tempobs, sep=' ', header=None, names=column_names)
    table = pd.read_csv(file_path_table)
    table_obs = pd.DataFrame() 
    for date in table['Date'].unique():
        pos_date = table.index[table['Date'] == date].tolist()
        if date in temp_obs['Date'].values:
            print(date)
            pos_date_obs = temp_obs.index[temp_obs['Date'] == date].tolist()
            depths_date = table['Depth'][pos_date]
            depths_date_obs = temp_obs['Depth'][pos_date_obs]
            for depth in depths_date:
                pos_date_depth = depths_date.index[depths_date == depth]
                if depth in depths_date_obs.values:
                    pos_depth = depths_date_obs.index[depths_date_obs == depth].tolist()
                    to_append = table.iloc[pos_date_depth]
                    to_append['Temp_obs'] = temp_obs['Temp'][pos_depth].values
                    table_obs = pd.concat([table_obs, to_append])
                else:
                    pos_depth_noexact = closest_value_to(depths_date_obs.values, depth)
                    to_append = table.iloc[pos_date_depth]
                    if pos_depth_noexact=='nan':
                        to_append['Temp_obs'] = np.nan
                    else:
                        to_append['Temp_obs'] = temp_obs['Temp'][pos_depth_noexact]
                    table_obs = pd.concat([table_obs, to_append])
                
        else:
            to_append = table.iloc[pos_date]
            to_append['Temp_obs'] = np.nan
            table_obs = pd.concat([table_obs, to_append])
    
    #table_obs = np.array(table_obs[0])
    #table_obs = np.squeeze(table_obs)
    #df = pd.DataFrame(table_obs)i
    file_path_save = os.path.join(folder_path, "table_obs.csv")
    #with open(file_path_save, mode='w', newline='') as file:
    #    csv.writer = csv.writer(file)
    #    csv.writer.writerows(table_obs)
    table_obs.to_csv(file_path_save, index=False, header=["date", "depth", "mod", "obs"])
    print('Ended ' +  folder)

if __name__ == "__main__":
    num_processes = 36 #multiprocessing.cpu_count()  # Number of CPU cores
    pool = multiprocessing.Pool(processes=num_processes)
    folders = os.listdir(directory)
    pool.map(process_folder, folders)
    pool.close()
    pool.join()
