#!/bin/bash
set -e  # exit immediately if error occurs

# module load python/3.6.1
# module load bwa
# module load samtools
# sed -i -e 's/\r$//' MiCoP_GenomeCoverageVisualizer.sh
# chmod +x MiCoP_GenomeCoverageVisualizer.sh
# time ./MiCoP_GenomeCoverageVisualizer.sh /u/project/zarlab/serghei/eupathdb/eupathdbFasta/piroplasma.fa /u/home/galaxy/collaboratory/serghei/MetaSUB-Inter-City-Challenge/data/SRR3546361.fastq /u/project/zarlab/malser/MiCoP/Scripts /u/project/zarlab/malser/MiCoP 200 1 2
#########################################################################
# Reference database (metagenome)
metagenome=$1 									# /u/project/zarlab/serghei/eupathdb/eupathdbFasta/piroplasma.fa
metagenomeBasename=`basename $metagenome`		# piroplasma.fa`
metagenomeFName="${metagenomeBasename%.*}"		# piroplasma
metagenomeExtention="${metagenomeBasename##*.}"	# fa
#########################################################################
# Microbiome under study
sample=$2								# /u/home/galaxy/collaboratory/serghei/MetaSUB-Inter-City-Challenge/data/SRR3546361.fastq
sampleBasename=`basename $sample`		# SRR3546361.fastq
sampleFName="${sampleBasename%.*}"		# SRR3546361
sampleExtention="${sampleBasename##*.}"	# fastq
#########################################################################
# Script Directory
scriptDir=$3							# /u/project/zarlab/malser/MiCoP/Scripts
#########################################################################
# Create auxiliary folders
dataDir=$4
dataDir="$dataDir/$metagenomeFName/$sampleFName/"
mkdir -p ${dataDir}
#########################################################################
# Coverage plot variables 
windowSize=$5
#########################################################################
# Call Necessary Tools
if [ "$6" = "1" ]
then
	echo "UCLA Hoffman2 mode is selected!"
	. /u/local/Modules/default/init/modules.sh
	module load python/3.6.1
	module load bwa
	module load samtools
elif [ "$6" = "2" ]
then
	echo "Non-Hoffman2 mode is selected"
else
	echo "Please select 1 or 2 for the sixth parameter!"
	exit
fi
#########################################################################
# Start Bulding the input data for the Genome Covergae Visualizer
if [ "$7" = "1" ]
then
	# Concatenate all contigs of the reference database
	echo "First step: Contigs Concatenation"
	grep '>' ${metagenome} | awk -F "|" '{print $2}' | uniq > ${dataDir}${metagenomeFName}_RefList_perGenome.txt
	python3 ${scriptDir}/ConcatContigs.py ${dataDir}${metagenomeFName}_RefList_perGenome.txt ${metagenome} > ${dataDir}${metagenomeFName}_ConcatContigs.${metagenomeExtention}

	# BWA-MEM Mapping
	echo "Next step: BWA-MEM Indexing, Mapping, & Sorting"
	bwa index ${dataDir}${metagenomeFName}_ConcatContigs.${metagenomeExtention}
	bwa mem -a -v 0 ${dataDir}${metagenomeFName}_ConcatContigs.${metagenomeExtention} ${sample} | awk '$3!="*"' | samtools view -bS - > ${dataDir}${metagenomeFName}_${sampleFName}_Filtered.bam
	samtools view -H ${dataDir}${metagenomeFName}_${sampleFName}_Filtered.bam > ${dataDir}header.txt  
	samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Filtered.bam | sort -t$'\t' -V -k 1,1n -V -k 3,3  | cat ${dataDir}header.txt -| samtools view -bS - >  ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam

	# Generate Reference List to be used for sorting the reads
	grep '>' ${dataDir}${metagenomeFName}_ConcatContigs.${metagenomeExtention} > ${dataDir}${metagenomeFName}_RefList_perGenome.txt
