# python3 /u/project/zarlab/malser/MiCoP/Scripts/FASTQformatter.py /u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered/archaea.1.1.genomic.fna archaea
import argparse

# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='Generate all non-redundunt non-overlapping seeds from many sequences')
	parser.add_argument('CSVF', help='Directory of all .csv files that are generated. Required.')
	parser.add_argument('OUTF', help='Output directory for seeds. Required.')
	args = parser.parse_args()
	return args

args = parseargs()

SeedCNT=0

with open(str(args.CSVF)) as fin:
	for line in fin:				
		if line and line.strip():
			SeedCNT=SeedCNT+1
			print('> '+str(args.OUTF)+"."+str(SeedCNT))
			print(line.rstrip())