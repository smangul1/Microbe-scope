# Seed Generator

1. It takes a RefSeq file after removing all genome sequences that are shared with EuPathDB.  
2. Then the script (e.g., submit-SeedGenerator-archaea.sh) generates all seeds (or k-mers) that are of length 30 bp (the length is configurable in "NonoverlappingSeedGenerator.py").
3. The script also removes all redundant seeds and keep only one.
4. The output of the script will be in fastq format.

** There are faster and more effiecient ways (such as maintaining a trie structure, commented in "NonoverlappingSeedGenerator.py") of doing the same job of the script, if and only if we can address the memory and execution time limitations imposed by UCLA-Hoffman2.
