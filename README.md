# Fastq Reads Correction (FRC)
The entire program written in python 3.8.2. Sequencing errors can have a significant impact on downstream bioinformatics analysis, particularly genome assembly and polymorphism identification.  It is recommended that errors in input DNA sequences are reduced through trimming of low-quality bases or through an error correction step.  One of the simplest ways to correct sequencing errors is to rely on kmer frequency to first identify bases that could be erroneous and second identify the nucleotide the base should be.
A strategy to correct reads would look something like this;
1.	Count all of the kmers in the file of reads you want to correct.  This creates the data you’ll need to identify erroneous bases and to correct the base
2.	Process each read you want to correct one at a time
3.	For each base in a read, check to see if any kmers that include the current base have counts that meet some minimum threshold.  Assume that if any kmers with high counts can be generated using the current base then that base is NOT an error.
4.	Once you’ve determined if a base in a read is an error, you need to determine which nucleotide that base should be.  This can be done by substituting the erroneous base with the other nucleotides and seeing if any of the changes results in high count kmers.  If so, then use that base to correct the read.
5.	Print the corrected read to a file

# Requirements
* kmer count file – A file containing the output of the ‘jellyfish dump’ command on jellyfish database created from the file containing the reads to correct
* reads to correct – A file of Illumina reads that are to be corrected.  NOTE: Assume this file is in fastq format
* kmer size – The kmer sized used when producing the kmer database file
*	threshold – The minimum count a kmer must have to not be considered an error.

# Usage
```sh
python .\correct_reads.py -h
usage: correct_reads.py [-h] [-km ACCESSION] [-i FASTQ] [-k KMER] [-t THRESHOLD]    

optional arguments:
  -h, --help            show this help message and exit
  -km ACCESSION, --kmerCounts ACCESSION
                        A file containing the output of the ‘jellyfish dump’ command
  -i FASTQ, --input FASTQ
                        A file of Illumina reads that are to be corrected. NOTE: Assume this file is in fastq format
  -k KMER, --kmerSize KMER
                        The kmer sized used when producing the kmer database file
  -t THRESHOLD, --threshold THRESHOLD
                        The minimum count a kmer must have to not be considered an error
```

