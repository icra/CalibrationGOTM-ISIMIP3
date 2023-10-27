#!/bin/bash

#directorio_base="/home/dmercado/calibration_local_lakes/lakes_default"
directorio_base="/home/dmercado/calibration_local_lakes/lakes_cal"

# Luego, ejecutar el comando de Singularity independientemente de si se encontró el archivo o no
for subdirectorio in "$directorio_base"/*; do
    if [ -d "$subdirectorio" ]; then
        echo "Entrando en: $subdirectorio"
        cd "$subdirectorio" || exit
        if [ -f "outputxr.nc" ]; then
            rm outputxr.nc
            echo "Archivo 'outputxr.nc' eliminado en: $subdirectorio"
        else
            echo "No se encontró el archivo 'outputxr.nc' en: $subdirectorio"
        fi
        # Ejecutar el comando de Singularity independientemente de si se encontró el archivo o no
        singularity exec /home/dmercado/containers/ubuntu_container_parsac/ ncrename -v z,z_coord output.nc outputxr.nc
        echo "Comando ejecutado en: $subdirectorio"
        cd "$directorio_base" || exit
    fi
done

