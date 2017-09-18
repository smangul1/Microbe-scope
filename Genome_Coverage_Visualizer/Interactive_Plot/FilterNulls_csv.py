# python3 /u/project/zarlab/malser/MiCoP/Scripts/FilterNulls_csv.py /u/project/zarlab/malser/MiCoP/eupathdbFasta_ConcatContigs/fungi/MiCoP_FinalCSVs /u/project/zarlab/malser/MiCoP/test/fungi/SRR3546361/fungi_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/HomologyInformation/ 30 200

# python3 /u/project/zarlab/malser/MiCoP/Scripts/FilterNulls_csv.py /u/scratch2/scratch2/m/malser/MiCoP_FinalCSVs /u/project/zarlab/malser/MiCoP/test/fungi/SRR3546361/fungi_RefList_perGenome.txt /u/scratch2/scratch2/m/malser/HomologyInformation/ 30 200

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


# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
	parser.add_argument('CSVF', help='Directory of all .csv files that are generated. Required.')
	parser.add_argument('IDs', help='Genome List: Name and length extracted from genome database (.fa). Required.')
	parser.add_argument('HMGtxt', help='Directory of all .txt files that contain start location (RefSeq Homology Information) for each organism in EuPathDB generated. Required.')
	parser.add_argument('KMER', help='RefSeq k-mer Size. Required.')
	parser.add_argument('WS', help='Plot Window Size. Required.')
	args = parser.parse_args()
	return args

args = parseargs()

if(str(args.CSVF)[len(args.CSVF)-1]=='/'):
	mypath= str(args.CSVF)
else:
	mypath= str(args.CSVF)+'/'	

	
for file in os.listdir(str(mypath)):
	try:
		if file.endswith(".csv"):
			#print("csv file found:\t", file)
			outputFile=str(mypath)+str(file)
			#Create temporary file read/write
			t = tempfile.NamedTemporaryFile(mode="r+")
			#Open input file read-only
			i = open(outputFile, 'r')
			#Copy input file to temporary file, modifying as we go
			for line in i:
				t.write(line.rstrip()+"\n")
			i.close() #Close input file
			t.seek(0) #Rewind temporary file to beginning
			
			############################################## Homology Plot
			# Extract the length of the organism genome and maintain an array of size equals to the genome length
			with open(args.IDs, 'r') as f:
				for line in f:
					if file[:-4] in line:
						splits2 = line.strip().split('|')
						header = splits2[0].strip()
						split3 = str(splits2[2]).strip().split('=')
						location_max = int(split3[1])
						location_list = [0] * (location_max+1) # we added 1 as we want our mapping range to start from 1-location_max and not 0-location_max
						break
			# Check if there is homology information
			if os.path.isfile(args.HMGtxt+file[:-4]+'.txt')==True:
				# Extract homology coverage information 
				Reads=0
				with open(args.HMGtxt+file[:-4]+'.txt', 'r') as f:
					for line in f:
						Reads=Reads+1
						location_start=int(line.rstrip())
						for list_no in range(location_start , location_start+int(args.KMER)):
							if list_no <= location_max:
								location_list[list_no] = location_list[list_no] + 1	
				# Rebuild the homology coverage based on the window size
				val = 0
				window_size=int(args.WS)
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
				if window_end>window_start: # in case last window is less than window size
					left_windows.append(int(window_start))
					right_windows.append(int(window_end-1))
					radii.append(float(float(val) / float(window_end - window_start)))
				##################################
				
				
				#Overwrite original file with temporary file contents     
				o = open(outputFile, "w")  #Reopen input file writable
				LineIndex=0
				for line in t:
					if LineIndex==0:
						o.write(line)
					elif LineIndex==1:	
						ChartSubtitle=line.rstrip()+'<br>'+'RefSeq homologous reads #='+str(' %s' % '{:,d}'.format(int(int(Reads))))+' -- '+'Coverage='+str('{:,d}'.format(coverage))+'bp out of '+str('{:,d}'.format(location_max))+'bp' +' ('+ str('%.2f%%' % float(float(float(coverage)/float(location_max))*100.0)+')')+'\n'
						o.write(ChartSubtitle)
					elif LineIndex==2:
						o.write(line.rstrip()+',RefSeq homologous reads\n')
					else:
						splits = line.strip().split(',')
						if (str(splits[1].strip().rstrip())=="0.0"):
							a=",null"
						else:
							a=","+splits[1].strip().rstrip()
						if (str(splits[2].strip().rstrip())=="0.0"):
							b=",null"
						else:
							b=","+splits[2].strip().rstrip()
						if (str(splits[3].strip().rstrip())=="0.0"):
							c=",null"
						else:
							c=","+splits[3].strip().rstrip()
						if str(radii[LineIndex-3])=="0.0":
							d=",null"
						else:
							d=','+str(radii[LineIndex-3])
						if (a==",null" and b==",null" and c==",null" and d==",null"):
							continue
						else:
							o.write(splits[0]+a+b+c+d+'\n')
					LineIndex=LineIndex+1
				t.close()
				o.close()
			else:
				#Overwrite original file with temporary file contents     
				o = open(outputFile, "w")  #Reopen input file writable
				LineIndex=0
				for line in t:
					if LineIndex==0:
						o.write(line)
					elif LineIndex==1:	
						#coverage=0
						#Reads=0
						#ChartSubtitle=line.rstrip()+'<br>'+'RefSeq homologous reads #='+str(' %s' % '{:,d}'.format(int(int(Reads))))+' -- '+'Coverage='+str('{:,d}'.format(coverage))+'bp out of '+str('{:,d}'.format(location_max))+'bp' +' ('+ str('%.2f%%' % float(float(float(coverage)/float(location_max))*100.0)+')')+'\n'
						o.write(line)
					elif LineIndex==2:
						o.write(line.rstrip()+',RefSeq homologous reads\n')
					else:
						splits = line.strip().split(',')
						if (str(splits[1].strip().rstrip())=="0.0"):
							a=",null"
						else:
							a=","+splits[1].strip().rstrip()
						if (str(splits[2].strip().rstrip())=="0.0"):
							b=",null"
						else:
							b=","+splits[2].strip().rstrip()
						if (str(splits[3].strip().rstrip())=="0.0"):
							c=",null"
						else:
							c=","+splits[3].strip().rstrip()
						d=",null"
						if (a==",null" and b==",null" and c==",null"):
							continue
						else:
							o.write(splits[0]+a+b+c+d+'\n')
						
					LineIndex=LineIndex+1
				t.close()
				o.close()
		#elif 'Mapped_Genome_List.txt' in file:	
	except Exception as e:
		raise e
		print("No files found here!")
		
		