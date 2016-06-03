__author__ = 'AndrewPolyak'
__date__ = '12-29-2015'
__description__ = 'Interface for inheritance.py'

'''
TODO: make vcf compatible

'''

import sys
import csv
import inheritance

if len(sys.argv) != 4:
	print "Calls de novo and inherited SNVs from tabbed file"
	print "Reads family information from FAMILY file (<mother>\t<father>\t<child>)"
	print "Usage callinheritance.py [infile.txt] [familyfile.fam] [outfile.txt]"
	exit(1)

infile = sys.argv[1]
pedfile = sys.argv[2]
outfile = sys.argv[3]

writef = file(outfile, 'w')
writefile = csv.writer(writef, delimiter='\t')

denovoCT = 0
inheritedCT = 0
unknownCT = 0
maternalCT = 0
paternalCT = 0
bothinCT = 0

reader = csv.reader(open(infile, 'r'), delimiter='\t')
pedfilereader = csv.reader(open(pedfile, 'r'), delimiter='\t')
pedfilelist = list(pedfilereader)

for row in reader:
    outrow = row
    for pedrow in pedfilelist:
        mother = pedrow[0]
        father = pedrow[1]
        child = pedrow[2]

		print pedrow

        genotype_child = row[int(child)]
        genotype_mother = row[int(mother)]
        genotype_father = row[int(father)]

        if '.' not in genotype_child and '.' not in genotype_mother and '.' not in genotype_father:
            if '/' in genotype_child:
                call = inheritance.unphased(genotype_mother,genotype_father,genotype_child)
            if '|' in genotype_child:
                call = inheritance.phased(genotype_mother,genotype_father,genotype_child)
        else:
            call = 'U  '

        outrow.append(call)
    writefile.writerow(outrow)

    print "Done:", row[0], row[1], row[3], row[4]
