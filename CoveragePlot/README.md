# Coverage Plot for Metagenomics

## About:
1- The script of "MiCoP_MakeCoveragePlot.sh" takes a single ".bam" file that is the output of "bwa-mem -a".
2- It extracts the unique reads that are mapped once and only once to the entire genome database.
3- It sorts the unique read list based on the genome.
4- For each genome, it takes the unique reads and builds coverage information and then generates the coverage plot.
5- The coverage information includes the genome name, bp index, and number of reads that are mapped to the bp located at the bp index.
6- All the coverage plots will be saved in "CoveragePlots" folder in the same working directory.

## Running a test:

```
$ samtools view ${BAMFile} | awk 'BEGIN { FS="\t" } { c[$1]++; l[$1,c[$1]]=$0 } END { for (i in c) { if (c[i] == 1) for (j = 1; j <= c[i]; j++) print l[i,j] } }' | sort -t$'\t' -k 3,3 -V -k 1,1 > ${UniqueReadList}

$ python ExtractCoverage.py ${UniqueReadList} GenomeInformation.txt
```
where ${BAMFile} is the output file of the "bwa-mem -a" and ${UniqueReadList} is the name of the produced list of all unique reads.

By Mohammed Alser, inspired by https://github.com/dkoslicki/CAMDA/tree/master/src
