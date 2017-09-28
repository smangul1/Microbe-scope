# python3 /u/project/zarlab/malser/MiCoP/Scripts/BuildHomologyCoverage.py /u/scratch2/scratch2/m/malser/HomologyInformation/ /u/scratch2/scratch2/m/malser/MergedEuPathDB/MiCoP_DB_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/HomologyInformation_Regions/ 

import argparse
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from errno import EEXIST
from os import makedirs,path
import textwrap as tw
import getopt
import tempfile


# handle user arguments
def parseargs():
	parser = argparse.ArgumentParser(description='Compute the coverage of RefSeq to EuPATHDB.')
	parser.add_argument('HMG', help='Directory of all .txt homology information files. Required.')
	parser.add_argument('REF', help='Genome List: Name and length extracted from genome database. Required.')
	parser.add_argument('HMG2', help='Directory of all .txt modified homology regions files. Required.')
	args = parser.parse_args()
	return args

args = parseargs()

if(str(args.HMG)[len(args.HMG)-1]=='/'):
	mypath= str(args.HMG)
else:
	mypath= str(args.HMG)+'/'	
	

if(str(args.HMG2)[len(args.HMG2)-1]=='/'):
	mypath2= str(args.HMG2)
else:
	mypath2= str(args.HMG2)+'/'	

location_max=0
for file in os.listdir(str(mypath)):
	try:
		if file.endswith(".txt"):
			# Extract the genome length from the database file
			with open(args.REF, 'r') as f:
				for line2 in f:
					if str('>organism='+file[:-4]+' | ') in line2:
						splits2 = line2.strip().split('|')
						split3 = str(splits2[2]).strip().split('=')
						location_max = int(split3[1])
						location_list = [0] * (location_max+1) # we added 1 as we want our mapping range to start from 1-location_max and not 0-location_max
						break
			# Build Coverage array 
			with open(mypath+file, 'r') as f:
				for line in f:
					if len(line.strip()) != 0 :
						location_start=int(line.rstrip())
						for list_no in range(location_start , (location_start+30)):
							#print(str(location_start)+'    '+str(location_max))
							if list_no <= location_max:
								location_list[list_no] = location_list[list_no] + 1	
			# write the homology coverage regions     
			o = open(str(mypath2+file), "w")
			coverage=0
			startCoverage=1
			for list_no in range(1 , location_max+1):
				if int(location_list[list_no])==0:
					if coverage>0:
						o.write(str(startCoverage)+'\t'+ str(int(int(startCoverage)+int(coverage)-1))+'\n')
					coverage=0
					startCoverage=list_no+1
				elif int(location_list[list_no])>0:
					#print(list_no)
					coverage=coverage+1
			if coverage>0: # print last region if no more zeros after it
				o.write(str(startCoverage)+'\t'+ str(int(int(startCoverage)+int(coverage)-1))+'\n')
			o.close()		
	except Exception as e:
		print("No files found here!")
		raise e