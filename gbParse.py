#File Name: gbParse.py
#Author: John Francis Lomibao
#PID: A11591509

import os.path
import sys
import gzip
import re

#open gzip file and set it to variable g
gbff = sys.argv[1]
g = gzip.open(gbff, 'rb')

#variables we want to store
taxID     = '' #source, db_xref
accession = '' #cds, protein_id
coords    = '' #cds, CDS line
strand    = '' #cds, CDS line, rev if complement in line, else fwd
geneName  = '' #cds, gene
locTag    = '' #cds, locus_tag
synonyms  = '' #cds, gene_synonym
protName  = '' #cds, product
ECnums    = [] #cds, EC_number (can have none, or multiple)
extRefs   = [] #cds, db_xref (has multiple)

'''
Lines were being printed twice, and breaking at the end of the first loop
failed to stop lines from being printed twice
LastTag is a variable used to record the locus tag read previously
locTag, the current locus tag is checked against lastTag to see if the line had already been printed
'''
lastTag = ''

#Using Biopython
from Bio import SeqIO
#parse through the genbank file with SeqIO
for rec in SeqIO.parse(g, "genbank"):
	#broke down file by feature using capabilities of Biopython
	for feature in rec.features:
		#check in "source" and "CDS" for the information we want to output to a table
		if feature.type == "source":
			taxID = feature.qualifiers['db_xref'][0]
		if feature.type == "CDS":
		
			#try/except used to continue program even if there is an error obtaining the info we want
			try:
				#broke it down further by accessing the qualifier
				locTag = feature.qualifiers["locus_tag"][0]
				
				#regex to find coordinate part of string and set coords to that value
				m1 = re.search(r"(([0-9]+:)\w+)", str(feature.location))
				coords = m1.group(1)
				
				#regex to find whether the strand is fwd or rev, and set that strand to that value
				m2 = re.search(r"([\-\+()]+)", str(feature.location))
				strand = m2.group(1)
				
				accession = feature.qualifiers["protein_id"][0]
				geneName  = feature.qualifiers["gene"][0]
				synonyms  = feature.qualifiers["gene_synonym"][0]
				protName  = feature.qualifiers["product"][0]
				
				#put all external references into the array extRef
				try:
					index = 0
					length = len(feature.qualifiers["db_xref"])
					while (index < length):
						extRefs.append(feature.qualifiers["db_xref"][index])
						index += 1
				except:
					continue
		
				#put all EC numbers into the array ECnums
				try:
					index = 0
					length = len(feature.qualifiers["EC_number"])
					while (index < length):
						ECnums.append(feature.qualifiers["EC_number"][index])
						index += 1
				except:
					continue		
			except:
				continue
		#This if statement is used to prevent double printing
		if locTag.strip() != '' and lastTag != locTag:
			lastTag = locTag
			
			#print out tab separated data
			sys.stdout.write(taxID+'\t'+accession+'\t'+coords+'\t'+strand+'\t'+
							 geneName+'\t'+locTag+'\t'+synonyms+'\t'+protName+'\t'+
							 str(ECnums)+'\t'+str(extRefs))
			print ""
			
			#empty arrays for next batch
			ECnums  = []
			extRefs = []
			'''
			try:
				for i in range(len(ECnums)-1):
					sys.stdout.write(str(ECnums[i])+',')
				sys.stdout.write(ECnums[-1]+'\t')
			except:
				sys.stdout.write('None'+'\t')
			try:
				for i in range(len(extRefs)-1):
					sys.stdout.write(str(extRefs[i])+',')
				sys.stdout.write(extRefs[-1])
			except:
				sys.stdout.write('None')
			'''
				