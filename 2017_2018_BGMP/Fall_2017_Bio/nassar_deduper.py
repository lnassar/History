
# coding: utf-8

# In[20]:

import re
import argparse
import sys

parser = argparse.ArgumentParser(description='Given a SAM file of uniquely mapped reads, removes all PCR duplicates as well as incorrect UMIs.')
parser.add_argument('-f', '--file', metavar='SAM File Path', required=True,type=str, help='Absolute file path to SAM file')
parser.add_argument('-p', '--paired', action='store_true', help='Optional: Designate if file is paired end or not')
parser.add_argument('-u', '--umi', metavar='UMI File Path', type=str, default=False, help='Optional: Designates absolute path to file containing list of UMIs')

parser = parser.parse_args()

if parser.paired:
    sys.exit("Paired end not implemented yet")

if parser.umi is False:
    sys.exit("Randomers feature not yet implemented")

#Read in files
#First we make read in our known UMI file and create a dictionary with all the UMIs as keys
#UMIs = open('STL96.txt') #This is for QA Testing
UMIs = open(parser.umi)

UMIs_Dic = {}

for umis in UMIs:
    umis = umis.rstrip()
    UMIs_Dic[umis] = []


#Read in our SAM file
#samfile = open('Dataset1.sam') #This is for QA testing
samfile = open(parser.file)

#Write our soft clipping fix function
def Fix_Position (StartPos, cigar):
    '''Checks to see if soft clipping occurs, and if so fixes the start position'''
    cigar = cigar.split('S')
    if re.search('[A-Z]', cigar[0]):
        pass
    else:
        StartPos = int(StartPos) - int(cigar[0])
    return StartPos

#Write function to combine both start position and chromosome
def Combine_Pos_Chrom (StartPos, Chrom):
    '''Combined the start position and chromosome number into a single string'''
    sep = 'chr'
    combo = [str(StartPos),str(Chrom)]
    return sep.join(combo)

#Make our new file, first making a new file name
newfilename = parser.file + "_deduped"
fh = open(newfilename, "a")

#Set a variable to count number of duplicates and wrong UMIs
duplicates = 0
wrongUMIs = 0


#Begin the script
for lines in samfile:
    #Skips the line if it's a header
    if lines.startswith('@'):
        fh.write(lines)
    else:
        #Split lines by tabs, then set your chromosome, start position, cigarstring and UMI
        entry = lines.split("\t")
        umi = entry[0].split(":")
        umi = umi[7]
        chrom = entry[2]
        cigar = entry[5]
        startpos = entry[3]
        startpos = Fix_Position(startpos,cigar)
        
        #Create a new variable combining both the chrosome and start position
        chrom_pos = Combine_Pos_Chrom(startpos,chrom)
        
        #Check to see if the UMI is in the known UMI dictionary then check to see if pos + chrom in that umi entry
        if umi in UMIs_Dic:
            #Check to see if the pos + chrom combination is already within that known UMI entry, if so it's a duplicate
            # if not, then add it in
            if chrom_pos in UMIs_Dic[umi]:
                duplicates +=1
            else:
                UMIs_Dic[umi].append(chrom_pos)
                fh.write(lines)
        else:
            wrongUMIs +=1
        
print("The total number of incorrect UMIs observed was ",wrongUMIs)
print("The total number of duplicates ommited was", duplicates)

fh.close
samfile.close()
UMIs.close()

