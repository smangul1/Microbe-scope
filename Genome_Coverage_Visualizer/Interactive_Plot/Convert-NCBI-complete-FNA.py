# Use the following command to extract all reference genomes
# python Convert-NCBI-complete-FNA.py fungi.fa > fungi_ConcatContigs.fa

import argparse
import sys
import os
from itertools import groupby
 
# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='Concates all contigs for each organism')
	parser.add_argument('RefDB', help='FASTQ of all reference genomes. Required File.')
	parser.add_argument('MergeRef', help='select to merge: complete genome, chromosome, scaffold, or contig.')
	args = parser.parse_args()
	return args

args = parseargs()

LineNo = 1
AllContigs=""


if args.MergeRef.lower() in "complete":
	exIn="complete genome"
	exIn2="complete genome"
	SO="Complete_genome"
	ex1="contig"
	ex2="scaffold"
	ex3="chromosome"
	ex4="plasmid"
	ex5="complete genome"
	
elif args.MergeRef.lower() in "contc":
	exIn="contig"
	exIn2="complete genome"
	SO="Contig"
	ex1="plasmid"
	ex2="scaffold"
	ex3="chromosome"
	ex4="chromosome"
	ex5="complete genome"
	
elif args.MergeRef.lower() in "scafc":
	exIn="scaffold"
	exIn2="complete genome"
	SO="Scaffold"
	ex1="contig"
	ex2="contig"
	ex3="plasmid"
	ex4="chromosome"
	ex5="complete genome"
	
elif args.MergeRef.lower() in "chroc":
	exIn="chromosome"
	exIn2="complete genome"
	SO="Chromosome"
	ex1="contig"
	ex2="scaffold"
	ex3="plasmid"
	ex4="plasmid"
	ex5="complete genome"
	
elif args.MergeRef.lower() in "plasc":
	exIn="plasmid"
	exIn2="complete genome"
	SO="plasmid"
	ex1="contig"
	ex2="scaffold"
	ex3="chromosome"
	ex4="scaffold"
	ex5="complete genome"
	
elif args.MergeRef.lower() in "contig":
	exIn="contig"
	exIn2="contig"
	SO="Contig"
	ex1="complete genome"
	ex2="scaffold"
	ex3="chromosome"
	ex4="plasmid"
	ex5="aaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	
elif args.MergeRef.lower() in "scaffold":
	exIn="scaffold"
	exIn2="scaffold"
	SO="Scaffold"
	ex1="contig"
	ex2="complete genome"
	ex3="chromosome"
	ex4="complete genome"
	ex5="aaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	
elif args.MergeRef.lower() in "chromosome":
	exIn="chromosome"
	exIn2="chromosome"
	SO="Chromosome"
	ex1="contig"
	ex2="scaffold"
	ex3="plasmid"
	ex4="complete genome"
	ex5="aaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	
elif args.MergeRef.lower() in "plasmid":
	exIn="plasmid"
	exIn2="plasmid"
	SO="plasmid"
	ex1="contig"
	ex2="scaffold"
	ex3="chromosome"
	ex4="complete genome"
	ex5="aaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	
elif args.MergeRef.lower() in "strain":
	exIn="strain"
	exIn2=">"
	SO="Strain"
	ex1="contig"
	ex2="scaffold"
	ex3="complete"
	ex4="scaffold"
	ex5="scaffold"

	
elif args.MergeRef.lower() in "others":
	exIn=">"
	exIn2=">"
	SO="Others"
	ex1="scaffold"
	ex2="scaffold"
	ex3="scaffold"
	ex4="scaffold"
	ex5="scaffold"
	
	
with open(args.RefDB, 'r') as f:
	if args.MergeRef.lower() in "strain":
		for line in f:
			if (line[0] ==">"):
				if LineNo == 1: # extract the header once for each organism
					organism="organism="+(str(args.RefDB).split("_genomic.fna")[0])+"_"+line.split(".")[0].split(">")[1]
					LineNo = 1 + LineNo
				try:
					nextLine = next(f)
					while (nextLine[0] !=">"):
						AllContigs= AllContigs.strip().rstrip() + nextLine.strip().rstrip()
						nextLine = next(f)
						if (nextLine[0] ==">"):
							sys.stdout.write('>' + organism + ' | ' + "version=Not_Reported" + ' | ' + 'length=' + str(len(AllContigs)) + ' | ' + SO + '\n')
							sys.stdout.write(AllContigs.strip().rstrip().upper()+'\n')
							AllContigs= ""
							organism="organism="+(str(args.RefDB).split("_genomic.fna")[0])+"_"+nextLine.split(".")[0].split(">")[1]
							nextLine = next(f)
				except StopIteration:
					pass
	else:
		for line in f:
			if (line[0] ==">"):
				if ((exIn.lower() in line.lower()) and (exIn2.lower() in line.lower()) and (ex1.lower() not in line.lower()) and (ex2.lower() not in line.lower()) and (ex3.lower() not in line.lower())and (ex4.lower() not in line.lower())):
					if LineNo == 1: # extract the header once for each organism
						organism="organism="+(str(args.RefDB).split("_genomic.fna")[0])
						LineNo = 1 + LineNo
					try:
						nextLine = next(f)
						while (nextLine[0] !=">"):
							AllContigs= AllContigs.strip().rstrip() + nextLine.strip().rstrip()
							nextLine = next(f)
							if ((nextLine[0] ==">") and (ex5.lower() not in nextLine.lower()) and (exIn2.lower() in line.lower()) and  (exIn.lower() in nextLine.lower()) and (ex1.lower() not in nextLine.lower()) and (ex2.lower() not in nextLine.lower()) and (ex3.lower() not in nextLine.lower())and (ex4.lower() not in nextLine.lower())):
								nextLine = next(f)
					except StopIteration:
						pass
	if (AllContigs !=""):	
		sys.stdout.write('>' + organism + ' | ' + "version=Not_Reported" + ' | ' + 'length=' + str(len(AllContigs)) + ' | ' + SO + '\n')
		sys.stdout.write(AllContigs.strip().rstrip().upper()+'\n')