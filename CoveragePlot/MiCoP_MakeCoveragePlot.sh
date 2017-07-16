#!/bin/bash
set -e

# module load python/3.6.1
# module load bwa
# module load samtools
# sed -i -e 's/\r$//' MiCoP_MakeCoveragePlot.sh
# chmod +x MiCoP_MakeCoveragePlot.sh
# time ./MiCoP_MakeCoveragePlot.sh /u/project/zarlab/serghei/eupathdb/eupathdbFasta/piroplasma.fa /u/home/galaxy/collaboratory/serghei/MetaSUB-Inter-City-Challenge/data/SRR3546361.fastq /u/project/zarlab/malser/MiCoP 100000


# Reference database (metagenome)
metagenome=$1 									# /u/project/zarlab/serghei/eupathdb/eupathdbFasta/piroplasma.fa
metagenomeBasename=`basename $metagenome`		# piroplasma.fa`
metagenomeFName="${metagenomeBasename%.*}"		# piroplasma
metagenomeExtention="${metagenomeBasename##*.}"	# fa

# Microbiome under study
sample=$2								# /u/home/galaxy/collaboratory/serghei/MetaSUB-Inter-City-Challenge/data/SRR3546361.fastq
sampleBasename=`basename $sample`		# SRR3546361.fastq
sampleFName="${sampleBasename%.*}"		# SRR3546361
sampleExtention="${sampleBasename##*.}"	# fastq

# Create auxiliary folders
dataDir=$3
dataDir="$dataDir/$metagenomeFName/$sampleFName/"
mkdir -p ${dataDir}

# Coverage plot variables 
windowSize=$4
truncateTo=8
bottom=35

# # Call Necessary Tools
# module load python/3.6.1
# module load bwa
# module load samtools

# Concatenate all contigs of the reference database
echo "Step 1: Contigs Concatenation"
grep '>' ${metagenome} | awk -F "|" '{print $2}' | uniq > ${dataDir}${metagenomeFName}_RefList.txt
python3 ConcatContigs.py ${dataDir}${metagenomeFName}_RefList.txt ${metagenome} > ${dataDir}${metagenomeFName}_ConcatContigs.${metagenomeExtention}

# # BWA-MEM Mapping
echo "Step 2: BWA-MEM Indexing, Mapping, & Sorting"
bwa index ${dataDir}${metagenomeFName}_ConcatContigs.${metagenomeExtention}
bwa mem -a -v 0 ${dataDir}${metagenomeFName}_ConcatContigs.${metagenomeExtention} ${sample} | awk '$3!="*"' | samtools view -bS - > ${dataDir}${metagenomeFName}_${sampleFName}_Filtered.bam
samtools view -h ${dataDir}${metagenomeFName}_${sampleFName}_Filtered.bam | sort -t$'\t' -V -k 1,1n -V -k 3,3 | samtools view -bS - >  ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam

# Unique Read
echo "Step 3: Unique Read Coverage"
grep '>' ${dataDir}${metagenomeFName}_ConcatContigs.${metagenomeExtention} > ${dataDir}${metagenomeFName}_RefList.txt
#samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam | python3 ReadClassifier.py /dev/fd/0  1 | sort -t$'\t' -V -k 3,3 > ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam
samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam | awk 'BEGIN { FS="\t" } { c[$1]++; l[$1,c[$1]]=$0 } END { for (i in c) { if (c[i] == 1) for (j = 1; j <= c[i]; j++) print l[i,j] } }' | sort -t$'\t' -k 3,3 > ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam
python3 CoveragePlot.py ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam ${dataDir}${metagenomeFName}_RefList.txt ${windowSize} 1 ${dataDir}

# Multimapped Read (within genome)
echo "Step 4: Multimapped Read (within genome) Coverage"
samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam | python3 ReadClassifier.py /dev/fd/0  2 | sort -t$'\t' -V -k 3,3 > ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam
python3 CoveragePlot.py ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam ${dataDir}${metagenomeFName}_RefList.txt ${windowSize} 2 ${dataDir}

# Multimapped Read (across genome)
echo "Step 5: Multimapped Read (across genome) Coverage"
samtools view ${dataDir}${metagenomeFName}_${sampleFName}_Sorted.bam | python3 ReadClassifier.py /dev/fd/0  3 | sort -t$'\t' -V -k 3,3 > ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam
python3 CoveragePlot.py ${dataDir}${metagenomeFName}_${sampleFName}_UniqueReads_Sorted.sam ${dataDir}${metagenomeFName}_RefList.txt ${windowSize} 3 ${dataDir}

echo "MiCoP coverage plots are genererated successfully ... $dataDir"