# python3 FilterNulls_csv.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi/MiCoP_FinalCSVs_smaller
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
	parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
	parser.add_argument('CSVF', help='Directory of all .csv files that are generated. Required.')
	args = parser.parse_args()
	return args

args = parseargs()

if(str(args.CSVF)[len(args.CSVF)-1]=='/'):
	mypath= str(args.CSVF)
else:
	mypath= str(args.CSVF)+'/'	

	
for file in os.listdir(str(mypath)):
	try:
		if file.endswith(".csv"):
			#print("csv file found:\t", file)
			outputFile=str(mypath)+str(file)
			#Create temporary file read/write
			t = tempfile.NamedTemporaryFile(mode="r+")
			#Open input file read-only
			i = open(outputFile, 'r')
			#Copy input file to temporary file, modifying as we go
			for line in i:
				t.write(line.rstrip()+"\n")
			i.close() #Close input file
			t.seek(0) #Rewind temporary file to beginning
			
			#Overwriting original file with temporary file contents     
			o = open(outputFile, "w")  #Reopen input file writable
			LineIndex=0
			for line in t:
				if LineIndex==0 or LineIndex==1 or LineIndex==2:
					o.write(line)
				else:
					splits = line.strip().split(',')
					if (str(splits[1].strip().rstrip())=="null" and str(splits[2].strip().rstrip())=="null" and str(splits[3].strip().rstrip())=="null"):
						continue
					else:
						o.write(line)
				LineIndex=LineIndex+1
			t.close()
			o.close()
			
	except Exception as e:
		raise e
		print("No files found here!")