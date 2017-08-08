#!/bin/sh
#$ -S /bin/bash
#$ -N job-Concat-Contigs_malser
#$ -cwd
#$ -M mealser@gmail.com
#$ -m abe
#$ -l h_data=15G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load python/3.6.1
#ameoba.fa  fungi.fa     microsporidia.fa  plasmo.fa  trich.fa
#crypto.fa  giardia.fa   piroplasma.fa     toxo.fa    tritryp.fa
grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/ameoba.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/ameoba_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/ameoba_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/ameoba.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/ameoba_ConcatContigs.fa

grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/fungi.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/fungi.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi_ConcatContigs.fa

grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/microsporidia.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/microsporidia_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/microsporidia_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/microsporidia.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/microsporidia_ConcatContigs.fa

grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/plasmo.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/plasmo_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/plasmo_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/plasmo.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/plasmo_ConcatContigs.fa

grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/trich.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/trich_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/trich_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/trich.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/trich_ConcatContigs.fa

grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/crypto.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/crypto_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/crypto_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/crypto.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/crypto_ConcatContigs.fa

grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/giardia.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/giardia_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/giardia_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/giardia.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/giardia_ConcatContigs.fa

grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/piroplasma.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/piroplasma_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/piroplasma_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/piroplasma.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/piroplasma_ConcatContigs.fa

grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/toxo.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/toxo_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/toxo_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/toxo.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/toxo_ConcatContigs.fa

grep '>' /u/project/zarlab/serghei/eupathdb/eupathdbFasta/tritryp.fa | awk -F "|" '{print $2}' | uniq > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/tritryp_RefList.txt
python3 ConcatContigs.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/tritryp_RefList.txt /u/project/zarlab/serghei/eupathdb/eupathdbFasta/tritryp.fa > /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/tritryp_ConcatContigs.fa