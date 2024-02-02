''' 
Script to parse the Huckleberry "csv" files and output a proper csv file so it can be read into pandas etc. 
Note: using csv.reader doesn't work because of the combo of quotes and curly brackets
'''

import glob

## Define the outfile to write to
outfile = 'Huckleberry_latest.csv'

## Find latest datafile, which have been named according to convention Huckleberry_data_YYYYMMDD.csv
hfiles = glob.glob('Huckleberry_data_*.csv')
hfiles.sort()
latestfile = hfiles[-1]

## Open the datafile and read in the data as a list of strings
with open(latestfile) as f:
	lines = f.readlines()

## Define the quotation mark and delimiter
quote = '"'
delim = ','

## Change all commas within quotations to semicolons, and remove the quotation marks
with open(outfile, 'w+') as f:
	for line in lines:
		n_quotes = 0
		a = list(line)
		for i in range(len(a)):
			if a[i] == quote:
				n_quotes += 1
			if a[i] == delim:
				if n_quotes % 2 == 1:
					a[i] = ';'
		line = ''.join(a)
		line = line.replace('"', '')
		f.write(line)
				

