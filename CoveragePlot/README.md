# Coverage Plot for Metagenomics
![alt text](https://github.com/smangul1/miCoP/blob/master/CoveragePlot/Malassezia_globosa_CBS_7966.png)
![alt text](https://github.com/smangul1/miCoP/blob/master/CoveragePlot/Malassezia_globosa_CBS_7966_MM.png)

## About:
1. The script of "MiCoP_MakeCoveragePlot.sh" takes a single ".bam" file that is the output of "bwa-mem -a".
2. It extracts the unique reads that are mapped once and only once to the entire genome database.
3. It sorts the unique read list based on the genome.
4. For each genome, it takes the unique reads and builds coverage information and then generates the coverage plot.
5. The coverage information includes the genome name, bp index, and number of reads that are mapped to the bp located at the bp index.
6. All the coverage plots will be saved in "CoveragePlots" folder in the same working directory.

## Pre-processing Step [optional]:
1. The reference genome database contains many contigs for each organism. If you like to generate a coverage plot for each organism rather than each contig, you need to pre-process the reference database.
2. "ConcatContigs.py" prepares the database (fungi.fa) by extracting the long sequence of all organisms involoved.
3. For each organism, it concats all contigs and generates a single fasta output (it updates the organism name and the length of the sequence in the header field & it also updates the sequence field with the new concatenated sequence). 

## Running a test:

Pre-processing:
```
$ awk -F "|" '{print $2}' fungi.names | uniq > RefList.txt
$ python ConcatContigs.py RefList.txt fungi.fa > fungi_ConcatContigs.fa
```
Coverage Plot:
```
$ samtools view ${BAMFile} | awk 'BEGIN { FS="\t" } { c[$1]++; l[$1,c[$1]]=$0 } END { for (i in c) { if (c[i] == 1) for (j = 1; j <= c[i]; j++) print l[i,j] } }' | sort -t$'\t' -k 3,3 -V -k 1,1 > ${UniqueReadList}

$ python ExtractCoverage.py ${UniqueReadList} GenomeInformation.txt
```
where ${BAMFile} is the output file of the "bwa-mem -a" and ${UniqueReadList} is the name of the produced list of all unique reads.

By Mohammed Alser, inspired by https://github.com/dkoslicki/CAMDA/tree/master/src
