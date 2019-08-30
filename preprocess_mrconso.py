#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 21:26:28 2018

@author: danielbean
"""

#preprocess MRCONSO

import csv, os, sys

processed_file = "MRCONSO.processed.csv"

if sys.argv[1] == 'full':
    path = "/mnt/datastore/umls/2017AB/META/"
    umls_file = "MRCONSO.RRF"
    
else:
    #test
    path = "."
    umls_file = "MRCONSO_TEST.RRF"

#load definition
with open("MRCONSO_definition.csv", 'rb') as f:
	reader = csv.reader(f)
	next(reader, None)
	definition = []
	for line in reader:
		definition.append(line[0])

out = open(os.path.join(path, processed_file), 'w')
writer = csv.writer(out)
cols = ['CUI:ID', 'name', ':LABEL']
writer.writerow(cols)
count = 0
done = set()
with open(os.path.join(path, umls_file)) as f:
    for line in f:
        parts = dict(zip(definition, line.split("|")))
        if parts['CUI'] in done:
            continue
        if parts['LAT'] == "ENG" and parts['TS'] == 'P':
            row = [parts['CUI'], parts['STR'], 'Concept']
            writer.writerow(row)
            done.add(parts['CUI'])
out.close()