# call the program using: python ExtractUniqueReads.py SRR3546361.sam UniqueReads.txt > UniqueReads_FullList.sam
import argparse
import sys
import os

def parseargs():    # handle user arguments
	parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
	parser.add_argument('bwa', help='BWA abundances results file. Required.')
	parser.add_argument('IDs', help='Uniquely mapped read IDs File. Required.')
	args = parser.parse_args()
	return args

args = parseargs()
ReadIDfile = open(args.IDs, 'r')
head, tail = os.path.split(args.bwa)
ReadSetName = (tail.split(".")[0])

for line in ReadIDfile:
	readID = str(ReadSetName + '.' + line.strip())
	infile = open(args.bwa, 'r')
	for line in infile:
		splits = line.strip().split('\t')
		IDFile = readID.split('.')
		BAMFile = splits[0].split('.')
		if int(IDFile[1]) == int(BAMFile[1]):
			print str(line.strip())
	infile.close()
ReadIDfile.close()