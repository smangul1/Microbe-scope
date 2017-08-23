#!/bin/sh
#$ -S /bin/bash
#$ -N job-Check-Duplication-bacteria_malser
#$ -cwd
#$ -M mealser@gmail.com
#$ -m abe
#$ -l h_data=15G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load python/3.6.1

python3 /u/project/zarlab/malser/MiCoP/Scripts/CheckDuplicationFromRefSeqFolder.py /u/scratch2/scratch2/m/malser/NCBI-RefSeq /u/scratch2/scratch2/m/malser/EuPathDB_Organism_List.txt bacteria  >> /u/scratch2/scratch2/m/malser/RemovedDuplicatesFrom_bacteria.txt
