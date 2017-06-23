# call the program using: python ExtractCoverage.py UniqueReads_FullList.sam GenomeInformation.txt > UniqueReads_FullList.sam
import argparse
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import getopt


# handle user arguments
def parseargs():    
	parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
	parser.add_argument('bwa', help='Uniquely mapped read alignment File. Required.')
	parser.add_argument('IDs', help='Genome Name and length Information File. Required.')
	args = parser.parse_args()
	return args

args = parseargs()
#ReadIDfile = open(args.IDs, 'r')
infile = open(args.bwa, 'r')

#head, tail = os.path.split(args.bwa)
#ReadSetName = (tail.split(".")[0])
#readID = str(ReadSetName + '.' + line.strip())

window_size = 1000
LineNo = 1
location_max = 30000000 #it should come from the genome file but we fix it here and we will change later
location_list = [0] * (location_max+1) # we added 1 as we want our mapping range to start from 1-location_max and not 0-location_max
previous_genome = ""
for line in infile:
	splits = line.strip().split('\t')
	header = str(splits[2].strip())
	location_start = int(splits[3].strip())
	#if (location_start+ int(len(str(splits[10].strip()))) -1) > location_max:
		#raise Exception("POS is out of range: mapping position is larger than the genome size")		
	current_genome = str(splits[2].strip())
	if LineNo ==1:
		previous_genome = current_genome
	if str(current_genome) == str(previous_genome): # clustering the reads based on genomes
		#print str(line)
		#print str(len(str(splits[10].strip())))
		if (location_start+ int(len(str(splits[10].strip()))) -1) < location_max:
			for list_no in range(location_start , location_start+int(len(str(splits[10].strip())))):
				location_list[list_no] = location_list[list_no] + 1
				#print str(list_no) + 'Index and Value' + str(location_list[list_no])
	else:
		#create the coverage file per genome
		val = 0
		location_start = 1
		location_end = 1
		radii = list()
		left_windows = list()
		right_windows = list()
		for list_no in range(location_start , location_max):
			val += int(location_list[list_no])
			location_end += 1
			if list_no % window_size == 0:
				left_windows.append(int(location_start))
				right_windows.append(int(location_end-1))
				radii.append(float(val / float(window_size)))
				#sys.stdout.write("%s\t%d\t%d\t%f\n" % (header, location_start, location_end-1, val / float(window_size)))
				location_start = location_end
				val = 0
		
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
		if figure_letter != '':
			ax.text(-.1, 1, '%s)' % figure_letter, horizontalalignment='left', verticalalignment='bottom', fontdict=font, transform=ax.transAxes)

		plt.savefig("CoveragePlots/%s.png" % header)
		#plt.savefig(os.path.abspath(output_file))
		plt.close()
		
		#-----------------------------------------------------------------------------
		#-----------------------------------------------------------------------------
		#move to next genome
		LineNo = 1
		location_list = [0] * (location_end+1) #each genome has a seperate list
		previous_genome = current_genome
		# as we already read one line so we repeat the code below to not lose it
		if (location_start+ int(len(str(splits[10].strip()))) -1) < location_max:
			for list_no in range(location_start , location_start+int(len(str(splits[10].strip())))):
				location_list[list_no] = location_list[list_no] + 1	
	LineNo = LineNo + 1	
infile.close()
#ReadIDfile.close()