elif [ "$7" = "2" ]
then
	# BWA-MEM Mapping
	echo "First step: BWA-MEM Indexing, Mapping, & Sorting"
	cp  ${metagenome} ${dataDir}
	bwa index ${dataDir}${metagenomeBasename}
	bwa mem -a -v 0 ${dataDir}${metagenomeBasename} ${sample} | awk '$3!="*"' | samtools view -bS - > ${dataDir}${metagenomeFName}_${sampleFName}_Filtered.bam
	samtools view -H ${dataDir}${metagenomeFName}_${sampleFName}_Filtered.bam > ${dataDir}header.txt  
	samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Filtered.bam | sort -t$'\t' -V -k 1,1n -V -k 3,3  | cat ${dataDir}header.txt -| samtools view -bS - >  ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam

	# Generate Reference List to be used for sorting the reads
	grep '>' ${dataDir}${metagenomeBasename} | awk -F "|" '{print $2}' | uniq > ${dataDir}${metagenomeFName}_RefList_perContigs.txt
	python3 ${scriptDir}/CalculateGenomeLengthFromContigs.py ${dataDir}${metagenomeFName}_RefList_perContigs.txt ${metagenome} > ${dataDir}${metagenomeFName}_RefList_perGenome.txt
elif [ "$7" = "3" ]
then
	# Sorting the input .bam file
	echo "First step: Sorting BWA-MEM's output"
	samtools view -H $8 > ${dataDir}header.txt  
	samtools view $8 | sort -t$'\t' -V -k 1,1n -V -k 3,3 | cat ${dataDir}header.txt -| samtools view -bS - >  ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam

	# Generate Reference List to be used for sorting the reads
	grep '>' ${dataDir}${metagenomeFName}_ConcatContigs.${metagenomeExtention} > ${dataDir}${metagenomeFName}_RefList_perGenome.txt
else
	echo "Please select 1 or 2 for the seventh parameter! (1) for concatenating the contigs of the reference database. (2) for not concatenating the contigs."
	exit
fi
#########################################################################
# Unique Read
echo "Next step: Unique Read Coverage"
#samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam | python3 ${scriptDir}/ReadClassifier_and_Filter.py /dev/fd/0  1 | sort -t$'\t' -V -k 3,3 > ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam
samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam | awk 'BEGIN { FS="\t" } { c[$1]++; l[$1,c[$1]]=$0 } END { for (i in c) { if (c[i] == 1) for (j = 1; j <= c[i]; j++) print l[i,j] } }' | sort -t$'\t' -k 3,3 > ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam
python3 ${scriptDir}/CoveragePlot_HighChartsSingleCSVperGenome.py ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam ${dataDir}${metagenomeFName}_RefList_perGenome.txt ${windowSize} 1 ${dataDir}
#########################################################################
# Multimapped Read (within genome)
echo "Next step: Multimapped Read (within genome) Coverage"
samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam | python3 ${scriptDir}/ReadClassifier_and_Filter.py /dev/fd/0  2 | sort -t$'\t' -V -k 3,3 > ${dataDir}${metagenomeFName}_${sampleFName}_MMWithinReads_Sorted.sam
python3 ${scriptDir}/CoveragePlot_HighChartsSingleCSVperGenome.py ${dataDir}${metagenomeFName}_${sampleFName}_MMWithinReads_Sorted.sam ${dataDir}${metagenomeFName}_RefList_perGenome.txt ${windowSize} 2 ${dataDir}
#########################################################################
# Multimapped Read (across genome)
echo "Next step: Multimapped Read (across genome) Coverage"
samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam | python3 ${scriptDir}/ReadClassifier_and_Filter.py /dev/fd/0  3 | sort -t$'\t' -V -k 3,3 > ${dataDir}${metagenomeFName}_${sampleFName}_MMAcrossReads_Sorted.sam
python3 ${scriptDir}/CoveragePlot_HighChartsSingleCSVperGenome.py ${dataDir}${metagenomeFName}_${sampleFName}_MMAcrossReads_Sorted.sam ${dataDir}${metagenomeFName}_RefList_perGenome.txt ${windowSize} 3 ${dataDir}
#########################################################################
# Multimapped Read (across genome)
echo "Last step: Finalizing the output .csv files"
python3 ${scriptDir}/FilterNulls_csv.py ${dataDir}MiCoP_FinalCSVs

echo "MiCoP Genome Coverage Visualizer is ready ... copy the following folder $dataDirMiCoP_FinalCSVs next to MiCoP.html from Scripts folder and open MiCoP.html"