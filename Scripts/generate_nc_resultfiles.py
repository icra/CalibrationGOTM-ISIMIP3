#!/usr/bin/env python3

import os
import xarray as xr
import pandas as pd
import numpy as np
from multiprocessing import Pool

def process_folder(folder):
    folder_path = os.path.join(directory, folder)
    print(folder_path)
    
    if os.path.isdir(folder_path):
        file_path = os.path.join(folder_path, "outputxr.nc")
        
        if os.path.exists(file_path):
            ds = xr.open_dataset(file_path)
            dates = ds['time'].values
            depths = ds['z_coord'].values
            temperatures = ds['temp'].values
            depths = np.squeeze(depths)
            temperatures = np.squeeze(temperatures)

            dates_list = []
            depths_list = []
            temperatures_list = []

            for i in range(len(dates)):
                for j in range(len(depths[i])):
                    date_current = pd.to_datetime(dates[i]).date()
                    if date_current.year > (pd.to_datetime(dates[0]).year + 19):
                        depth_current = depths[i][j]
                        temperature_current = temperatures[i][j]
                        dates_list.append(date_current)
                        depths_list.append(depth_current)
                        temperatures_list.append(temperature_current)

            data = {
                'Date': dates_list,
                'Depth': depths_list,
                'Temp': temperatures_list
            }

            df = pd.DataFrame(data)
            df = df.groupby('Date', group_keys=False).apply(lambda x: x[::-1])

            print("saving", folder_path, "file")
            df.to_csv(os.path.join(folder_path, "table.csv"), index=False)
            print(folder_path, "saved!")

if __name__ == '__main__':
    # Path to the directory containing the folders/lakes
    directory = "/home/dmercado/calibration_local_lakes/lakes_cal"
    #directory = "/home/dmercado/calibration_local_lakes/lakes_default"
    
    # Get a list of folders in the directory
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]

    # Specify the number of parallel processes (adjust as needed)
    num_processes = 30

    # Create a multiprocessing pool and process the folders in parallel
    with Pool(num_processes) as pool:
        pool.map(process_folder, folders)

