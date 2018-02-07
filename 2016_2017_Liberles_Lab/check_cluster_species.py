#!/usr/bin/python
##Check how many species are in each cluster
import re
clusters = open("saccharromycetales_40_90")
fastas = open("saccharromycetales.fasta")
cluster_list = []
all_fastas = fastas.readlines()

for i in clusters:
	cluster_list.append(i)
	
for cluster in cluster_list:
	cluster = cluster.split(" ")
	for code in cluster:
		for line in all_fastas:
			if re.search(code, line):
				#print line
				print line
				strin = str(line)
				#print strin
				print (re.search(r'^OS.*\GN$',line))
				#if hit:
				#	k = hit.group()
				#	print k

#print smallcluster 
#for i in range(
#print smallcluster[6]



clusters.close()
fastas.close()
