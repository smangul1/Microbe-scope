# samtools view /u/scratch2/scratch2/m/malser/MergedEuPathDB/EuPathDB_Merged_fungidb_ConcatContigs.bam | python3 /u/project/zarlab/malser/MiCoP/Scripts/homology_per_genome.py /dev/fd/0 /u/scratch2/scratch2/m/malser/HomologyInformation/


import argparse
import sys
import os
import matplotlib.pyplot as plt
from errno import EEXIST
from os import makedirs,path


   
# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='save each mapping from .bam file to a separated .bam file named by the organism name')
	parser.add_argument('RSDB', help='Directory of Merged EuPathDB database. Required.')
	parser.add_argument('EPDB', help='Directory to save .bam files for each organism. Required.')
	args = parser.parse_args()
	return args

args = parseargs()
if(str(args.EPDB)[len(args.EPDB)-1]=='/'):
	mypath= str(args.EPDB)
else:
	mypath= str(args.EPDB)+'/'	

with open(args.RSDB, 'r') as f:
	try:
		for line in f:
			splits = line.strip().split('\t')
			organism_name = str(splits[2].rstrip().split('=')[1])
			start_location = splits[3].rstrip()
			
			text_file = open(mypath+organism_name+'.txt', "a+")
			text_file.write(start_location+"\n")
			text_file.close()
										
	except Exception as e:
		raise e
		print(args.RSDB+ " file is empty or doesn't exist!")