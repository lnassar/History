#!/usr/bin/python
import re

##Check two clusters against each other for differences
check_yes = 0
check_no = 0
with open("alveolata_plus_human_anopheles_aedes_40_90",'r') as inp:
	file_as_list=[line.rstrip("\r\n") for line in inp]
	
with open("alveolata_40_90",'r') as inp:
	file_as_list_alv=[line.rstrip("\r\n") for line in inp]
	
for i in file_as_list_alv:
#	print i
	if i in file_as_list:
		#print "YES!"
		check_yes = check_yes + 1
	else:
		print "NO!"
		check_no = check_no + 1
		print i
		
print "Amount of yes = " + str(check_yes)
print "Amount of no = " + str(check_no)
