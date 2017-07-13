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

mypath= str(args.CPD)+'CoveragePlots_'+fcat+'_WS'+str(window_size)+'/'	
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
		#creat the plot 
		bottom = 8
		truncate_to = 2  # this needs to be a power of two since we are plotting on a sqrt scale
		units = 'M'
		num_labels = 8
		figure_letter = ''
		
		# Helper rotate function
		def rotate(l, n):
			return l[-n:] + l[:-n]
		
		N = len(radii)
		radii = rotate(radii, -int(np.floor(len(radii) / float(4))))  # rotate 90 degress counter clockwise
		#radii = np.flip(np.array(radii), 0)  # make it go clockwise
		radii = np.sqrt(radii)  # do it on a sqrt scale
		# Truncate the radii to the given truncate_to
		radii_truncated = list()
		for val in radii:
			if val > truncate_to:
				val = truncate_to
			radii_truncated.append(val)
		radii_truncated = np.array(radii_truncated)
		radii = radii_truncated  # replace with truncated value
		max_height = int(np.ceil(max(radii)))  # outer ring location

		# Create outer ring labels in Kb or Mb
		genome_length = max(right_windows)
		genome_locations = np.floor(np.linspace(0, genome_length, num_labels))
		labels = list()
		if units == 'K':
			for i in range(len(genome_locations)):
				labels.append('%.1f Kbp' % (genome_locations[i] / float(1000)))
		elif units == 'M':
			for i in range(len(genome_locations)):
				labels.append('%.1f Mbp' % (genome_locations[i] / float(1000000)))
		elif units == 'bp':
			for i in range(len(genome_locations)):
				labels.append('%d bp' % genome_locations[i])
		else:
			raise Exception('Unknown unit type. Pick one of "bp", "K" or "M"')

		labels.reverse()  # make labels go clockwise
		labels = rotate(labels, int(np.floor(len(labels) / float(4))))  # rotate 90 degrees counter clockwise
		labels.insert(0, labels[-1])  # start at 0
		labels = labels[0:num_labels]  # make correct length

		theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)  # location of bars (evenly across 0->2*Pi)
		width = (2*np.pi) / N  # width of bars

		# Do all the plotting and decorating
		plt.figure(figsize=(8, 8))
		ax = plt.subplot(111, polar=True)  # make plot
		bars = ax.bar(theta, radii, width=width, bottom=bottom)  # plot data
		ax.set_xticklabels(labels)  # put the labels on
		ax.set_thetagrids(np.linspace(0, 360, num_labels, endpoint=False), frac=1.03)  # make labels not so close

		# put labels on inner/outer rings
		ax.set_rgrids([bottom, bottom + max_height],  # plotted on sqrt scale
					labels=['0 X', '%.1f X' % (max_height**2)],  # but the actual value is ^2 of what's given
					angle=90, va='top', ha='center', color='b')
		ax.grid(linewidth=0)  # get rid of all the grid lines except the outer one (clear where it starts)
		ax.spines['polar'].set_alpha(0.1)  # make the rings lighter

		# add small lines to designate the location of the labels
		inner_radius = bottom
		outer_radius = bottom + max_height
		for angle in np.linspace(0, 360, num_labels, endpoint=False):
			# Recall that we are in polar, so (theta, r)
			#plt.plot([angle * np.pi / 180., angle * np.pi / 180.], [bottom, bottom + max_height], color='k', alpha=0.1)
			plt.plot([angle * np.pi / 180., angle * np.pi / 180.], [bottom + 0.75*max_height, bottom + max_height], color='k', alpha=0.1)

		# Set the ylim so it doesn't scale to the newly plotted lines
		plt.ylim([0, bottom + max_height])

		# Figure letter
		font = {'family': 'serif', 
				'color':  'black',
				'weight': 'normal',
				'size': 18,
				}
		coverage_font = {'family': 'serif', 
				'color':  'red',
				'weight': 'normal',
				'size': 9,
				}
		if figure_letter != '':
			ax.text(-.1, 1, '%s)' % figure_letter, horizontalalignment='left', verticalalignment='bottom', fontdict=font, transform=ax.transAxes)
		header = header.split('=')[1]
		
		ax.text(0.25,0.56, 'Organism='+header, horizontalalignment='left', verticalalignment='center', fontdict=coverage_font, transform=ax.transAxes)
		ax.text(0.25,0.52, rcat+' %s' % '{:,d}'.format(int(int(UniqueReads)-1)), horizontalalignment='left', verticalalignment='center', fontdict=coverage_font, transform=ax.transAxes)
		ax.text(0.25,0.48,'Coverage='+'{:,d}'.format(coverage)+'bp out of '+'{:,d}'.format(location_max)+'bp' +' ('+ str('%.2f%%' % float(float(float(coverage)/float(location_max))*100.0)+')'), horizontalalignment='left', verticalalignment='center', fontdict=coverage_font, transform=ax.transAxes)
		ax.text(0.25,0.44, 'Window Size='+ '{:,d}'.format(window_size), horizontalalignment='left', verticalalignment='center', fontdict=coverage_font, transform=ax.transAxes)
		
		plt.savefig(mypath+str(header)+'.png')
		#plt.savefig(os.path.abspath(output_file))
		plt.close()
		
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
#creat the plot 
bottom = 8
truncate_to = 2  # this needs to be a power of two since we are plotting on a sqrt scale
units = 'M'
num_labels = 8
figure_letter = ''

