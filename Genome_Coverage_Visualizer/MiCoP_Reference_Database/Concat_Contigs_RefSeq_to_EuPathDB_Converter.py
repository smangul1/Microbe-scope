# Use the following command to extract all reference genomes
# awk -F "|" '{print $2}' fungi.names | uniq > RefList.txt
# python Concat_Contigs_RefSeq_to_EuPathDB_Converter.py RefList.txt fungi.fa > fungi_ConcatContigs.fa


import argparse
import sys
import os
from itertools import groupby

# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='Concates all contigs for each organism')
	parser.add_argument('OrganismList', help='List of organism names. Required File.')
	parser.add_argument('RefDB', help='FASTQ of all reference genomes. Required File.')
	args = parser.parse_args()
	return args

args = parseargs()
with open(args.OrganismList, 'r') as f:
    queries = [l.strip() for l in f]

for query in queries:
	LineNo = 1
	AllContigs=""
	TotalLength=0
	nextLine=""
	with open(args.RefDB, 'r') as f:
		for line in f:
			if (query in line):
				splits = line.rstrip().split(' ', 1)[1]
				
				if LineNo == 1: # extract the header once for each organism
					organism="organism="+str(query).replace(" ", "_")
					if (len(splits.rstrip().split(','))==1):
						SO="SO=Not_Reported"
					else:
						SO="SO="+splits.rstrip().split(',')[len(splits.rstrip().split(','))-1].replace(" ", "_")
					LineNo = 1 + LineNo
				try:
					nextLine = next(f)
					while (nextLine[0] !=">"):
						AllContigs= AllContigs.strip().rstrip() + nextLine.strip().rstrip()
						nextLine = next(f)
						if (nextLine[0] ==">") and (query in nextLine):
							TotalLength = len(AllContigs)
							nextLine = next(f)
				except StopIteration:
					pass
	if (AllContigs !=""):	
		sys.stdout.write('>' + organism + ' | ' + "version=Not_Reported" + ' | ' + 'length=' + str(TotalLength) + ' | ' + SO + '\n')
		sys.stdout.write(AllContigs.strip().rstrip()+'\n')