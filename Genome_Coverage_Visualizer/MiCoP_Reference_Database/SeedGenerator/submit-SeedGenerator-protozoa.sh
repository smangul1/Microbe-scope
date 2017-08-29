#!/bin/sh
#$ -S /bin/bash
#$ -N job-Seed-Generator-protozoa-malser
#$ -M mealser@gmail.com
#$ -m abe
#$ -l h_data=25G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load python/3.6.1

 
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/protozoa
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/bacteria  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/complete  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/protozoa  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/protozoa  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/protozoa  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/protozoa  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/protozoa  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/protozoa  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/protozoa  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_protozoa


dataDir="/u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/protozoa"
dataDirBasename=`basename $dataDir`		#protozoa			
dataDir="$dataDir/"						

Subdirectory=$(ls $dataDir)
for file in $Subdirectory
do
	if [ -s "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fastq" ] #if file exists, to avoid overwriting existing files 
	then
		echo "$file found."
	else
		if [ -s "$dataDir$file" ] # if file is not empty
		then
			#mkdir -p "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${dataDirBasename}"
			python3 /u/project/zarlab/malser/MiCoP/Scripts/NonoverlappingSeedGenerator.py ${dataDir}${file} | awk '!seen[$0]++' | python3 /u/project/zarlab/malser/MiCoP/Scripts/FASTQformatter.py /dev/fd/0 ${file}> "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fastq"
			# to verify that the output of previous command is correct 
			# sort /u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/protozoa.1.1.fastq | uniq -c |wc -l
		fi
	fi
done
