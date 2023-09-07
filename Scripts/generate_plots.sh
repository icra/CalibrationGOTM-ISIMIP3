
#!/bin/bash

ml nco-4.6.7-gcc-4.9.4-z6lh2ni


# Ruta a la carpeta base
base_folder="/home/ollorente/local_lakes_climate/20CRv3-ERA5_test"

# Comando que deseas ejecutar
command="singularity exec /home/ollorente/local_lakes_climate/scripts/container/ python3 /home/ollorente/local_lakes_climate/scripts/plot_stats.py"

# Iterar a través de las carpetas
for folder in "$base_folder"/*; do
    if [ -d "$folder" ]; then
        cd "$folder"
        rm outputxr.nc
        ncrename -v z,z_coord output.nc outputxr.nc
        # Verificar si es una carpeta antes de ejecutar el comando
        echo "Entrando en la carpeta: $folder"
        $command
    fi
done