# Helper rotate function
def rotate(l, n):
	return l[-n:] + l[:-n]

N = len(radii)
radii = rotate(radii, -int(np.floor(len(radii) / float(4))))  # rotate 90 degress counter clockwise
#radii = np.flip(np.array(radii), 0)  # make it go clockwise
radii = np.sqrt(radii)  # do it on a sqrt scale
# Truncate the radii to the given truncate_to
radii_truncated = list()
for val in radii:
	if val > truncate_to:
		val = truncate_to
	radii_truncated.append(val)
radii_truncated = np.array(radii_truncated)
radii = radii_truncated  # replace with truncated value
max_height = int(np.ceil(max(radii)))  # outer ring location

# Create outer ring labels in Kb or Mb
genome_length = max(right_windows)
genome_locations = np.floor(np.linspace(0, genome_length, num_labels))
labels = list()
if units == 'K':
	for i in range(len(genome_locations)):
		labels.append('%.1f Kbp' % (genome_locations[i] / float(1000)))
elif units == 'M':
	for i in range(len(genome_locations)):
		labels.append('%.1f Mbp' % (genome_locations[i] / float(1000000)))
elif units == 'bp':
	for i in range(len(genome_locations)):
		labels.append('%d bp' % genome_locations[i])
else:
	raise Exception('Unknown unit type. Pick one of "bp", "K" or "M"')

labels.reverse()  # make labels go clockwise
labels = rotate(labels, int(np.floor(len(labels) / float(4))))  # rotate 90 degrees counter clockwise
labels.insert(0, labels[-1])  # start at 0
labels = labels[0:num_labels]  # make correct length

theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)  # location of bars (evenly across 0->2*Pi)
width = (2*np.pi) / N  # width of bars

# Do all the plotting and decorating
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)  # make plot
bars = ax.bar(theta, radii, width=width, bottom=bottom)  # plot data
ax.set_xticklabels(labels)  # put the labels on
ax.set_thetagrids(np.linspace(0, 360, num_labels, endpoint=False), frac=1.03)  # make labels not so close

# put labels on inner/outer rings
ax.set_rgrids([bottom, bottom + max_height],  # plotted on sqrt scale
			labels=['0 X', '%.1f X' % (max_height**2)],  # but the actual value is ^2 of what's given
			angle=90, va='top', ha='center', color='b')
ax.grid(linewidth=0)  # get rid of all the grid lines except the outer one (clear where it starts)
ax.spines['polar'].set_alpha(0.1)  # make the rings lighter

# add small lines to designate the location of the labels
inner_radius = bottom
outer_radius = bottom + max_height
for angle in np.linspace(0, 360, num_labels, endpoint=False):
	# Recall that we are in polar, so (theta, r)
	#plt.plot([angle * np.pi / 180., angle * np.pi / 180.], [bottom, bottom + max_height], color='k', alpha=0.1)
	plt.plot([angle * np.pi / 180., angle * np.pi / 180.], [bottom + 0.75*max_height, bottom + max_height], color='k', alpha=0.1)

# Set the ylim so it doesn't scale to the newly plotted lines
plt.ylim([0, bottom + max_height])

# Figure letter
font = {'family': 'serif', 
		'color':  'black',
		'weight': 'normal',
		'size': 18,
		}
coverage_font = {'family': 'serif', 
		'color':  'red',
		'weight': 'normal',
		'size': 9,
		}
if figure_letter != '':
	ax.text(-.1, 1, '%s)' % figure_letter, horizontalalignment='left', verticalalignment='bottom', fontdict=font, transform=ax.transAxes)
header = header.split('=')[1]
ax.text(0.25,0.56, 'Organism='+header, horizontalalignment='left', verticalalignment='center', fontdict=coverage_font, transform=ax.transAxes)
ax.text(0.25,0.52, rcat+' %s' % '{:,d}'.format(int(int(UniqueReads)-1)), horizontalalignment='left', verticalalignment='center', fontdict=coverage_font, transform=ax.transAxes)
ax.text(0.25,0.48,'Coverage='+'{:,d}'.format(coverage)+'bp out of '+'{:,d}'.format(location_max)+'bp' +' ('+ str('%.2f%%' % float(float(float(coverage)/float(location_max))*100.0)+')'), horizontalalignment='left', verticalalignment='center', fontdict=coverage_font, transform=ax.transAxes)
ax.text(0.25,0.44, 'Window Size='+ '{:,d}'.format(window_size), horizontalalignment='left', verticalalignment='center', fontdict=coverage_font, transform=ax.transAxes)

plt.savefig(mypath+str(header)+'.png')
plt.close()
infile.close()