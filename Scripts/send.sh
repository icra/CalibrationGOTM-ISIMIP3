#!/bin/sh 
#SBATCH --nodelist=compute-12
#SBATCH --ntasks=8 

##SBATCH --cpus-per-task=1 
##SBATCH --mem-per-cpu=512M


./correr_gotam_todo.sh
