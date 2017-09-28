# Build comprehensive MiCoP database:
1. Download all genomes from EuPathDB.org
2. Download all genomes from NCBI-RefSeq
3. Move NCBI-RefSeq-Viral folder from NCBI-RefSeq to EuPathDB
4. Exclude NCBI-RefSeq-fungi from NCBI-RefSeq
5. Exclude any organism from NCBI-RefSeq that is included in EuPathDB
6. Concat all contigs from EuPath and convert RefSeq-Viral from .fna into .fasta
7. Generate all nonoverlapping 30-mers from RefSeq, BWA-MEM them with the concatenated contigs of Eupath, and Generate Homology Information Folder
8. Generate the start and end coordinates of homologous regions.

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
5. Summary reports of all genomes removed from NCBI-RefSeq that exist in the EuPathDB can be downloaded from: https://github.com/smangul1/miCoP/tree/master/Genome_Coverage_Visualizer/MiCoP_Reference_Database/Removed_Genomes_from_RefSeq
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
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral.genomic.fna | awk -F ' ' '$NF=="genome" {print}' | awk -F ',' '{print $1}' | awk '{ $1=""; print}' >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral.genomic.fna | awk -F ' ' '$NF!="genome" {print}' | awk -F ',' '{print $1}' | awk '{ $1=""; $NF=""; print}' | uniq  >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_RefList_perGenome.txt
python3 /u/project/zarlab/malser/MiCoP/Scripts/Concat_Contigs_RefSeq_to_EuPathDB_Converter.py /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral.genomic.fna > /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
```

## Refine the NCBI-RefSeq-Viral .fasta file
Some organisms in the RefSeq-Viral have different versions, but they used same organism name (e.g., Tomato leaf curl Palampur virus, Blotched snakehead virus, Potato yellow vein virus, Hantaan virus, Humulus japonicus latent virus, Amasya cherry disease-associated mycovirus, Adult diarrheal rotavirus strain J19). This can lead to ignore these versions and consider them as a single reference genome in the BWA-MEM stage. Hence, we used the following script to add the sequence number to the organism name:
```
# Extract the sequence number and line number to use them for replacing the name of similar complete genomes
grep 'Amasya cherry disease-associated mycovirus' /u/scratch2/scratch1/d/dkim/EuPathDB/NCBI-RefSeq-viral/viral.1.1.genomic.fna
grep -n 'Amasya_cherry_disease-associated_mycovirus' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
# Replace   
sed -i '7807s/.*/>organism=Amasya_cherry_disease-associated_mycovirus_NC_006440.1 | version=Not_Reported | length=3841 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '7809s/.*/>organism=Amasya_cherry_disease-associated_mycovirus_NC_006441.1 | version=Not_Reported | length=3841 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta

# Extract the sequence number and line number to use them for replacing the name of similar complete genomes
grep 'Humulus japonicus latent virus' /u/scratch2/scratch1/d/dkim/EuPathDB/NCBI-RefSeq-viral/viral.1.1.genomic.fna
grep -n 'Humulus_japonicus_latent_virus' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
# Replace   
sed -i '7733s/.*/>organism=Humulus_japonicus_latent_virus_NC_006064.1 | version=Not_Reported | length=8130 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '7735s/.*/>organism=Humulus_japonicus_latent_virus_NC_006065.1 | version=Not_Reported | length=8130 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '7737s/.*/>organism=Humulus_japonicus_latent_virus_NC_006066.1 | version=Not_Reported | length=8130 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta

# Extract the sequence number and line number to use them for replacing the name of similar complete genomes
grep 'Hantaan virus' /u/scratch2/scratch1/d/dkim/EuPathDB/NCBI-RefSeq-viral/viral.1.1.genomic.fna
grep -n 'Hantaan_virus' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
# Replace   
sed -i '7663s/.*/>organism=Hantaan_virus_NC_005218.1 | version=Not_Reported | length=11845 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '7665s/.*/>organism=Hantaan_virus_NC_005219.1 | version=Not_Reported | length=11845 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta

# Extract the sequence number and line number to use them for replacing the name of similar complete genomes
grep 'Potato yellow vein virus' /u/scratch2/scratch1/d/dkim/EuPathDB/NCBI-RefSeq-viral/viral.1.1.genomic.fna
grep -n 'Potato_yellow_vein_virus' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
# Replace  
sed -i '3273s/.*/>organism=Potato_yellow_vein_virus_NC_006062.1 | version=Not_Reported | length=17266 | SO=_complete_sequence/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '3275s/.*/>organism=Potato_yellow_vein_virus_NC_006063.1 | version=Not_Reported | length=17266 | SO=_complete_sequence/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta

