# Building Reference Genome Database for MiCoP:
1. Download all genomes from EuPathDB.org
2. Download all genomes from NCBI-RefSeq
3. Move NCBI-RefSeq-Viral folder from NCBI-RefSeq to EuPathDB
4. Exclude NCBI-RefSeq-fungi from NCBI-RefSeq.

###Download EuPathDB.org
```
mkdir /u/scratch2/scratch2/m/malser/EuPathDB/amoebadb
cd /u/scratch2/scratch2/m/malser/EuPathDB/amoebadb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://amoebadb.org/common/downloads/Current_Release/

mkdir /u/scratch2/scratch2/m/malser/EuPathDB/cryptodb
cd /u/scratch2/scratch2/m/malser/EuPathDB/cryptodb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://cryptodb.org/common/downloads/Current_Release/

mkdir /u/scratch2/scratch2/m/malser/EuPathDB/fungidb
cd /u/scratch2/scratch2/m/malser/EuPathDB/fungidb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://fungidb.org/common/downloads/Current_Release/

mkdir /u/scratch2/scratch2/m/malser/EuPathDB/giardiadb
cd /u/scratch2/scratch2/m/malser/EuPathDB/giardiadb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://giardiadb.org/common/downloads/Current_Release/

mkdir /u/scratch2/scratch2/m/malser/EuPathDB/microsporidiadb
cd /u/scratch2/scratch2/m/malser/EuPathDB/microsporidiadb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://microsporidiadb.org/common/downloads/Current_Release/

mkdir /u/scratch2/scratch2/m/malser/EuPathDB/piroplasmadb
cd /u/scratch2/scratch2/m/malser/EuPathDB/piroplasmadb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://piroplasmadb.org/common/downloads/Current_Release/

mkdir /u/scratch2/scratch2/m/malser/EuPathDB/plasmodb
cd /u/scratch2/scratch2/m/malser/EuPathDB/plasmodb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://plasmodb.org/common/downloads/Current_Release/

mkdir /u/scratch2/scratch2/m/malser/EuPathDB/toxodb
cd /u/scratch2/scratch2/m/malser/EuPathDB/toxodb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://toxodb.org/common/downloads/Current_Release/

mkdir /u/scratch2/scratch2/m/malser/EuPathDB/trichdb
cd /u/scratch2/scratch2/m/malser/EuPathDB/trichdb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://trichdb.org/common/downloads/Current_Release/

mkdir /u/scratch2/scratch2/m/malser/EuPathDB/tritrypdb
cd /u/scratch2/scratch2/m/malser/EuPathDB/tritrypdb
wget -A Genome.fasta --no-clobber --convert-links --random-wait --no-directories --recursive -e robots=off -U mozilla --no-parent http://tritrypdb.org/common/downloads/Current_Release/
```

## Download NCBI-RefSeq
```
cd /u/scratch2/m/malser
wget -r -A genomic.fna.gz ftp://ftp.ncbi.nih.gov/refseq/release/* --ftp-user=anonymous
wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/release-catalog/* --ftp-user=anonymous
```

## Unzip the downloaded files [optional]:
```
gunzip -r ftp.ncbi.nih.gov/refseq/release/
```

## Build a list of all organisms covered by EuPathDB :
```
grep -r '>' /u/scratch2/scratch2/m/malser/EuPathDB/ | awk -F '|' '{print $2}' | awk -F '=' '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/EuPathDB_Organism_List.txt
grep -r '>' /u/scratch2/scratch2/m/malser/EuPathDB/NCBI-RefSeq-viral/ | awk -F ' ' '{print $2 "_" $3}' | uniq >> /u/scratch2/scratch2/m/malser/EuPathDB_Organism_List.txt
```

## Exclude any organism from NCBI-RefSeq that is included in EuPathDB:
### If the workload can be done with 24 hours [limited by UCLA hoffman2]
1. Download submit-RemoveRefSeqDuplicatedGenomes_bacteria.sh and CheckDuplicationFromRefSeqFolder.py
2. Modify submit-RemoveRefSeqDuplicatedGenomes_bacteria.sh as needed (change email address, directories, and RefSeq folder name (e.g., replace the word "bacteria" with "archaea"))
3. Submit the Job to UCLA Hoffman2
4. The results will be one text file (contains the removed genomes) and one folder (RefSeq_filtered) in the same directory that contains the RefSeq folder 
```
qsub submit-RemoveRefSeqDuplicatedGenomes_bacteria.sh
```
### If the workload needs more than 24 hours
1. Download submit-RemoveRefSeqDuplicatedGenomes_bacteria_part1.sh and CheckDuplicationFromRefSeqFolder-parallel.py
2. File group ID: is a number specified in the submit-RemoveRefSeqDuplicatedGenomes_bacteria_part1.sh. It allows CheckDuplicationFromRefSeqFolder-parallel.py to run on specific group of files, each of which starts with organism_name then that number. Typically RefSeq files are numbered from 1 to ~2500. So we divide the files into groups based on the first digit of the file number.
3. Modify submit-RemoveRefSeqDuplicatedGenomes_bacteria_part1.sh as needed (change email address, directories, file group ID, and RefSeq folder name (e.g., replace the word "bacteria" with "archaea"))
4. Submit the Job (many jobs) to UCLA Hoffman2
5. The results will be one text file (contains the removed genomes) and one folder (RefSeq_filtered) in the same directory that contains the RefSeq folder 
```
qsub submit-RemoveRefSeqDuplicatedGenomes_bacteria_part1.sh
qsub submit-RemoveRefSeqDuplicatedGenomes_bacteria_part2.sh
qsub submit-RemoveRefSeqDuplicatedGenomes_bacteria_part3.sh
qsub submit-RemoveRefSeqDuplicatedGenomes_bacteria_part4.sh
```
