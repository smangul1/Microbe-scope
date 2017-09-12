#!/bin/bash
set -e  # exit immediately if error occurs

# module load python/3.6.1
# module load bwa
# module load samtools
# sed -i -e 's/\r$//' /u/project/zarlab/malser/MiCoP/Scripts/MiCoP_GenomeCoverageVisualizer.sh
# chmod +x /u/project/zarlab/malser/MiCoP/Scripts/MiCoP_GenomeCoverageVisualizer.sh
# /u/project/zarlab/malser/MiCoP/Scripts/MiCoP_GenomeCoverageVisualizer.sh /u/scratch2/scratch2/m/malser/MergedEuPathDB /u/home/galaxy/collaboratory/serghei/MetaSUB-Inter-City-Challenge/data/SRR3546361.fastq /u/project/zarlab/malser/MiCoP/Scripts /u/project/zarlab/malser/MiCoP 1 /u/scratch2/scratch2/m/malser/HomologyInformation/ 30
#########################################################################
# Reference database (metagenome)
metagenome=$1 									# /u/scratch2/scratch2/m/malser/MergedEuPathDB
case "$metagenome" in
*/)
    metagenome="$metagenome"
    ;;
*)
    metagenome="$metagenome/"
    ;;
esac
#########################################################################
# Microbiome under study
sample=$2								# /u/home/galaxy/collaboratory/serghei/MetaSUB-Inter-City-Challenge/data/SRR3546361.fastq
sampleBasename=`basename $sample`		# SRR3546361.fastq
sampleFName="${sampleBasename%.*}"		# SRR3546361
sampleExtention="${sampleBasename##*.}"	# fastq
#########################################################################
# Script Directory
scriptDir=$3							# /u/project/zarlab/malser/MiCoP/Scripts
case "$scriptDir" in
*/)
    scriptDir="$scriptDir"
    ;;
*)
    scriptDir="$scriptDir/"
    ;;
esac
#########################################################################
# Create auxiliary folders
dataDir=$4
case "$dataDir" in
*/)
    dataDir="$dataDir"
    ;;
*)
    dataDir="$dataDir/"
    ;;
esac
dataDir="${dataDir}MiCoP_$sampleFName/"
mkdir -p ${dataDir}
#########################################################################
# Coverage plot variables 
windowSize=$5
#########################################################################
# Homology (RefSeq <-> EuPathDB) Information
HomologyDir=$6                               # /u/scratch2/scratch2/m/malser/HomologyInformation/
case "$HomologyDir" in
*/)
    HomologyDir="$HomologyDir"
    ;;
*)
    HomologyDir="$HomologyDir/"
    ;;
esac
#########################################################################
KmerSize=$7                                  # 30
#########################################################################

#########################################################################
#########################################################################
#########################################################################
# BWA-MEM Mapping
echo "First step: BWA-MEM Mapping, & Sorting"
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_amoebadb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")' >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_cryptodb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")' >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_fungidb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")'  >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_giardiadb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")'  >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_microsporidiadb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")' >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")' >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_piroplasmadb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")' >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_plasmodb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")' >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_toxodb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")' >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_trichdb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")' >> ${dataDir}${sampleFName}_BWA-MEM.sam
bwa mem -a -v 0 ${metagenome}EuPathDB_Merged_tritrypdb_ConcatContigs.fasta ${sample} | awk '(!/^ *@/) && ($3!="*")' >> ${dataDir}${sampleFName}_BWA-MEM.sam

# Sort .bam content
sort -t$'\t' -V -k 1,1n -V -k 3,3 ${dataDir}${sampleFName}_BWA-MEM.sam > ${dataDir}${sampleFName}_BWA-MEM_sorted.sam
#########################################################################
# Unique Read
echo "Second step: Unique Read Coverage"
#samtools view ${dataDir}${sampleFName}_Sorted.bam| python3 ${scriptDir}/ReadClassifier_and_Filter.py /dev/fd/0  1 | sort -t$'\t' -V -k 3,3 > ${dataDir}${sampleFName}_UniqueReads_Sorted.sam
awk 'BEGIN { FS="\t" } { c[$1]++; l[$1,c[$1]]=$0 } END { for (i in c) { if (c[i] == 1) for (j = 1; j <= c[i]; j++) print l[i,j] } }' ${dataDir}${sampleFName}_BWA-MEM_sorted.sam| sort -t$'\t' -k 3,3 > ${dataDir}${sampleFName}_UniqueReads_Sorted.sam
python3 ${scriptDir}/CoveragePlot_HighChartsSingleCSVperGenome.py ${dataDir}${sampleFName}_UniqueReads_Sorted.sam ${metagenome}MiCoP_DB_RefList_perGenome.txt ${windowSize} 1 ${dataDir}
#########################################################################
# Multimapped Read (within genome)
echo "Third step: Multimapped Read (within genome) Coverage"
python3 ${scriptDir}/ReadClassifier_and_Filter.py ${dataDir}${sampleFName}_BWA-MEM_sorted.sam 2 | sort -t$'\t' -V -k 3,3 > ${dataDir}${sampleFName}_MMWithinReads_Sorted.sam
python3 ${scriptDir}/CoveragePlot_HighChartsSingleCSVperGenome.py ${dataDir}${sampleFName}_MMWithinReads_Sorted.sam ${metagenome}MiCoP_DB_RefList_perGenome.txt ${windowSize} 2 ${dataDir}
#########################################################################
# Multimapped Read (across genome)
echo "Four step: Multimapped Read (across genome) Coverage"
python3 ${scriptDir}/ReadClassifier_and_Filter.py ${dataDir}${sampleFName}_BWA-MEM_sorted.sam 3 | sort -t$'\t' -V -k 3,3 > ${dataDir}${sampleFName}_MMAcrossReads_Sorted.sam
python3 ${scriptDir}/CoveragePlot_HighChartsSingleCSVperGenome.py ${dataDir}${sampleFName}_MMAcrossReads_Sorted.sam ${metagenome}MiCoP_DB_RefList_perGenome.txt ${windowSize} 3 ${dataDir}
#########################################################################
# Homologous Read Coverage and Finalizing the output .csv files
echo "Fifth step: Homologous Read Coverage and finalizing the output .csv files"
python3 ${scriptDir}/FilterNulls_csv.py ${dataDir}MiCoP_FinalCSVs ${metagenome}MiCoP_DB_RefList_perGenome.txt ${HomologyDir} ${KmerSize} ${windowSize}
#########################################################################
# Deleting Temporary Files
echo "Last step: Deleting Temporary Files"
#rm -f ${dataDir}header.txt
#find ${dataDir} -maxdepth 1 -name "${sampleFName}_*.bam" -type f -delete

echo "MiCoP Genome Coverage Visualizer is ready ... copy the following folder $dataDirMiCoP_FinalCSVs next to MiCoP.html from Scripts folder and open MiCoP.html"
