__author__ = 'AndrewPolyak'
__date__ = '12-30-2015'

import sys
import vcf
import csv
import sqlite3 as sql

#conn = sql.connect('16p12_database.db') 
#conn.text_factory = str

#c = conn.cursor()
#c.execute("CREATE TABLE IF NOT EXISTS variants(varid primary key autoincrement, chr TEXT, pos INTEGER, ref TEXT, alt TEXT)")

#vcfreader = vcf.Reader(open('vcffile.vcf','r'))
    
def load(database):
    conn = sql.connect(database)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS variants(chr TEXT, pos INTEGER, ref TEXT, alt TEXT, INTEGER PRIMARY KEY (chr, pos, ref, alt))")
    return c
    
def addAnnotation(annotationfile, database):
    load(database)
    c.execute("ALTER TABLE variants ADD COLUMN 'annotationfile' IF NOT EXISTS")
    annotationfilereader = csv.reader(open(annotationfile,'r'))
    for row in annotationfilereader:
        c.execute("UPDATE variants SET 'annotationfile'=row[4] WHERE chr=row[0] pos=row[1] ref=row[2] alt=row[3]")
        
def addVariant(inchr, inpos, inref, inalt, variants):
    c.execute("INSERT INTO variants(chr, pos, ref, alt) IF NOT EXISTS (inchr, inpos, inref, inalt)")
    
def addVariantsFromVCF(vcffile, variants):
    vcfreader = vcf.Reader(open(vcffile,'r'))
    for record in vcfreader:
        c.execute("INSERT OR IGNORE INTO variants(chr, pos, ref, alt) VALUES(record.CHR, record.POS, record.REF, record.ALT)")
            
def addVariantsFromAnnovar(infile, database):
    c = load(database)
    print c
    infilereader = csv.reader(open(infile,'r'),delimiter='\t')
    infilereader.next()
    print "Working..."
    for row in infilereader:
        c.execute("INSERT INTO variants (chr, pos, ref, alt) VALUES (?,?,?,?)", (row[0], row[1], row[3], row[4]))
        #print row[0], row[1], row[3], row[4], "...Added"
        
def getFromTable(database, table):
    c = load(database)
    c.execute("SELECT * FROM variants")
    return c.fetchall()