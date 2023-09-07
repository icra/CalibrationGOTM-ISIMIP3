#!/bin/bash

# Rutas de las carpetas de origen y destino
carpeta_origen="/home/ollorente/local_lakes_climate/20CRv3_test"
carpeta_destino="/home/ollorente/local_lakes_climate/20CRv3-ERA5_test"

# Itera a través de las subcarpetas en la carpeta de origen
for subcarpeta in "$carpeta_origen"/*/; do
    if [ -d "$subcarpeta" ]; then
        # Extrae el nombre de la subcarpeta (nombre del lago)
        nombre_lago=$(basename "$subcarpeta")

        # Verifica si existe una subcarpeta con el mismo nombre en la carpeta de destino
        if [ -d "$carpeta_destino/$nombre_lago" ]; then
            # Copia el archivo "hypsograph.dat" si existe en la carpeta de origen
            if [ -f "$subcarpeta/hypsograph.dat" ]; then
                cp "$subcarpeta/hypsograph.dat" "$carpeta_destino/$nombre_lago/"
                echo "Se copió hypsograph.dat a $carpeta_destino/$nombre_lago/"
            else
                echo "No se encontró hypsograph.dat en $subcarpeta"
            fi
        else
            echo "No existe una subcarpeta con el nombre de lago correspondiente en $carpeta_destino"
        fi
    fi
done
