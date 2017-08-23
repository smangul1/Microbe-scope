# python3 /u/project/zarlab/malser/MiCoP/Scripts/CheckDuplicationFromInputFolder.py /u/scratch2/scratch2/m/malser/NCBI-RefSeq /u/scratch2/scratch2/m/malser/EuPathDB_Organism_List.txt archaea
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
import gzip

   
# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='Check if there is a similar genomes shared between EuPathDB and RefSeq databases based on organism name')
	parser.add_argument('RSDB', help='Directory of NCBI RefSeq database. Required.')
	parser.add_argument('EPDBtxt', help='Directory of txt file that contains all organism names in the EuPathDB. Required.')
	parser.add_argument('FOLDER', help='Specific folder in RefSeq. Required.')
	args = parser.parse_args()
	return args

args = parseargs()
if(str(args.RSDB)[len(args.RSDB)-1]=='/'):
	mypath= str(args.RSDB)
else:
	mypath= str(args.RSDB)+'/'

try:
	for subfile in os.listdir(mypath+str(args.FOLDER)+'/'):
		if subfile.endswith(".genomic.fna.gz"):
			try:
				makedirs(str(mypath[:-1])+'_filtered/'+str(args.FOLDER)+'/')
			except OSError as exc:
				if exc.errno == EEXIST and path.isdir(str(mypath[:-1])+'_filtered/'+str(args.FOLDER)+'/'):
					pass
				else: raise exc
			
			if os.path.exists(str(mypath[:-1])+'_filtered/'+str(args.FOLDER)+'/'+str(subfile[:-3]))==False:
				text_file = open(str(mypath[:-1])+'_filtered/'+str(args.FOLDER)+'/'+str(subfile[:-3]), "w")
				with gzip.open(mypath+str(args.FOLDER)+'/'+str(subfile), 'rt') as fin:
					for line in fin:
						if line[0]==('>'):
							#print(line.rstrip().split(' ')[1])							
							RemoveFlag=0 #don't remove this contig
							ContigName=line
							FirstLine=1
							with open(args.EPDBtxt) as f: #EuPath
								for line2 in f:
									if str(line.rstrip().split(' ')[1]) == str(line2.rstrip().split('_')[0]):
										if str(line.rstrip().split(' ')[2]) == str(line2.rstrip().split('_')[1]):
											print(str(args.FOLDER)+"\\"+subfile+"\\"+ str(line2.rstrip()))
											RemoveFlag=1
											break
						else:
							if RemoveFlag==0:
								if int(FirstLine)==1: # print contig information only once for each contig
									text_file.write(ContigName)
									FirstLine=0
								text_file.write(line)
				text_file.close()
									
except Exception as e:
	raise e
	print("No files found here!")