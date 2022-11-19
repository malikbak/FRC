import argparse
import subprocess
import os
# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument

parser.add_argument("-km", "--kmerCounts", dest="accession", help = "A file containing the output of the ‘jellyfish dump’ command")
parser.add_argument("-i", "--input", dest="fastq", help ="A file of Illumina reads that are to be corrected.  NOTE: Assume this file is in fastq format")
parser.add_argument("-k", "--kmerSize", dest="kmer", help = "The kmer sized used when producing the kmer database file")
parser.add_argument("-t", "--threshold", dest="threshold", help = "The minimum count a kmer must have to not be considered an error")

args = parser.parse_args()

import sys
fasta = {}
with open(args.accession) as file_one:
    for line in file_one:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            active_sequence_name = line[1:]
            if active_sequence_name not in fasta:
                fasta[active_sequence_name] = []
            continue
        sequence = line
        fasta[active_sequence_name].append(sequence)

#print (fasta.keys())
my_list = fasta[args.threshold]
#print(my_list)
import re
my_list2 = [i for i in my_list if re.findall(r"AA$", i)]
#print(my_list2)

################### Kmer read correction program #################
from datetime import datetime

start = datetime.now()

with open(args.fastq) as f:
    contents = f.read()
    #print(contents)

lines = [line.strip() for line in contents.split('\n') if line != '']

endfile = datetime.now()

countFromKmer = {}
topcount = 10
tes = []
k = int(args.kmer)
linesProcessed = 0
for line in lines[1::4]:
    #print(line)
    tes.append(line)
    startIdx = 0
    while startIdx + k <= len(line):
        kmer = line[startIdx:(startIdx+k)]
        countFromKmer[kmer] = countFromKmer.get(kmer, 0) + 1
        startIdx += 1
        #print(countFromKmer)
    linesProcessed += 1

endhist = datetime.now()    
            
kmerCounts = list(countFromKmer.items())
kmerCounts.sort(reverse = True, key = lambda kmerCount: kmerCount[1])

if len(kmerCounts) < topcount:
    raise Exception('fewer kmers than topcount')

end = datetime.now()
uniqueKmers = len(countFromKmer.keys())
totalKmers = sum(countFromKmer.values())
#print(uniqueKmers)
#print(kmerCounts)
lower = []
for i in kmerCounts:
    if i[1] <= int(args.threshold):
        lower.append(i)
corrected = []
for i in kmerCounts:
    if i[1] <= 1:
        corrected.append(i[0])

joi = '\n'.join(tes)
#print(corrected[1][1])
error_base = []
for i in range(0,len(lines[1::4])):
    for char in lines[1::4][i]:
        k = char.islower()
        if k == True:
            error_base.append(joi.index(char))

#print(error_base)
if joi[error_base[0]] == 'c':
    joi = joi.replace(joi[joi.index(char)], 'G')

for i in error_base:
    joi = joi.replace(joi[i], joi[i - len(tes[1])-1])
    lines[1::4] = list(joi.split('\n'))

with open('error_free.fastq', 'w') as f:
    f.write('\n'.join(lines))
    