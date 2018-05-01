#!/usr/bin/python

#This is a prototype variant annotation tool by Luis Nassar designed to provide a specified output given a VCF file input.
#The script is divided into 5 sections:
#1. LIBRARIES: Libraries required to run program.
#2. ARGPARSE: The argparse section which gives a command line functionality
#3. OPEN FILES AND CREATE FIRST DESCRIPTIVE LINES: Opens VCF files and creates new file. Also provides a description of all the output format columns.
#4. FUNCTIONS: All the functions used in the script.
#5. MAIN LOOP: The file loop that parses through the VCF file and extracts/computes/queries the required information

#####################################################################################
#1. LIBRARIES
import urllib.request, json, re, argparse

#####################################################################################
#2. ARGPARSE

#Set our argparse arguments, first the program description, followed by the input file name, and an optional desirded output file name
parser = argparse.ArgumentParser(description='Variant Annotation Tool. Given a VCF file as input, extracts Chrom, Pos, Ref, Alt, Qual and Depth values for each entry. Additionally computes the percentage of reads supporting variant vs. reference (AOPvsROP), and queries the ExAC database for variant consequence and allele frequency. Result is a tab delimeted file.')
parser.add_argument('-f', '--file', metavar='VCF File Path', required=True,type=str, help='Absolute file path to VCF file')
parser.add_argument('-o', '--output', metavar='Output File Name', type=str, default=False, help='Optional: Designate output file name.')

parser = parser.parse_args()

#Check to see if an option desired name was chosen, if so use it. Otherwise create a new extension to the original file name
if parser.output is False: #Add our conditional to check if a custom name was passed
    FileName = str(parser.file+".annotation.output.tsv")
else:
    FileName = parser.output

#####################################################################################
#3. OPEN FILES AND CREATE FIRST DESCRIPTIVE LINES

#Open VCF file as well as new annotation file
VCFfile = open(parser.file)
Output = open(FileName, 'w')

#Write out the column descriptions
Output.write("CHROM: Chromosome"+"\n"+"POS: Position"+"\n"+"REF: Reference base(s)"+"\n"+"ALT: Alternative base(s)"+"\n"+"QUAL: Quality"+"\n"+"DP: Depth of sequence coverage"+"\n"+"AO: Number of reads supporting variant"+"\n"+"AOPvsROP:Percentage of reads supporting the variant versus those supporting reference reads"+"\n"+"ALLFREQ: Allele Frequency from ExAC"+"\n"+"CONSEQ: Variant consequence from ExAC"+"\n")

#Write out the column header tabs                   
Output.write("CHROM"+"\t"+"POS"+"\t"+"REF"+"\t"+"ALT"+"\t"+"QUAL"+"\t"+"DP"+"\t"+"AO"+"\t"+"AOPvsROP"+"\t"+"ALLFREQ"+"\t"+"CONSEQ"+"\n")                   

######################################################################################
#4. FUNCTIONS

#Function which exctracts the sequence coverage of current variant from INFO column
def extract_coverage_depth(entry):
    #First the 8th column(INFO) is selected, and subsequently the value of the 8th entry (depth) is also extracted
    Cov_Dep = entry[7].split(';')
    Cov_Dep = Cov_Dep[7].split('=')
    Cov_Dep = Cov_Dep[1]
    return(Cov_Dep)

#Similar to extract_coverage_depth function, simply extracts the number of reads supporting the variant
def extract_alternative_variant_reads(entry):
    Alt_Var = entry[7].split(';')
    Alt_Var = Alt_Var[5].split('=')
    Alt_Var = Alt_Var[1]
    return(Alt_Var)

#Similar to extract_coverage_depth function, simply extracts the number of reads supprting the reference
def extract_reference_reads(entry):
    Ref_Var = entry[7].split(';')
    Ref_Var = Ref_Var[28].split('=')
    Ref_Var = Ref_Var[1]
    return(Ref_Var)

#Takes as input the vcf entry split by tabs and sets the chromosome, position, reference variant, alternative variant and quality score to a variable
def extract_chrom_pos_ref_alt_qual(entry):
    chrom = entry[0]
    pos = entry[1]
    ref = entry[3]
    alt = entry[4]
    qual = entry[5]
    return(chrom, pos, ref, alt, qual)

######################################################################################
#5. MAIN LOOP

#Begin parsing file, remove newline characters with rstrip
for entry in VCFfile:
    entry = entry.rstrip()
    
    #First we check if the line is a header and if so write it out to our file, or pass for clarity
    if entry.startswith('#'):
        pass
        #Output.write(entry+"\n") #Optional to enable saving header lines
    
    #Commense parsing individual entrie by tab splitting lines and assigning values with the proper functions
    else:
        entry = entry.split('\t')
        chrom, pos, ref, alt, qual = extract_chrom_pos_ref_alt_qual(entry)
        DoC = extract_coverage_depth(entry)

        #Alternative variant requires us to remove decimals as some of them are partial reads (This is a biologically incorrect way to do it!)
        AO = float(extract_alternative_variant_reads(entry).replace(',', ''))
        
        RO = extract_reference_reads(entry)
        AOP = round(float(AO)/float(DoC),2) #Ratio of Alternative calls to total reads
        ROP = round(float(RO)/float(DoC),2) #Ratio of Reference calls to total reads
        AOPvsROP = str(AOP)+":"+str(ROP) #Join the two percentages to make a ratio

        #Write out our data in a tab delimeted fashion
        Output.write(chrom+"\t"+pos+"\t"+ref+"\t"+alt+"\t"+qual+"\t"+DoC+"\t"+str(AO)+"\t"+AOPvsROP+"\t")

        #Maintain print statements for quality control
#         print("AO is ", str(AO))
#         print("Depth of Coverage is",DoC)
#         print("AO is ", AO)
#         print("Percentage of reads supporting variant vs. reference is ", str(AOP) + ":" + str(ROP))
        
        #Query the ExAC database for the variant allele frequency, if none found return No Data
        with urllib.request.urlopen(str("http://exac.hms.harvard.edu/rest/variant/variant/"+ entry[0]+ "-"+ entry[1]+ "-" +entry[3]+ "-"+ entry[4])) as url:
            data = json.loads(url.read()) #Read JSON format
            
            #Check to see if allele frequency information was pulled from ExAC, if so then save it. Otherwise indicate no data.
            if 'allele_freq' in data:
                Output.write(str(round(data['allele_freq'],3))+"\t")
                
#                 print(round(data['allele_freq'],3)) #Retain for quality control

                #Treat the ExAC entry as a string and use regex to find the consequence. Then use splitting to pull exact consequence.
                consequence = re.search('Consequence(.*)', str(data))
                if consequence:
                    consequence = consequence.group(1)
                    consequence = consequence.split("'")
                    Output.write(str(consequence[2])+"\n")
					
#		print(consequence[2]) #Retain for quality control
            
            else:
                #If ExAC database had no info on our variant, then allele frequency and consequence are "No Data"
                Output.write("No Data"+"\t"+"No Data"+"\n")

#                 print("No Data") #Retain for quality control
                   
#Close out our files
VCFfile.close()                
Output.close()
