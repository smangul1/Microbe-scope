#!/bin/bash
set -e  # exit immediately if error occurs

# sed -i -e 's/\r$//' /u/project/zarlab/malser/MiCoP/Scripts/HomologyGenerator.sh
# chmod +x /u/project/zarlab/malser/MiCoP/Scripts/HomologyGenerator.sh
# /u/project/zarlab/malser/MiCoP/Scripts/HomologyGenerator.sh archaea  bacteria  complete  invertebrate  mitochondrion  other  plant  plasmid  plastid  protozoa  vertebrate_mammalian  vertebrate_other

RefSeqFolder=$1
dataDir="/u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/$RefSeqFolder/"

Subdirectory=$(ls -r $dataDir)
for file in $Subdirectory
do
	if [ -s "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" ] #if file exists, to avoid overwriting existing files 
	then
		echo "$file found."
	else
		if [ -s "$dataDir$file" ] # if file is not empty
		then
			# Generating all non-overlapping 30bp seeds
			python3 /u/project/zarlab/malser/MiCoP/Scripts/NonoverlappingSeedGenerator.py ${dataDir}${file} | awk '!seen[$0]++' | python3 /u/project/zarlab/malser/MiCoP/Scripts/FASTAformatter.py /dev/fd/0 ${file} > "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta"
			# BWA-MEM for EuPathDB and 30bp-seeds from RefSeq
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_amoebadb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_cryptodb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_giardiadb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_microsporidiadb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_piroplasmadb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_plasmodb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_toxodb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_trichdb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_tritrypdb_ConcatContigs.fasta "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta" | samtools view -bS - | samtools view -F 4 - > "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			# Extract mapping location for each organism
			python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam" /u/scratch2/scratch2/m/malser/HomologyInformation/
			rm -f "/u/scratch2/scratch2/m/malser/MergedEuPathDB/BWA-MEM_EuPathDB_${file%.*}.sam"
			echo "Done" > "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta"
		fi
	fi
done
