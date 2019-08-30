#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 21:45:37 2018

@author: danielbean
"""

#preprocess MRREL

import csv, os, sys

processed_cui = 'MRCONSO.processed.csv'

if sys.argv[1] == 'full':
    path = "/mnt/datastore/umls/2017AB/META/"
    umls_file = "MRREL.RRF"
    
else:
    #test
    path = "."
    umls_file = "MRREL_TEST.RRF"

#load definition 
with open("MRREL_definition.csv", 'rb') as f:
	reader = csv.reader(f)
	next(reader, None)
	definition = []
	for line in reader:
		definition.append(line[0])
        
#load processed CUI
print "load known concepts"
exists = set()
with open(os.path.join(path, processed_cui)) as f:
    reader = csv.reader(f)
    next(reader, None)
    for line in reader:
        exists.add(line[0])

print "process relationships"
out = open(os.path.join(path, 'MRREL.processed.csv'), 'w')
writer = csv.writer(out)
cols = [':START_ID', ':END_ID', ':TYPE']
writer.writerow(cols)
count = 0
done = set()
with open(os.path.join(path, umls_file)) as f:
    for line in f:
        parts = dict(zip(definition, line.split("|")))
        if parts['CUI1'] in exists and parts['CUI2'] in exists:
            #cui2 is the source
            row = [parts['CUI2'], parts['CUI1'], parts['REL']]
            writer.writerow(row)
            if parts['RELA'] != '':
                row = [parts['CUI2'], parts['CUI1'], parts['RELA']]
                writer.writerow(row)
out.close()