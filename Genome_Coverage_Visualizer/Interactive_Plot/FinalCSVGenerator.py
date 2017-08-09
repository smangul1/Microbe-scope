# python3 FinalCSVGenerator.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi/ /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi/fungi_RefList.txt 200 2 /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi/Unique2

import sys
import os
import csv
import itertools
import argparse
from errno import EEXIST
from os import makedirs,path

# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
	parser.add_argument('bwa', help='Directory of unique, MMWithin, and MMAcross Folders. Required.')
	parser.add_argument('IDs', help='Genome List: Name and length extracted from genome database (.fa). Required.')
	parser.add_argument('WS', help='Plot Window Size. Required.')
	parser.add_argument('CAT', help='Read Category Number: Enter one of the following numbers: (1) Unique Reads, (2) MultiMapped reads within genome, (3) MultiMapped reads across genomes. Required.')
	parser.add_argument('CPD', help='Coverage Plot Directory. Required.')
	args = parser.parse_args()
	return args

args = parseargs()
		
window_size = int(args.WS) #100000

if(str(args.bwa)[len(args.bwa)-1]=='/'):
	RootFolder= str(args.bwa)
else:
	RootFolder= str(args.bwa)+'/'
	
OutputPath= RootFolder+'MiCoP_FinalCSVs_WS'+str(window_size)+'/'	
try:
	makedirs(OutputPath)
except OSError as exc: # Python >2.5
	if exc.errno == EEXIST and path.isdir(OutputPath):
		pass
	else: raise




	
with open(args.IDs, 'r') as f:
	for line2 in f:
		print(line2)
		splits2 = line2.strip().split('|')
		header = splits2[0].strip().split('=')[1]
		
		UniqFile = RootFolder+'CoveragePlots_Unique_WS'+str(window_size)+'/'+str(header)+'.csv'
		MMWFile = RootFolder+'CoveragePlots_MultiMapped_within_WS'+str(window_size)+'/'+str(header)+'.csv'
		MMAFile = RootFolder+'CoveragePlots_MultiMapped_across_WS'+str(window_size)+'/'+str(header)+'.csv'

		filenames = [UniqFile, MMWFile, MMAFile]
		# put files in the order you want concatentated
		csv_names = filenames
		try:
			readers = [csv.reader(open(fn, 'r'), delimiter=',') for fn in csv_names]
			writer = csv.writer(open(OutputPath+str(header)+'.csv', 'w'), delimiter=',')

			for row_chunks in itertools.izip(*readers):
				writer.writerow(list(itertools.chain.from_iterable(row_chunks)))
		except Exception as e:
			print(e)
		# with open(OutputPath+str(header)+'.csv', 'w') as outfile:
			# for fname in filenames:
				# try:
					# with open(fname) as infile:
						# for line in infile:
						# outfile.write(line+"\n")
				# except Exception as e:
					# print(e)
		# outfile.close()
		# infile.close()
f.close()