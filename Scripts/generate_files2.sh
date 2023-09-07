
#!/bin/bash

# Ruta a la carpeta base
base_folder="/home/ollorente/local_lakes_climate/20CRv3-ERA5_test2"

# Comando que deseas ejecutar
command="singularity exec /home/ollorente/local_lakes_climate/scripts/container/ python3 /home/ollorente/local_lakes_climate/scripts/meteo_files_generator.py"

# Iterar a través de las carpetas
for folder in "$base_folder"/*; do
    if [ -d "$folder" ]; then
        # Verificar si es una carpeta antes de ejecutar el comando
        echo "Entrando en la carpeta: $folder"
        (cd "$folder" && $command)
    fi
done

