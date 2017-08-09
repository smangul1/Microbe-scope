#!/bin/sh
#$ -S /bin/bash
#$ -N job-BWA-Index_malser
#$ -M mealser@gmail.com
#$ -m abe
#$ -l h_data=15G,h_rt=24:00:00


. /u/local/Modules/default/init/modules.sh

module load bwa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/ameoba
bwa index ameoba_ConcatContigs.fa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/crypto
bwa index crypto_ConcatContigs.fa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi
bwa index fungi_ConcatContigs.fa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/giardia
bwa index giardia_ConcatContigs.fa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/microsporidia
bwa index microsporidia_ConcatContigs.fa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/piroplasma
bwa index piroplasma_ConcatContigs.fa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/plasmo
bwa index plasmo_ConcatContigs.fa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/toxo
bwa index toxo_ConcatContigs.fa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/trich
bwa index trich_ConcatContigs.fa

cd /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/tritryp
bwa index tritryp_ConcatContigs.fa