#!/bin/sh
#$ -S /bin/bash
#$ -N job-Seed-Generator-vertebrate_mammalian-malser
#$ -cwd
#$ -M mealser@gmail.com
#$ -m abe
#$ -l h_data=15G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load python/3.6.1

 
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/bacteria  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/complete  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian  
# /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_vertebrate_mammalian


dataDir="/u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/vertebrate_mammalian"
dataDirBasename=`basename $dataDir`		#vertebrate_mammalian			
dataDir="$dataDir/"						

Subdirectory=$(ls $dataDir)
for file in $Subdirectory
do
	if [ -s "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" ] #if file exists, to avoid overwriting existing files 
	then
		echo "$file found."
	else
		if [ -s "$dataDir$file" ] # if file is not empty
		then
			#mkdir -p "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${dataDirBasename}"
			python3 /u/project/zarlab/malser/MiCoP/Scripts/NonoverlappingSeedGenerator.py ${dataDir}${file} | awk '!seen[$0]++' | python3 /u/project/zarlab/malser/MiCoP/Scripts/FASTAformatter.py /dev/fd/0 ${file}> "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta"
			# to verify that the output of previous command is correct 
			# sort /u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/vertebrate_mammalian.1.1.fasta | uniq -c |wc -l
		fi
	fi
done
