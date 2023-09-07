import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import xarray as xr
from math import pi
from pathlib import Path

directorio_actual = os.getcwd()

# Lista todos los archivos en el directorio actual
archivos_en_directorio = os.listdir(directorio_actual)

# Encuentra el primer archivo que contiene "obsclim" en su nombre
archivo_con_obsclim = next((archivo for archivo in archivos_en_directorio if "obsclim" in archivo), None)

lake_df = pd.read_csv(archivo_con_obsclim)

#-------------------------------------------------

lake_name_style = r'obsclim_(\w+)_daily'
lake_name = resultado = re.search(lake_name_style, archivo_con_obsclim).group(1)

coordinates_df = pd.read_excel("/home/ollorente/local_lakes_climate/scripts/ISIMIP3_Lake_Sector_Contributions.xlsx", sheet_name="MetaData Hydrothermal")

filtered_row = coordinates_df[coordinates_df["Lake Name in file name (reporting)"].str.contains(lake_name, case=False)]

coordinates_long= filtered_row["longitude (dec deg)"].values[0]
coordinates_elv = filtered_row["elevation (m)"].values[0]
coordinates_lat = filtered_row["latitude (dec deg)"].values[0]

#-------------------------------------------------

def calc_cc_dewp(date, airt, relh, swr, lat, lon, elev):
  
  date = pd.to_datetime(date, format='%d/%m/%Y %H:%M:%S')
  date = pd.date_range(start=date[0],end=(date[-1]+datetime.timedelta(days = 1)-datetime.timedelta(hours = 1)),freq='H')
    

  yday = np.array(date.dayofyear)
  
  hour = np.array(date.hour)
  hour[hour==0]=24

  stdmer = range(-180,180, 15)
  Lsm = stdmer[np.argmin([abs(lon-x) for x in list(stdmer)])] # Local standard meridian (degrees)

  Hsc = 1390 # Solar constant (W/m2)
  cd = 0.06 # Dust coefficient
  Rg = 0.045 # Reflectivity of the ground - extended mixed forest


  theta = lat*pi/180 # Latitude in radians

  r = 1 + 0.017 * np.cos((2*pi/365)*(186-yday)) # Relative earth-sun distance

  d = 23.45 * pi/180 * np.cos((2*pi/365)*(172-yday)) # Declination of the sun

  dts = (1/15) * (Lsm-lon) # Fraction of 15-degree increment Llm is east of Lsm
  value = (np.sin(theta)*np.sin(d))
  value = value/(np.cos(theta)*np.cos(d))
  
  value[value > 1] = 1
  value[value < -1] = -1

  tss = (12/pi) * np.arccos(-value) + dts + 12 # Time of sunset
  tsu = -tss + (2 * dts) + 24 # Time of sunrise

  gamma = np.repeat(0, len(tss)) # Correction factor
  dum = np.where(np.logical_and(hour>tsu, hour<tss))
  gamma[dum] = 1

  #Calculate Hb and Htheta
  dum1 = np.where(hour <=12 )
  dum2 = np.where(hour > 12 )
  hb1  = pi/12*(hour-1-dts)
  hb1[dum1] = hb1[dum1]+pi
  hb1[dum2] = hb1[dum2]-pi
  hb  = hb1
  dum3 = np.where(hb1 > 2*pi)
  hb[dum3] = hb[dum3] - 2 * pi
  dum4 = np.where(hb1 < 0)
  hb[dum4] = hb[dum4] + 2 * pi
  #rm(c(dum3, dum4))
  he1  = pi/12*(hour-dts)
  he1[dum1] = he1[dum1]+pi
  he1[dum2] = he1[dum2]-pi
  he  = he1
  dum3 = np.where(he1 > 2*pi)
  he[dum3] = he[dum3] - 2*pi
  dum4 = np.where(he1 < 0)
  he[dum4] = he[dum4] + 2*pi
  #clear dum1 dum2 dum3 dum4

  Ho = Hsc/(r**2)*(np.sin(theta)*np.sin(d)+12/pi*np.cos(theta)*np.cos(d)*(np.sin(he)-np.sin(hb)))*gamma

  # Radiation scattering and absorption #####################################

  w = (he+hb)/2 # Hour angle
  alpha1 = abs(np.sin(theta)*np.sin(d)+np.cos(theta)*np.cos(d)*np.cos(w))
  alpha = np.arctan(alpha1/np.sqrt(1-alpha1**2)) # Solar altitude

  theta_am1 = ((288-0.0065*elev)/288)**5.256
  theta_am2 = np.sin(alpha)+0.15*((alpha*180/pi)+3.855)**(-1.253)
  theta_am = theta_am1/theta_am2 # Optical air mass

  # Dewpoint temperature
  dewt_daily = 243.04*(np.log(relh/100)+((17.625*airt)/(243.04+airt)))/(17.625-np.log(relh/100)-((17.625*airt)/(243.04+airt)))
  dewt_hourly = np.repeat(dewt_daily, 24)  

  Pwc = 0.85*np.exp(0.11+0.0614*dewt_hourly) # Precipitable atmospheric water content

  a2 = np.exp(-(0.465+0.134*Pwc)*(0.179+0.421*np.exp(-0.721*theta_am))*theta_am) # Atmospheric transmission coefficient after scattering and absorption
  a1 = np.exp(-(0.465+0.134*Pwc)*(0.129+0.171*np.exp(-0.88*theta_am))*theta_am)
  at = (a2+0.5*(1-a1-cd))/(1-0.5*Rg*(1-a1-cd)) # attenuation (scattering and absorption)
  #att = mean(at)

  Ho = at*Ho
  #Ho = att*Ho

  dum5 = np.where(Ho<0)
  Ho[dum5] = 1

  
  Ho_daily = np.average(Ho.reshape(-1, 24), axis=1)  
  
  ccsim = np.empty(len(Ho_daily))
  ccsim[:] = np.nan
  for i in range(0,len(Ho_daily)):
    if Ho_daily[i] > swr[i]:
        ccsim[i] = np.sqrt((1 - (swr[i]/Ho_daily[i]))/0.65)
  
  ccsim[ccsim > 1] = 1
  
  #this happens usually in winter in high latitudes, put a mean value of 0.5
  if np.isnan(ccsim[0]):
      ccsim[0] = 0.5
  if np.isnan(ccsim[-1]):
      ccsim[0] = 0.5

  ccsim = pd.DataFrame(ccsim).interpolate()
  ccsim = np.array(ccsim[0])
  
  ccsim[ccsim > 1] = 1
  

  return ccsim, dewt_daily

