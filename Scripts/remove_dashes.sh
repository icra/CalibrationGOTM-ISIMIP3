#!/bin/bash

# Ruta al directorio principal que contiene los subdirectorios
directorio_principal="/home/ollorente/local_lakes_climate/20CRv3-ERA5_test"

# Itera a través de los subdirectorios
for subdirectorio in "$directorio_principal"/*/; do
    if [ -d "$subdirectorio" ]; then
        # Extrae el nombre base del subdirectorio (sin la ruta)
        nombre_base=$(basename "$subdirectorio")

        # Elimina guiones (-) del nombre base
        nuevo_nombre="${nombre_base//-/}"

        # Renombra el subdirectorio
        if [ "$nombre_base" != "$nuevo_nombre" ]; then
            mv "$subdirectorio" "$directorio_principal/$nuevo_nombre"
            echo "Renombrado: $nombre_base -> $nuevo_nombre"
        fi
    fi
done
