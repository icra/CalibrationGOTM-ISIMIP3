#!/bin/bash

# Directorio de origen
origen="/home/ollorente/local_lakes_climate/20CRv3-ERA5_test"

# Directorio de destino
destino="/home/ollorente/local_lakes_climate/default_calibration"

# Buscar subdirectorios en el directorio de origen
find "$origen" -mindepth 1 -maxdepth 1 -type d | while read subdir; do
    # Extraer el nombre del subdirectorio
    dir_name=$(basename "$subdir")
    
    # Crear el directorio correspondiente en el directorio de destino
    mkdir -p "$destino/$dir_name"
    
    # Copiar los archivos que cumplan con los criterios
    cp "$subdir"/*.pdf "$subdir"/statistics.csv "$subdir"/statistics_bott.csv "$destino/$dir_name/" 2>/dev/null
done