#-------------------------------------------------

res_df = pd.DataFrame()

res_df["!Date"] = lake_df["time"]
res_df["Hour"] = "12:00:00"
res_df["E_Wind_(m/s)"] = lake_df["sfcwind"].round(2)
res_df["N_Wind_(m/s)"] = 0.0
res_df["Barometric_P_(hPa)"] = (lake_df["ps"] / 100).round(2)
res_df["Ta_(C)"] = (lake_df["tas"] - 273.15).round(2)

lake_df["time"] = pd.to_datetime(lake_df["time"])
lake_df["time"] = lake_df["time"].dt.strftime("%d/%m/%Y")
lake_df["time_with_hour"] = lake_df["time"] + " 00:00:00"
date = pd.to_datetime(lake_df["time_with_hour"], format="%d/%m/%Y %H:%M:%S")
date = np.array(date)

clouds, td = calc_cc_dewp(date, np.array(res_df["Ta_(C)"]), np.array(lake_df["hurs"]), np.array(lake_df["rsds"]), np.array(coordinates_lat), np.array(coordinates_long), np.array(coordinates_elv))

res_df["Td_(C)"] = td.round(2)
res_df["Cloud_fract"] = clouds.round(2)


res_df["SolarRadiation_W/m2"] = lake_df["rsds"].round(2)
res_df["precipitation_m/s"] = (lake_df["pr"] / 1000)

#plt.figure(figsize=(10, 6))  # Opcional: ajusta el tamaño de la figura
#plt.plot(lake_df["pr"], label="Precipitación")
#plt.xlabel("Índice de Tiempo")
#plt.ylabel("Precipitación (m/s)")
#plt.title("Gráfico de Precipitación")
#plt.legend()
#plt.grid(True)
#plt.show()

res_df['!Date'] = pd.to_datetime(res_df['!Date'])

first_date = res_df['!Date'].min()

twenty_years_later = first_date + pd.DateOffset(years=20)

new_rows = res_df[(res_df['!Date'] >= first_date) & (res_df['!Date'] < twenty_years_later)].copy()

new_rows['!Date'] = new_rows['!Date'] - pd.DateOffset(years=20)

res_df = pd.concat([new_rows, res_df], ignore_index=True)

print(res_df)

res_df.to_csv("meteo_file.dat", sep=' ', index=False)

#-------------------------------------------------

file = "/home/ollorente/gotm.yaml"

with open(file, 'r') as archivo:
    lines = archivo.readlines()

df = pd.read_csv("hypsograph.dat", delimiter='\t', header=None)
depth = df.iloc[0, 0]

temperature = res_df.at[0, "Ta_(C)"]

if temperature < 0:
    temperature = 0
else:
    temperature.round(2)

for i, line in enumerate(lines):
    if "latitude:" in line:
        # Modifica la línea que contiene la latitud
        lines[i] = f"   latitude: {coordinates_lat.round(2)}\n"
    
    if "longitude:" in line:
        # Modifica la línea que contiene la latitud
        lines[i] = f"   longitude: {coordinates_long.round(2)}\n"

    if "depth:" in line:
        # Modifica la línea que contiene la latitud
        lines[i] = f"   depth: {math.ceil(depth)}\n"
    
    if "nlev:" in line:
        # Modifica la línea que contiene la latitud
        lines[i] = f"   nlev: {math.ceil(depth*2)}\n"

    if "t_1:" in line:
        # Modifica la línea que contiene la latitud
        lines[i] = f"      t_1: {temperature}\n"

    if "t_2:" in line:
        # Modifica la línea que contiene la latitud
        lines[i] = f"      t_2: {temperature}\n"

with open("gotm.yaml", 'w', newline='\n') as output_file:
    output_file.writelines(lines)


