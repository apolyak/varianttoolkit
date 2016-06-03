#! usr/bin/env python

import sys
import csv

if len(sys.argv) != 5:
    print "Determines if SNV is carried by individual"
    print "Usage: carries_snv.py [infile.txt] [start] [end] [outfile.txt]"
    exit(1)

infile = open(sys.argv[1], 'r')
start = int(sys.argv[2])
stop = int(sys.argv[3])
outfile = file(sys.argv[4], 'w')

infileReader = csv.reader(infile, delimiter='\t')
infileList = list(infileReader)
writefile = csv.writer(outfile, delimiter='\t')

for row in infileList:
    outrow = [row[0], row[1], row[2], row[3], row[4]]
    for i in range(start, stop):
        genotype = row[i]

        if '/' in genotype:
            genotype_split = genotype.split('/')
        elif '|' in genotype: 
            genotype_split = genotype.split('|')
        else:
            genotype_split = "PP"

        if genotype_split[0] == row[3] and genotype_split[1] == row[3]:
            out = 0
        else:
            out = 1
            
        if genotype_split == "PP":
            out = row[i]
            
        outrow.append(out)

    writefile.writerow(outrow)

    print outrow
        
print "Done!"