# Extract the sequence number and line number to use them for replacing the name of similar complete genomes
grep 'Blotched snakehead virus' /u/scratch2/scratch1/d/dkim/EuPathDB/NCBI-RefSeq-viral/viral.1.1.genomic.fna
grep -n 'Blotched_snakehead_virus' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
# Replace
sed -i '1959s/.*/>organism=Blotched_snakehead_virus_NC_005983.1 | version=Not_Reported | length=6179 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '1861s/.*/>organism=Blotched_snakehead_virus_NC_005982.1 | version=Not_Reported | length=6179 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta

# Extract the sequence number and line number to use them for replacing the name of similar complete genomes
grep 'Tomato leaf curl Palampur virus' /u/scratch2/scratch1/d/dkim/EuPathDB/NCBI-RefSeq-viral/viral.1.1.genomic.fna
grep -n 'Tomato_leaf_curl_Palampur_virus' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
# Replace
sed -i '1849s/.*/>organism=Tomato_leaf_curl_Palampur_virus_NC_010840.1 | version=Not_Reported | length=5481 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '1851s/.*/>organism=Tomato_leaf_curl_Palampur_virus_NC_010839.1 | version=Not_Reported | length=5481 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta

# Extract the sequence number and line number to use them for replacing the name of similar complete genomes
grep 'Adult diarrheal rotavirus strain J19' /u/scratch2/scratch1/d/dkim/EuPathDB/NCBI-RefSeq-viral/viral.1.1.genomic.fna
grep -n 'Adult_diarrheal_rotavirus_strain_J19' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
# Replace
sed -i '8331s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007548.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8333s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007549.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8335s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007550.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8337s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007551.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8339s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007552.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8341s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007553.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8343s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007554.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8345s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007555.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8347s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007556.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8349s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007557.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
sed -i '8351s/.*/>organism=Adult_diarrheal_rotavirus_strain_J19_NC_007558.1 | version=Not_Reported | length=17961 | SO=_complete_genome/' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
```

## Refine the name of some organisms:
Some organism names in the .fasta files contain slashes. This causes a problem when we generate .csv as we use the organism name as .csv file name. So we replace them by underscore '_'. 
```
sed -i 's/\//_/g' /u/scratch2/scratch2/m/malser/MergedEuPathDB/*.fasta
```

## Building the BWA index and Generating the genome list covered by our database:
```
# Building the BWA index
module load bwa
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_amoebadb_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_cryptodb_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_giardiadb_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_microsporidiadb_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_piroplasmadb_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_plasmodb_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_toxodb_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_trichdb_ConcatContigs.fasta
bwa index /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_tritrypdb_ConcatContigs.fasta
# Generating the genome list covered by our database
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_amoebadb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_cryptodb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_giardiadb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_microsporidiadb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_NCBI-RefSeq-viral_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_piroplasmadb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_plasmodb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_toxodb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_trichdb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
grep '>' /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_tritrypdb_ConcatContigs.fasta >> /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt
```

## Generate all nonoverlapping 30-mers from RefSeq, BWA-MEM them with the concatenated contigs of Eupath, and Generate Homology Information Folder
1. It takes a RefSeq file after removing all genome sequences that are shared with EuPathDB.  
2. It then generates all seeds (or k-mers) that are of length 30 bp (the length is configurable in "NonoverlappingSeedGenerator.py").
3. The script also removes all redundant seeds and keep only one. There are faster and more effiecient ways (such as maintaining a trie structure, commented in "NonoverlappingSeedGenerator.py") of doing the same job of the script, if and only if we can address the memory and execution time limitations imposed by UCLA-Hoffman2.
4. It BWA-MEMs (fully mapped reads with an edit distance of zero) the seeds with our database built from EuPathDB and RefSeq-Viral. Based on the mapping locations, it generates the homology information folder.
5. USAGE: Download "HomologyGenerator.sh" and use the following script. Replace archaea with one of the following: bacteria  complete  invertebrate  mitochondrion  other  plant  plasmid  plastid  protozoa  vertebrate_mammalian  vertebrate_other
```
qrsh -l i,h_rt=24:00:00,h_data=25G
module load python/3.6.1
module load bwa
module load samtools
sed -i -e 's/\r$//' /u/project/zarlab/malser/MiCoP/Scripts/HomologyGenerator.sh
chmod +x /u/project/zarlab/malser/MiCoP/Scripts/HomologyGenerator.sh
/u/project/zarlab/malser/MiCoP/Scripts/HomologyGenerator.sh archaea
```
## Generate the start and end coordinates of homologous regions
```
qrsh -l i,h_rt=24:00:00,h_data=25G
module load python/3.6.1
python3 /u/project/zarlab/malser/MiCoP/Scripts/BuildHomologyCoverage.py /u/scratch2/scratch2/m/malser/HomologyInformation/ /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/HomologyInformation_Regions/ 
```
