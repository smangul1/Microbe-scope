# Use the following command to extract all reference genomes
# awk -F "|" '{print $2}' fungi.names | uniq > RefList.txt
# python ConcatContigs.py RefList.txt fungi.fa > fungi_ConcatContigs.fa


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
				splits = line.strip().split('|')
				LengthSplits = splits[3].strip().split('=')
				TotalLength = TotalLength + int(LengthSplits[1])
				if LineNo == 1: # print the header once for each organism
					HeaderSplits = splits
					LineNo = 1 + LineNo
				try:
					nextLine = next(f)
					while (nextLine[0] !=">"):
						AllContigs= AllContigs.strip().rstrip() + nextLine.strip().rstrip()
						nextLine = next(f)
						if (nextLine[0] ==">") and (query in nextLine):
							splits = nextLine.strip().split('|')
							LengthSplits = splits[3].strip().split('=')
							TotalLength = TotalLength + int(LengthSplits[1])
							nextLine = next(f)
				except StopIteration:
					pass
	if (AllContigs !="") and (TotalLength == len(AllContigs)):	
		sys.stdout.write('>' + HeaderSplits[1] + ' | ' + HeaderSplits[2] + ' | ' + 'length=' + str(TotalLength) + ' | ' + HeaderSplits[4] + '\n')
		sys.stdout.write(AllContigs.strip().rstrip()+'\n')