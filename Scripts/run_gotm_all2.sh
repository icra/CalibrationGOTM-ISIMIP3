#!/bin/bash

# Ruta al directorio principal que contiene los subdirectorios
directorio_principal="/home/ollorente/local_lakes_climate/20CRv3-ERA5_test2"

# Ruta al script que deseas ejecutar desde cada subdirectorio
script_a_ejecutar="/home/ollorente/run_gotm.sh"

# Nombre del archivo para registrar errores
archivo_errores="fail.txt"

# Itera a través de los subdirectorios en el directorio principal
for subdirectorio in "$directorio_principal"/*/; do
    if [ -d "$subdirectorio" ]; then
        # Entra al subdirectorio
        cd "$subdirectorio"

        # Ejecuta el script desde el subdirectorio
        if [ -f "$script_a_ejecutar" ]; then
            # Ejecuta el script y redirige la salida y los errores a un archivo temporal
            bash "$script_a_ejecutar" 2> tmp_stderr.txt

            # Verifica si hubo errores
            if [ $? -ne 0 ]; then
                # Guarda el nombre del archivo que dio error en el archivo de errores
                echo "Error en: $subdirectorio" >> "$archivo_errores"
            fi

            # Borra el archivo temporal de errores
            rm -f tmp_stderr.txt

            echo "Script ejecutado en: $subdirectorio"
        else
            echo "El archivo $script_a_ejecutar no existe en: $subdirectorio"
        fi

        # Regresa al directorio principal
        cd "$directorio_principal"
    fi
done

