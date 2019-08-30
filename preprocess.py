import csv, os

output_conso_file = "MRCONSO.processed.csv"
output_rel_file ="'MRREL.processed.csv"
output_path = "."

input_path = "/mnt/datastore/umls/2017AB/META/"
input_conso_file = "MRCONSO.RRF"
input_rel_file = "MRREL.RRF"


#load definition
with open("MRCONSO_definition.csv", 'rb') as f:
	reader = csv.reader(f)
	next(reader, None)
	conso_definition = []
	for line in reader:
		conso_definition.append(line[0])

with open("MRREL_definition.csv", 'rb') as f:
    reader = csv.reader(f)
    next(reader, None)
    rel_definition = []
    for line in reader:
        rel_definition.append(line[0])

out = open(os.path.join(output_path, output_conso_file), 'w')
writer = csv.writer(out)
cols = ['CUI:ID', 'name', ':LABEL']
writer.writerow(cols)
count = 0
exists = set()
with open(os.path.join(input_path, input_umls_file)) as f:
    for line in f:
        parts = dict(zip(conso_definition, line.split("|")))
        if parts['CUI'] in done:
            continue
        if parts['LAT'] == "ENG" and parts['TS'] == 'P':
            row = [parts['CUI'], parts['STR'], 'Concept']
            writer.writerow(row)
            exists.add(parts['CUI'])
out.close()

print "process relationships"
out = open(os.path.join(output_path, output_rel_file), 'w')
writer = csv.writer(out)
cols = [':START_ID', ':END_ID', ':TYPE']
writer.writerow(cols)
count = 0
done = set()
with open(os.path.join(input_path, input_rel_file)) as f:
    for line in f:
        parts = dict(zip(rel_definition, line.split("|")))
        if parts['CUI1'] in exists and parts['CUI2'] in exists:
            #cui2 is the source
            row = [parts['CUI2'], parts['CUI1'], parts['REL']]
            writer.writerow(row)
            if parts['RELA'] != '':
                row = [parts['CUI2'], parts['CUI1'], parts['RELA']]
                writer.writerow(row)
out.close()