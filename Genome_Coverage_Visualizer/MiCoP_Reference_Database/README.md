# Building Reference Genome Database for MiCoP:
1. Download all genomes from EuPathDB.org
2. Download all genomes from NCBI-RefSeq
3. Move NCBI-RefSeq-Viral folder from NCBI-RefSeq to EuPathDB
4. Exclude NCBI-RefSeq-fungi from NCBI-RefSeq
5. Exclude any organism from NCBI-RefSeq that is included in EuPathDB
6. Generate all nonoverlapping K-mers of size 30bp from RefSeq
7. Concat all contigs from EuPath and convert RefSeq-Viral from .fna into .fasta
8. BWA-MEM K-mers of RefSeq to concatenated contigs of Eupath
9. Generate Homology Information Folder

## Download EuPathDB.org
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

## Unzip the downloaded files:
```
gunzip -r ftp.ncbi.nih.gov/refseq/release/
```

## Build a list of all organisms covered by EuPathDB :
```
grep -r '>' /u/scratch2/scratch2/m/malser/EuPathDB/ | awk -F '|' '{print $2}' | awk -F '=' '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/EuPathDB_Organism_List.txt
grep -r '>' /u/scratch2/scratch2/m/malser/EuPathDB/NCBI-RefSeq-viral/ | awk -F ' ' '{print $2 "_" $3}' | uniq >> /u/scratch2/scratch2/m/malser/EuPathDB_Organism_List.txt
```

## Exclude any organism from NCBI-RefSeq that is included in EuPathDB:
### If the workload can be done within 24 hours [limited by UCLA hoffman2]
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

## Generate all nonoverlapping K-mers of size 30bp from RefSeq (change archaea to your target organism of the RefSeq, e.g., plant or mitochondrion)
1. Run hoffman2 in interactive session mode
```
qrsh -l i,h_rt=24:00:00,h_data=25G
```
2. Save the shell script below to SeedGenerator.sh (change all directories and archaea folder into your target folders) 
```
dataDir="/u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/archaea"
dataDirBasename=`basename $dataDir`		#archaea			
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
			python3 /u/project/zarlab/malser/MiCoP/Scripts/NonoverlappingSeedGenerator.py ${dataDir}${file} | awk '!seen[$0]++' | python3 /u/project/zarlab/malser/MiCoP/Scripts/FASTAformatter.py /dev/fd/0 ${file}> "/u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/${file%.*}.fasta"
		fi
	fi
done
```
3. Run the SeedGenerator.sh from the interactive mode as follows
```
module load python/3.6.1
sed -i -e 's/\r$//' /u/project/zarlab/malser/MiCoP/Scripts/SeedGenerator.sh
chmod +x /u/project/zarlab/malser/MiCoP/Scripts/SeedGenerator.sh
/u/project/zarlab/malser/MiCoP/Scripts/SeedGenerator.sh
```

## Concat all contigs from EuPath and convert RefSeq-Viral from .fna into .fasta
```
module load python/3.6.1
# Concat EuPathDB .fasta files into a single file then concat all its contigs into a complete genome
cat /u/scratch2/scratch1/d/dkim/EuPathDB/fungidb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.fasta

cat /u/scratch2/scratch1/d/dkim/EuPathDB/tritrypdb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_tritrypdb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_tritrypdb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_tritrypdb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_tritrypdb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_tritrypdb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_tritrypdb_ConcatContigs.fasta

cat /u/scratch2/scratch1/d/dkim/EuPathDB/trichdb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_trichdb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_trichdb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_trichdb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_trichdb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_trichdb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_trichdb_ConcatContigs.fasta

cat /u/scratch2/scratch1/d/dkim/EuPathDB/toxodb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_toxodb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_toxodb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_toxodb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_toxodb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_toxodb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_toxodb_ConcatContigs.fasta

cat /u/scratch2/scratch1/d/dkim/EuPathDB/plasmodb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_plasmodb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_plasmodb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_plasmodb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_plasmodb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_plasmodb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_plasmodb_ConcatContigs.fasta

cat /u/scratch2/scratch1/d/dkim/EuPathDB/piroplasmadb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_piroplasmadb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_piroplasmadb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_piroplasmadb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_piroplasmadb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_piroplasmadb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_piroplasmadb_ConcatContigs.fasta

cat /u/scratch2/scratch1/d/dkim/EuPathDB/microsporidiadb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_microsporidiadb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_microsporidiadb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_microsporidiadb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_microsporidiadb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_microsporidiadb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_microsporidiadb_ConcatContigs.fasta

cat /u/scratch2/scratch1/d/dkim/EuPathDB/giardiadb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_giardiadb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_giardiadb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_giardiadb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_giardiadb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_giardiadb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_giardiadb_ConcatContigs.fasta

cat /u/scratch2/scratch1/d/dkim/EuPathDB/cryptodb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_cryptodb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_cryptodb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_cryptodb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_cryptodb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_cryptodb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_cryptodb_ConcatContigs.fasta

cat /u/scratch2/scratch1/d/dkim/EuPathDB/amoebadb/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_amoebadb.fasta
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_amoebadb.fasta | awk -F "|" '{print $2}' | uniq > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_amoebadb_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/ConcatContigs.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_amoebadb_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_amoebadb.fasta > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_amoebadb_ConcatContigs.fasta

# Concat NCBI RefSeq Viral files into a single file then convert .fna into .fasta format and concat all sequences but dont touch "complete genomes"
cat /u/scratch2/scratch1/d/dkim/EuPathDB/NCBI-RefSeq-viral/* > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral.genomic.fna
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral.genomic.fna | awk -F ' ' '$NF=="genome" {print $0}' | awk -F ',' '{print $1}' | awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}' >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_EuPathDB_Merged_NCBI-RefSeq-viral_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral.genomic.fna | awk -F ' ' '$NF!="genome" {print $2,$3}' | uniq >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_EuPathDB_Merged_NCBI-RefSeq-viral_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/Concat_Contigs_RefSeq_to_EuPathDB_Converter.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_EuPathDB_Merged_NCBI-RefSeq-viral_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral.genomic.fna > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
```

## BWA-MEM K-mers of RefSeq to concatenated contigs of Eupath
```
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.fasta
bwa mem /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.fasta /u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered_Seeds/plant.100.1.genomic.fasta  | samtools view -bS - | samtools view -b -F 4  - > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.bam
```

## [Optional] Keep fully mapped reads with an edit distance of 0 (exact matching)
```
samtools view /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.bam | awk '$12=="NM:i:0"' | awk '$6=="30M"'
```

## Generate Homology Information Folder
```
samtools view /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.bam | python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py /dev/fd/0 /u/scratch2/scratch2/m/malser/HomologyInformation/
```
