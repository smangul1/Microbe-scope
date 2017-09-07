# python3 /u/project/zarlab/malser/MiCoP/Scripts/NonoverlappingSeedGenerator.py /u/scratch2/scratch1/d/dkim/NCBI-RefSeq_filtered/archaea/archaea.1.1.genomic.fna
import argparse


# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='Generate all non-redundunt non-overlapping seeds from many sequences')
	parser.add_argument('CSVF', help='Directory of all .csv files that are generated. Required.')
	args = parser.parse_args()
	return args

args = parseargs()
SeedSize = 30

if str(args.CSVF).endswith(".genomic.fna"):
	with open(str(args.CSVF)) as fin:
		sequence=""
		for line in fin:				
			if line[0]!=('>'):
				sequence=sequence+line.rstrip()
			elif line[0]==('>'):
				#print(sequence)
				if len(sequence) >=SeedSize:
					Ex=len(sequence)%SeedSize
					for SeedNo in range(0, int(len(sequence)/SeedSize)):
						print(str(sequence[(SeedNo*SeedSize):((SeedNo+1)*SeedSize)-1]))
					#Check the last seed if the sequence is indivisible by the seed length
					if Ex>0:
						print(str(sequence[len(sequence)-1-SeedSize:len(sequence)-1]))
					sequence=""			
# in case there is only a single genome in the file		
if sequence!="":
	if len(sequence) >=SeedSize:
		Ex=len(sequence)%SeedSize
		for SeedNo in range(0, int(len(sequence)/SeedSize)):
			print(str(sequence[(SeedNo*SeedSize):((SeedNo+1)*SeedSize)-1]))
		#Check the last seed if the sequence is indivisible by the seed length
		if Ex>0:
			print(str(sequence[len(sequence)-1-SeedSize:len(sequence)-1]))
		sequence=""	
# # python3 /u/project/zarlab/malser/MiCoP/Scripts/NonoverlappingSeedGenerator.py /u/scratch2/scratch2/m/malser/NCBI-RefSeq_filtered /u/scratch/d/dkim/NCBI-RefSeq_filtered_Seeds
# import argparse
# import sys
# import os
# import numpy as np
# from errno import EEXIST
# from os import makedirs,path
# import textwrap as tw
# import getopt


# # handle user arguments
# def parseargs():    
	# parser = argparse.ArgumentParser(description='Generate all non-redundunt non-overlapping seeds from many sequences')
	# parser.add_argument('CSVF', help='Directory of all .csv files that are generated. Required.')
	# parser.add_argument('OUTF', help='Output directory for seeds. Required.')
	# args = parser.parse_args()
	# return args

# args = parseargs()
# SeedSize = 30
# if(str(args.CSVF)[len(args.CSVF)-1]=='/'):
	# mypath= str(args.CSVF)
# else:
	# mypath= str(args.CSVF)+'/'

# if(str(args.OUTF)[len(args.OUTF)-1]=='/'):
	# outpath= str(args.OUTF)
# else:
	# outpath= str(args.OUTF)+'/'
	
# SeedGlobalCNT=0
# SeedFileCNT=1
# text_file = open(outpath+'RefSeqSeeds_'+str(SeedFileCNT)+'.fastq', "w")
# for file in os.listdir(str(mypath)):
	# try:
		# for subfile in os.listdir(str(mypath+'/'+file)):
			# #if subfile.endswith(".genomic.fna.gz"):
			# if subfile.endswith(".genomic.fna"):
				# #print(subfile)
				# #with gzip.open(str(mypath+'/'+file+'/'+subfile), 'rt') as fin:
				# with open(str(mypath+'/'+file+'/'+subfile)) as fin:
					# sequence=""
					# #SeedCNT=0
					# for line in fin:
						# if int(SeedGlobalCNT)==100_000_000: # save each 10 million seeds in a separate file
							# SeedFileCNT=SeedFileCNT+1
							# SeedGlobalCNT=0
							# text_file = open(outpath+'RefSeqSeeds_'+str(SeedFileCNT)+'.fastq', "w")
							
						# if line[0]!=('>'):
							# sequence=sequence+line.rstrip()
						# elif line[0]==('>'):
							# #print(sequence)
							# if len(sequence) >=SeedSize:
								# Ex=len(sequence)%SeedSize
								# for SeedNo in range(0, int(len(sequence)/SeedSize)):
									# #SeedCNT=SeedCNT+1
									# SeedGlobalCNT=SeedGlobalCNT+1
									# #text_file.write('>'+(str(subfile).rstrip().split('.')[0])+"."+str(SeedCNT)+'\n')
									# text_file.write(str(sequence[(SeedNo*SeedSize):((SeedNo+1)*SeedSize)-1])+'\n')
								# #Check the last seed if the sequence is indivisible on the seed length
								# if Ex>0:
									# #SeedCNT=SeedCNT+1
									# SeedGlobalCNT=SeedGlobalCNT+1
									# #text_file.write('>'+(str(subfile).rstrip().split('.')[0])+"."+str(SeedCNT)+'\n')
									# text_file.write(str(sequence[len(sequence)-1-SeedSize:len(sequence)-1])+'\n')
								# sequence=""		
						# if int(SeedGlobalCNT)==100_000_000:
							# text_file.close()
	# except Exception as e:
		# raise e
		# print("No files found here!")