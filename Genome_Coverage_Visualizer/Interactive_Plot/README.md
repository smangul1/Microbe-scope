# Genome Coverage Visualizer for Metagenomics

## Online Demo:
For more information please visit http://mohammedalser.bilkent.edu.tr/MiCoP.html !
![alt text](https://github.com/smangul1/miCoP/blob/master/Genome_Coverage_Visualizer/Interactive_Plot/MiCoP_Demo.png)

## Running a test:
### Contigs concatenation + BWA-MEM + Read Clustering
```
module load python/3.6.1
module load bwa
module load samtools
sed -i -e 's/\r$//' MiCoP_GenomeCoverageVisualizer.sh
chmod +x MiCoP_GenomeCoverageVisualizer.sh
./MiCoP_GenomeCoverageVisualizer.sh [full directory to your reference] [full directory to your read set] [full directory of Scripts folder] [full directory to where you want to save the output?even if not exists] [window size] 2 1
```
### Read Clustering Only from .bam file
```
./MiCoP_GenomeCoverageVisualizer.sh [full directory to your reference] [full directory to your read set] [full directory of Scripts folder] [full directory to where you want to save the output?even if not exists] [window size] 2 3 [full directory to the .bam file (it should be in the same folder as it was generated from Step #2 above)]
```
