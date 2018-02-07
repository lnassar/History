#Import numpy and open file/also have a test file for QA
#for file 11_2H_both_S9_L008_R2_001.fastq.gz
import numpy as np
my_file=open("11_2H_both_S9_L008_R1_001.fastq")
#my_file=open("test_file.txt")

#Initialize a numpy array with 101 by 4,000,000 elements to hold all the quality scores in the file
whole_read = np.zeros((101,37061136))

#Our number of lines counter
NR = 0

#To convert phred scores to numbers
def convert_phred(letter):
    """Converts a single character into a phred score"""
    QScore = ord(letter) - 33
    return QScore

#Populate our array, we keep count with NR and divide by 4 to relate it to our numpy array
for lines in my_file:
    NR = NR + 1
    #if NR%500000==0:
    #    print (NR)
    if NR%4 == 0:
        for i in range((len(lines)-1)):
            Current_line = (int(NR/4))-1
            whole_read[i][Current_line] = convert_phred(lines[i])

#Print our statements
print("11_2H_both_S9_L008_R1_001.fastq")
print("# Base Pair","\t","Mean Quality Score","\t","Variance","\t","Standard Deviation","\t","Median")
for i in range(101):
    print(i,"\t\t",np.mean(whole_read[i,:]),"\t",np.var(whole_read[i,:]),"\t",np.std(whole_read[i,:]),"\t",np.median(whole_read[i,:]))

my_file.close()

my_file=open("11_2H_both_S9_L008_R2_001.fastq")
#my_file=open("test_file.txt")

#Initialize a numpy array with 101 by 4,000,000 elements to hold all the quality scores in the file
whole_read = np.zeros((101,37061136))

#Our number of lines counter
NR = 0

#To convert phred scores to numbers
def convert_phred(letter):
    """Converts a single character into a phred score"""
    QScore = ord(letter) - 33
    return QScore

#Populate our array, we keep count with NR and divide by 4 to relate it to our numpy array
for lines in my_file:
    NR = NR + 1
    #if NR%500000==0:
    #    print (NR)
    if NR%4 == 0:
        for i in range((len(lines)-1)):
            Current_line = (int(NR/4))-1
            whole_read[i][Current_line] = convert_phred(lines[i])

#Print our statements
print("11_2H_both_S9_L008_R2_001.fastq")
print("# Base Pair","\t","Mean Quality Score","\t","Variance","\t","Standard Deviation","\t","Median")
for i in range(101):
    print(i,"\t\t",np.mean(whole_read[i,:]),"\t",np.var(whole_read[i,:]),"\t",np.std(whole_read[i,:]),"\t",np.median(whole_read[i,:]))

my_file.close()