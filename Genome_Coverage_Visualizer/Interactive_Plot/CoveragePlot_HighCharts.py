# python CoveragePlot.py Read_FullList.sam GenomeInformation.txt 100000 1
import argparse
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from errno import EEXIST
from os import makedirs,path
import textwrap as tw
import getopt


# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
	parser.add_argument('bwa', help='Output of BWA after processing, extraction, and sorting. Required.')
	parser.add_argument('IDs', help='Genome List: Name and length extracted from genome database (.fa). Required.')
	parser.add_argument('WS', help='Plot Window Size. Required.')
	parser.add_argument('CAT', help='Read Category Number: Enter one of the following numbers: (1) Unique Reads, (2) MultiMapped reads within genome, (3) MultiMapped reads across genomes. Required.')
	parser.add_argument('CPD', help='Coverage Plot Directory. Required.')
	args = parser.parse_args()
	return args

args = parseargs()
infile = open(args.bwa, 'r')
		
window_size = int(args.WS) #100000
LineNo = 1
previous_genome = ""
UniqueReads=0
mypath=""
Read_CAT = int(args.CAT) #1 or 2 or 3
if Read_CAT==1:
	rcat='Unique reads #='
	fcat='Unique'
elif Read_CAT==2:
	rcat='MultiMapped reads (within-genome) #='
	fcat='MultiMapped_within'
elif Read_CAT==3:
	rcat='MultiMapped reads (across-genome) #='
	fcat='MultiMapped_across'

if(str(args.CPD)[len(args.CPD)-1]=='/'):
	mypath= str(args.CPD)+'CoveragePlots_'+fcat+'_WS'+str(window_size)+'/'	
else:
	mypath= str(args.CPD)+'/'+'CoveragePlots_'+fcat+'_WS'+str(window_size)+'/'	

try:
	makedirs(mypath)
except OSError as exc: # Python >2.5
	if exc.errno == EEXIST and path.isdir(mypath):
		pass
	else: raise
		
for line in infile:
	splits = line.strip().split('\t')
	#header = str(splits[2].strip())
	location_start = int(splits[3].strip())	
	current_genome = str(splits[2].strip())
	UniqueReads=UniqueReads+1

	if LineNo ==1:
		previous_genome = current_genome
		LineNo = LineNo + 1	
		# Extract the genome information from the database file
		with open(args.IDs, 'r') as f:
			for line2 in f:
				if current_genome in line2:
					splits2 = line2.strip().split('|')
					header = splits2[0].strip()
					split3 = str(splits2[2]).strip().split('=')
					location_max = int(split3[1])
					location_list = [0] * (location_max+1) # we added 1 as we want our mapping range to start from 1-location_max and not 0-location_max
					break
	if str(current_genome) == str(previous_genome): # clustering the reads based on genomes
		for list_no in range(location_start , location_start+int(len(str(splits[9].strip())))):
			if list_no <= location_max:
				location_list[list_no] = location_list[list_no] + 1	
			#else:
			#	sys.stdout.write(str(list_no) +' max: '+ str(location_max)+' genome: '+ str(current_genome)+'\n')
				#raise Exception("POS is out of range: mapping position is larger than the genome size")	
	else:
		
		# #create the coverage file per genome
		val = 0
		window_start = 1
		window_end = 1
		radii = list()
		left_windows = list()
		right_windows = list()
		coverage=0
		for list_no in range(1 , location_max):
			if int(location_list[list_no])>0:
				coverage=coverage+1
			val += int(location_list[list_no])
			window_end += 1
			if list_no % window_size == 0:
				left_windows.append(int(window_start))
				right_windows.append(int(window_end-1))
				radii.append(float(float(val) / float(window_size)))
				#sys.stdout.write("%s\t%d\t%d\t%f\n" % (header, window_start, window_end-1, val / float(window_size)))
				window_start = window_end
				val = 0
		coverage_percentage=((int(coverage)/int(location_max))*100)
		header = header.split('=')[1]
		f = open(mypath+str(header)+'.csv', 'a')
		headerchart='Organism='+header+' -- '+rcat+str(' %s' % '{:,d}'.format(int(int(UniqueReads)-1)))+' -- '+'Coverage='+str('{:,d}'.format(coverage))+'bp out of '+str('{:,d}'.format(location_max))+'bp' +' ('+ str('%.2f%%' % float(float(float(coverage)/float(location_max))*100.0)+')')+' -- '+'Window Size='+ '{:,d}'.format(window_size)+'\n'
		f.write(headerchart)
		for list_no in range(1 , len(left_windows)):
			ss=str(left_windows[list_no])+','+str(radii[list_no])+'\n'
			f.write(ss)
		f.close()
		
		#-----------------------------------------------------------------------------
		#-----------------------------------------------------------------------------
		#move to next genome
		UniqueReads=1
		LineNo = 2
		previous_genome = current_genome
		# Extract the genome information from the database file
		with open(args.IDs, 'r') as f:
			for line2 in f:
				if current_genome in line2:
					splits2 = line2.strip().split('|')
					header = splits2[0].strip()
					split3 = str(splits2[2]).strip().split('=')
					location_max = int(split3[1])
					location_list = [0] * (location_max+1) # we added 1 as we want our mapping range to start from 1-location_max and not 0-location_max
					break
		# as we already read one line so we repeat the code below to not lose it
		for list_no in range(location_start , location_start+int(len(str(splits[9].strip())))):
			if list_no <= location_max:
				location_list[list_no] = location_list[list_no] + 1	
			#else:
			#	sys.stdout.write(str(list_no) +' max: '+ str(location_max)+' genome: '+ str(current_genome)+'\n')
				#raise Exception("POS is out of range: mapping position is larger than the genome size")	


#This is to plot the last genome in the .sam file
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# #create the coverage file per genome
val = 0
window_start = 1
window_end = 1
radii = list()
left_windows = list()
right_windows = list()
coverage=0
for list_no in range(window_start , location_max):
	if int(location_list[list_no])>0:
		coverage=coverage+1
	val += int(location_list[list_no])
	window_end += 1
	if list_no % window_size == 0:
		left_windows.append(int(window_start))
		right_windows.append(int(window_end-1))
		radii.append(float(float(val) / float(window_size)))
		#sys.stdout.write("%s\t%d\t%d\t%f\n" % (header, window_start, window_end-1, val / float(window_size)))
		window_start = window_end
		val = 0
coverage_percentage=((int(coverage)/int(location_max))*100)
header = header.split('=')[1]
f = open(mypath+str(header)+'.csv', 'a')
headerchart='Organism='+header+' -- '+rcat+str(' %s' % '{:,d}'.format(int(int(UniqueReads)-1)))+' -- '+'Coverage='+str('{:,d}'.format(coverage))+'bp out of '+str('{:,d}'.format(location_max))+'bp' +' ('+ str('%.2f%%' % float(float(float(coverage)/float(location_max))*100.0)+')')+' -- '+'Window Size='+ '{:,d}'.format(window_size)+'\n'
f.write(headerchart)
for list_no in range(1 , len(left_windows)):
	ss=str(left_windows[list_no])+','+str(radii[list_no])+'\n'
	f.write(ss)
f.close()
infile.close()