#!/bin/bash

# Ruta al primer directorio
dir_origen="/home/ollorente/local_lakes_climate/20CRv3-ERA5_test2"

# Ruta al segundo directorio
dir_destino="/home/ollorente/local_lakes_climate/20CRv3-ERA5_test"

# Itera a través de las carpetas en el primer directorio
for carpeta in "$dir_origen"/*/; do
    if [ -d "$carpeta" ]; then
        # Extrae el nombre de la carpeta sin la ruta
        nombre_carpeta=$(basename "$carpeta")
        
        # Copia el archivo "temp_daily.csv" desde el primer directorio al segundo
        cp "$carpeta/temp_daily.csv" "$dir_destino/$nombre_carpeta/"
        
        echo "Archivo copiado desde $carpeta a $dir_destino/$nombre_carpeta/"
    fi
done

