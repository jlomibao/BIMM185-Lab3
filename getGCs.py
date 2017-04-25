#File Name: getGC.py
#Author: John Francis Lomibao
#PID: A11591509

import os.path
import sys

loc_seq_file = sys.argv[1]

gcCount = 0
geneAndGC = ['gene', 'gcContent']
max = -1
min = 2

#Open the 2 column file containing the gene locus and the sequence
with open(loc_seq_file, 'r') as f:
	#Put each line into an array called tableData
	tableData = [line.strip() for line in f]
for i in range(len(tableData)):
	#split each line into loctag and seq; store them
	data = tableData[i].split('\t')
	locTag = data[0]
	seq = data[1]

	#count the number of G's and C's
	for i in seq:
		if (i=='C' or i=='G') :
			gcCount += 1
			
	#calculate GC content from (GC count/length of sequence)
	gcContent = float(gcCount)/float(len(seq))
	gcCount = 0
	geneAndGC.append([locTag, gcContent])

#find max
for i in geneAndGC:
	if i[1] > max and isinstance(i[1], float):
		max = i[1]
		prMax = i

print 'Max GC: '+str(prMax)
		
#find min
for i in geneAndGC:
	if i[1] < min and isinstance(i[1], float):
		min = i[1]
		prMin = i

print 'Min GC: '+str(prMin)
	
