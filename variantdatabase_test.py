__author__ = 'AndrewPolyak'
__date__ = '12-30-2015'
__description__ = 'Interface for variantdatabase.py'

import csv
import sys
import hashlib
import sqlite3 as sql

if len(sys.argv) == 3:
    databasefile = sys.argv[1]
    variantfile = sys.argv[2]
else:
    print "Usage: variantdatabase_test.py [databasefile.db] [variantfile.txt]"
    exit(1)
    
conn = sql.connect(databasefile)
conn.text_factory = str
c = conn.cursor()
#c.execute("CREATE TABLE IF NOT EXISTS variants(chr TEXT, pos INTEGER, ref TEXT, alt TEXT, PRIMARY KEY (chr, pos, ref, alt))") 
c.execute("CREATE TABLE IF NOT EXISTS variants(varid TEXT PRIMARY KEY, chr TEXT, pos INTEGER, ref TEXT, alt TEXT)") 

infilereader = csv.reader(open(variantfile,'r'),delimiter='\t')
infilereader.next()
print "Adding variants to master database..."
for row in infilereader:
    varstring = row[0] + row[1] + row[3] + row[4]
    varhashobject = hashlib.md5(varstring.encode())
    varhashcode = varhashobject.hexdigest()
    c.execute("INSERT OR IGNORE INTO variants (varid, chr, pos, ref, alt) VALUES (?,?,?,?,?)", (varhashcode, row[0], row[1], row[3], row[4]))

#c.execute("SELECT * FROM variants")
#print c.fetchall()   
conn.commit()
print "Done!"