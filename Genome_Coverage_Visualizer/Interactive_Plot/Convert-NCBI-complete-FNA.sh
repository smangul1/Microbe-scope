#!/bin/bash
set -e  # exit immediately if error occurs

# qrsh -l i,h_rt=24:00:00,h_data=25G
# sed -i -e 's/\r$//' Convert-NCBI-complete-FNA.sh
# chmod +x Convert-NCBI-complete-FNA.sh
# module load python/3.6.1
# ./Convert-NCBI-complete-FNA.sh /u/flashscratch/flashscratch2/m/malser/MiCoP_July2018 Bacteria


dataDir=$1
case "$dataDir" in
*/)
    dataDir="$dataDir"
    ;;
*)
    dataDir="$dataDir/"
    ;;
esac

Tax=$2
#dataDir="/u/flashscratch/flashscratch1/d/dkim/NCBI-Archaea-DB"

Subdirectory=$(ls $dataDir)
for file in $Subdirectory
do
	if [[ $file == *.fna ]]
	then
		if [[ "$(grep -i 'complete genome' "$file"|wc -l)">0  &&  "$(grep -i 'complete genome' "$file"|grep -i -v 'plasmid'|grep -i -v 'chromosome'|grep -i -v 'scaffold'|grep -i -v 'contig'|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} complete>> NCBI-${Tax}.fasta
		#--------------------------------------------------------
		elif [[ "$(grep -i 'complete genome' "$file"|wc -l)">0  &&  "$(grep -i 'complete genome' "$file"|grep -i 'chromosome'|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} chroC>> NCBI-${Tax}.fasta
		
		elif [[ "$(grep -i 'chromosome' "$file"|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} chromosome>> NCBI-${Tax}.fasta
		#--------------------------------------------------------		
		
		elif [[ "$(grep -i 'complete genome' "$file"|wc -l)">0  &&  "$(grep -i 'complete genome' "$file"|grep -i 'scaffold'|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} scafC>> NCBI-${Tax}.fasta
		
		elif [[ "$(grep -i 'scaffold' "$file"|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} scaffold>> NCBI-${Tax}.fasta					
		#--------------------------------------------------------
		elif [[ "$(grep -i 'complete genome' "$file"|wc -l)">0  &&  "$(grep -i 'complete genome' "$file"|grep -i 'contig'|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} contC>> NCBI-${Tax}.fasta
		elif [[ "$(grep -i 'contig' "$file"|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} contig>> NCBI-${Tax}.fasta
		#--------------------------------------------------------
		elif [[ "$(grep -i 'complete genome' "$file"|wc -l)">0  &&  "$(grep -i 'complete genome' "$file"|grep -i 'plasmid'|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} plasC>> NCBI-${Tax}.fasta
		elif [[ "$(grep -i 'plasmid' "$file"|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} plasmid>> NCBI-${Tax}.fasta
		#--------------------------------------------------------
		elif [[ "$(grep -i 'strain' "$file"|wc -l)">0 ]]
		then
			python3 Convert-NCBI-complete-FNA.py ${file} strain>> NCBI-${Tax}.fasta
		#--------------------------------------------------------
		else
			python3 Convert-NCBI-complete-FNA.py ${file} others>> NCBI-${Tax}.fasta
		fi
	fi
done

