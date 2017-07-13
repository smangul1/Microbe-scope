#!/bin/sh
#$ -S /bin/bash
#$ -N job-bwa-mem_malser
#$ -cwd
#$ -M mealser@gmail.com
#$ -m abe
#$ -l h_data=15G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa

bwa index /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi_ConcatContigs.fa

bwa mem -a /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi_ConcatContigs.fa /u/home/galaxy/collaboratory/serghei/MetaSUB-Inter-City-Challenge/data/SRR3546361.fastq | awk '$3!="*"' 
 > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/SRR3546361_MergedContigs_Filtered.sam

sort -t$'\t' -k 1,1 -V -k 3,3 SRR3546361_MergedContigs_Filtered.sam > SRR3546361_MergedContigs_Sorted.sam