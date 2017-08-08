#.sam file fields:
# QNAME: Query name of the read or the read pair
# FLAG: Bitwise flag (pairing, strand, mate strand, etc.)
# RNAME: Reference sequence name
# POS: 1-Based leftmost position of clipped alignment
# MAPQ: Mapping quality (Phred-scaled)
# CIGAR: Extended CIGAR string (operations: MIDNSHP)
# MRNM: Mate reference name (‘=’ if same as RNAME)
# MPOS: 1-based leftmost mate position
# ISIZE: Inferred insert size
# SEQQuery: Sequence on the same strand as the reference
# QUAL: Query quality (ASCII-33=Phred base quality)


#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# This script will extract all Unique Reads from .sam/.bam files
#
#
# Method 1:------------------------------------------------------------------------------------
# print the frequency of each mapped read and the read ID from the .bam file 
samtools view SRR3546361.bam | awk '{print $1}' | awk -F. '{print $2}' | uniq -c > readFrequency.txt
# pick only the uniquiely mapped reads (occured once and only once)
awk '$1 ~ /^1$/' readFrequency.txt | awk '{print $2}' > UniqueReads.txt
# then use ExtractUniqueReads.py as follows:
# call the program using: python ExtractUniqueReads.py SRR3546361.sam UniqueReads.txt > UniqueReads_FullList.sam
import argparse
import sys
import os

def parseargs():    # handle user arguments
	parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
	parser.add_argument('bwa', help='BWA abundances results file. Required.')
	parser.add_argument('IDs', help='Uniquely mapped read IDs File. Required.')
	args = parser.parse_args()
	return args

args = parseargs()
ReadIDfile = open(args.IDs, 'r')
head, tail = os.path.split(args.bwa)
ReadSetName = (tail.split(".")[0])

for line in ReadIDfile:
	readID = str(ReadSetName + '.' + line.strip())
	infile = open(args.bwa, 'r')
	for line in infile:
		splits = line.strip().split('\t')
		IDFile = readID.split('.')
		BAMFile = splits[0].split('.')
		if int(IDFile[1]) == int(BAMFile[1]):
			print str(line.strip())
	infile.close()
ReadIDfile.close()
# 
# 
# Method 2: Much faster------------------------------------------------------------------------------------
# Print the entire .sam line for each Unique read and
# cluster the reads based on the target genome and sort (sort -V Numerically) the read list based on their ID
# .sam output (larger file size but readable)
samtools view SRR3546361.bam | awk 'BEGIN { FS="\t" } { c[$1]++; l[$1,c[$1]]=$0 } END { for (i in c) { if (c[i] == 1) for (j = 1; j <= c[i]; j++) print l[i,j] } }' | sort -t$'\t' -k 3,3 -V -k 1,1 > UniqueReads_FullList.sam
# .bam output (smaller output size, compressed)
samtools view SRR3546361.bam | awk 'BEGIN { FS="\t" } { c[$1]++; l[$1,c[$1]]=$0 } END { for (i in c) { if (c[i] == 1) for (j = 1; j <= c[i]; j++) print l[i,j] } }' | sort -t$'\t' -k 3,3 -V -k 1,1 | samtools view -Sb > UniqueReads_FullList.bam




#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# This script will demonstrate how to call SNAP and samtools to generate the coverage figure
#
#
# Method 1:(using the original MakeCoveragePlot.sh)------------------------------------------------
# Make the index
chmod u+x snap-aligner
./snap-aligner index NC_026440.1_Pandoravirus.fasta /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1 -s 16 -large
# Align the paired reads, only output aligned, allow larger edit distance to get more candidate alignment locations
./snap-aligner single /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1 /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1/SRR3546361_NW_001849834.bam -F a -hp -mrl 20 -xf 1.2 -d 40 -o -sam /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1/Data.21.jf-aligned.sam > /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1/Data.21.jf-alignment-stats.txt
# Sort the output
cd /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1
make
chmod u+x samtools
./samtools sort --output-fmt sam /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1/Data.21.jf-aligned.sam > /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1/Data.21.jf-aligned.sorted.sam
# Windowed coverage information, only use MAPQ quality >= 20
./samtools depth -q 20 -a --reference NC_026440.1_Pandoravirus.fasta /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1/Data.21.jf-aligned.sorted.sam | python GetCoverage.py 10 /dev/fd/0 /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1/Data.21.jf-coverage_10.txt
# Make the plot
python CoveragePlot.py -i /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1/Data.21.jf-coverage_10.txt -o /mnt/compgen/homes/mealser/MiCoP_UCLA/samtools-1.4.1/Data.21.jf-CoveragePlot.png -t 8 -u bp -b 35
#
#
#
#
# Method 2: (using our generated .sam file )------------------------------------------------------------------------------------
# Print the entire .sam line for each Unique read and
python ExtractCoverage.py UniqueReads_FullList.sam GenomeInformation.txt > test.txt


#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# This script will extract all genomes that are used to mapp the reads
#
#
# Printing the involved genomes of the .bam file
samtools view -H SRR3546361.bam | awk -F _ '{print $1}' | awk '{print $2}' | uniq -c
# Selecting manually any of them and then extract the reads that are mapped to the selected genome
grep 'CM003142' SRR3546361.sam > SRR3546361_CM003142.sam