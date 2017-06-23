#!/bin/bash
set -e

# This script will demonstrate how to call SNAP and samtools to generate the coverage figure
# window size for coverage plot
windowSize=10
# truncate the coverage plot to the following coverage (must be a power of two)
truncateTo=8
# bottom tells where to start the inner ring of the plot
bottom=35
UniqueReadList="UniqueReads_FullList.sam"
BAMFile="SRR3546361.bam"


# This script will extract all Unique Reads from .sam/.bam files

# Print the entire .sam line for each Unique read and
# cluster the reads based on the target genome and 
# sort (sort -V for numerically sorting rather than as a string sorting) the read list based on their ID
# .sam output (larger file size but readable)
samtools view ${BAMFile} | awk 'BEGIN { FS="\t" } { c[$1]++; l[$1,c[$1]]=$0 } END { for (i in c) { if (c[i] == 1) for (j = 1; j <= c[i]; j++) print l[i,j] } }' | sort -t$'\t' -k 3,3 -V -k 1,1 > ${UniqueReadList}
# .bam output (smaller output size, compressed)
#samtools view ${BAMFile} | awk 'BEGIN { FS="\t" } { c[$1]++; l[$1,c[$1]]=$0 } END { for (i in c) { if (c[i] == 1) for (j = 1; j <= c[i]; j++) print l[i,j] } }' | sort -t$'\t' -k 3,3 -V -k 1,1 | samtools view -Sb > UniqueReads_FullList.bam



#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# This script will generate the coverage information and the coverage plot for each genome
# The plots will be saved in "CoveragePlots" folder in the same working directory
python ExtractCoverage.py ${UniqueReadList} GenomeInformation.txt