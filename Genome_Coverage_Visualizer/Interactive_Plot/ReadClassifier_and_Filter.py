# python ReadClassifier.py SRR3546361_MergedContigs_Sorted.sam 1 > Read_FullList.sam


import argparse
import sys
import os
import re
import random

def parseargs():    # handle user arguments
	parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
	parser.add_argument('bwa', help='BWA abundances results file. Required.')
	parser.add_argument('CAT', help='Read Category Number: Enter one of the following numbers: (1) Unique Reads, (2) MultiMapped reads within genome, (3) MultiMapped reads across genomes. Required.')
	args = parser.parse_args()
	return args

args = parseargs()
infile = open(args.bwa, 'r')

Read_CAT = int(args.CAT) #1 or 2 or 3
	
current_read=""
prev_read=""
current_ref=""
prev_ref=""

index=1
MMWithin=1
SameReadCounter=0
MM_Storage=[]
MMWithin_Storage=[]
#Unique_Storage=[]
CommonRef=0
for line in infile:
	splits = line.strip().split('\t')
	current_read = splits[0].strip()
	current_ref = splits[2].strip()
	if index==1:
		prev_read = current_read
		prev_ref = current_ref
		index=index+1
	result = re.findall('\\b'+current_read+'\\b', prev_read)
	if len(result)>0: # if current_read==prev_read:
		SameReadCounter=SameReadCounter+1
		#Unique_Storage.append(splits)
		MM_Storage.append(splits)
		ref_result = re.findall('\\b'+current_ref+'\\b', prev_ref)
		if len(ref_result)>0:
			CommonRef=CommonRef+1
		if len(ref_result)>0 and MMWithin==1: # if current_ref==prev_ref nad the this read is still MMWithin:
			MMWithin=1 #so far this read is still MMWithin
			#MMWithin_Storage.append(splits)
		else:
			MMWithin=2
	else:
		#Print MMWithin reads
		#Nominate best Multimapped read within genomes based on edit distance.
		if MMWithin==1 and SameReadCounter>1 and Read_CAT==2:
			try:
				EDFlag=[x[11] for x in MM_Storage]
				minEditDistance = min([x[5:] for x in EDFlag])
			except:
				minEditDistance = -1
			if minEditDistance!=-1:
				minED_Storage=[]
				for Litem in range(0,len(MM_Storage)):
					if (EDFlag[Litem].strip().split(':')[2]==minEditDistance):
						minED_Storage.append(MM_Storage[Litem])
			if (len(minED_Storage)==1):
				for item in minED_Storage:
					ThisLine=""
					for Litem in range(0,len(item)):
						if Litem==len(item):
							ThisLine=ThisLine+item[Litem]
						else:
							ThisLine=ThisLine+item[Litem]+'\t'
					print(ThisLine)
			#Nominate best Multimapped read within genomes based on alignment score.
			else:
				try:
					ASFlag=[x[13] for x in MM_Storage]
					maxAlignmentScore = max([x[5:] for x in ASFlag])
				except:
					maxAlignmentScore = -1
				if maxAlignmentScore!=-1:
					maxAS_Storage=[]
					for Litem in range(0,len(MM_Storage)):
						if (ASFlag[Litem].strip().split(':')[2]==maxAlignmentScore):
							maxAS_Storage.append(MM_Storage[Litem])
				if (len(maxAS_Storage)==1):
					for item in maxAS_Storage:
						ThisLine=""
						for Litem in range(0,len(item)):
							if Litem==len(item):
								ThisLine=ThisLine+item[Litem]
							else:
								ThisLine=ThisLine+item[Litem]+'\t'
						print(ThisLine)
				#Nominate best Multimapped read within genomes based on random assignment.
				else:
					item =maxAS_Storage[random.randint(0, len(maxAS_Storage)-1)]
					ThisLine=""
					for Litem in range(0,len(item)):
						if Litem==len(item):
							ThisLine=ThisLine+item[Litem]
						else:
							ThisLine=ThisLine+item[Litem]+'\t'
					print(ThisLine)

				#print(MM_Storage)
			# for item in MM_Storage:
				# ThisLine=""
				# for Litem in range(0,len(item)):
					# if Litem==len(item):
						# ThisLine=ThisLine+item[Litem]
					# else:
						# ThisLine=ThisLine+item[Litem]+'\t'
				# print(ThisLine)
		#Print MMAcross reads
		# if there are differerent genomes, no duplicated references, not Unique read, and in MM Across mode
		if MMWithin==2 and CommonRef==1 and SameReadCounter>1 and Read_CAT==3: 
			for item in MM_Storage:
				ThisLine=""
				for Litem in range(0,len(item)):
					if Litem==len(item):
						ThisLine=ThisLine+item[Litem]
					else:
						ThisLine=ThisLine+item[Litem]+'\t'
				print(ThisLine)
		MM_Storage=[]
		# #Print Unique Reads
		# if SameReadCounter<=1 and Read_CAT==1:
			# for item in Unique_Storage:
				# ThisLine=""
				# for Litem in range(0,len(item)):
					# if Litem==len(item):
						# ThisLine=ThisLine+item[Litem]
					# else:
						# ThisLine=ThisLine+item[Litem]+'\t'
				# print(ThisLine)
		#Unique_Storage=[]
		MM_Storage.append(splits)
		#Unique_Storage.append(splits)
		MMWithin=1
		SameReadCounter=1
		CommonRef=1
		
	prev_read = current_read
	prev_ref = current_ref

# If last read is MMWithin, print it
if MMWithin==1 and SameReadCounter>1 and Read_CAT==2:
	for item in MM_Storage:
		ThisLine=""
		for Litem in range(0,len(item)):
			if Litem==len(item):
				ThisLine=ThisLine+item[Litem]
			else:
				ThisLine=ThisLine+item[Litem]+'\t'
		print(ThisLine)
# If last read is MMAcross, print it
if MMWithin==2 and CommonRef==1 and SameReadCounter>1 and Read_CAT==3: 
	for item in MM_Storage:
		ThisLine=""
		for Litem in range(0,len(item)):
			if Litem==len(item):
				ThisLine=ThisLine+item[Litem]
			else:
				ThisLine=ThisLine+item[Litem]+'\t'
		print(ThisLine)
# If last read is Unique, print it
# if SameReadCounter==1 and Read_CAT==1:
	# sys.stdout.write(line)
infile.close()
