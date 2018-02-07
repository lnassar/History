##Ex 3
#Read the tabular blast output files (you should have 6 total) into R. Use your
#knowledge of R to produce a data frame of reciprocal best blast hits for each species
#pair (3 total). Each RBBH data frame should have two columns, corresponding to
#sequence IDs for the two species. Here is one possible strategy:

#Make all the column names for the file
columns = c('qseqid', 'qlen', 'sseqid', 'slen', 'pident', 'nident', 'mismatch', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore')

#Read in all the files
garVSpuff <- read.table('garVSpuff.out.tsv', sep='\t', col.names = columns)
garVSstickle <- read.table('garVSstickle.out.tsv', sep='\t', col.names = columns)
pufferVSgar <- read.table('pufferVSgar.out.tsv', sep='\t', col.names = columns)
pufferVSstickle <- read.table('pufferVSstickle.out.tsv', sep='\t', col.names = columns)
stickleVSgar <- read.table('stickleVSgar.out.tsv', sep='\t', col.names = columns)
stickleVSpuffer <- read.table('stickleVSpuffer.out.tsv', sep='\t', col.names = columns)

#Add a new column which will depend on reverse/forward so they match RBHs
garVSpuff$garVpuffF <- ""
garVSstickle$garVstickF <- ""
pufferVSgar$puffVgarR <- ""
pufferVSstickle$puffVstickF <- ""
stickleVSgar$stickVgarR <- ""
stickleVSpuffer$stickVpuffR <- ""

#First adds the seqid and the qid in forward or reverse fashion
#Pastes the 2 ID's and adds them to the final column
garVSpuff$garVpuffF <- paste(garVSpuff$sseqid,garVSpuff$qseqid, sep = " ")
pufferVSgar$puffVgarR <- paste(pufferVSgar$qseqid,pufferVSgar$sseqid, sep = " ")

garVSstickle$garVstickF <- paste(garVSstickle$sseqid,garVSstickle$qseqid, sep = " ")
stickleVSgar$stickVgarR <- paste(stickleVSgar$qseqid,stickleVSgar$sseqid, sep = " ")

pufferVSstickle$puffVstickF <- paste(pufferVSstickle$sseqid,pufferVSstickle$qseqid, sep = " ")
stickleVSpuffer$stickVpuffR <- paste(stickleVSpuffer$qseqid,stickleVSpuffer$sseqid, sep = " ")

#Merges two of the databases depending on how many RBH hits match
garVpuffRBH <-merge(x=garVSpuff, y=pufferVSgar, by.x="garVpuffF", by.y="puffVgarR")[]
garVstickleRBH <-merge(x=garVSstickle, y=stickleVSgar, by.x="garVstickF", by.y="stickVgarR")[]
puffVstickleRBH <-merge(x=pufferVSstickle, y=stickleVSpuffer, by.x="puffVstickF", by.y="stickVpuffR")[]

#6. How many rows (RBBH orthologs) are there for each species pair? Using head(),
#print the first 5 rows of each of your 3 RBBH data frames and include this
#information with what you turn in. (6 points)

#garVpuffRBH = 12291
#garVstickleRBH = 13094
#puffVstickleRBH = 14623

#Getting the head value first five lines, only the first few entries are pasted here due to size
head(garVpuffRBH, n=5L)
#1 ENSTNIP00000000002.1 ENSLOCP00000002391.1 ENSLOCP00000002391.1    476 ENSTNIP00000000002.1
#2 ENSTNIP00000000005.1 ENSLOCP00000014083.1 ENSLOCP00000014083.1    272 ENSTNIP00000000005.1
#3 ENSTNIP00000000007.1 ENSLOCP00000011217.1 ENSLOCP00000011217.1   1048 ENSTNIP00000000007.1
#4 ENSTNIP00000000008.1 ENSLOCP00000020023.1 ENSLOCP00000020023.1    106 ENSTNIP00000000008.1
#5 ENSTNIP00000000010.1 ENSLOCP00000020484.1 ENSLOCP00000020484.1    232 ENSTNIP00000000010.1

head(garVstickleRBH, n=5L)
#1 ENSGACP00000000006.1 ENSLOCP00000009376.1 ENSLOCP00000009376.1    593 ENSGACP00000000006.1
#2 ENSGACP00000000010.1 ENSLOCP00000009427.1 ENSLOCP00000009427.1    245 ENSGACP00000000010.1
#3 ENSGACP00000000014.1 ENSLOCP00000007780.1 ENSLOCP00000007780.1    125 ENSGACP00000000014.1
#4 ENSGACP00000000015.1 ENSLOCP00000007789.1 ENSLOCP00000007789.1    109 ENSGACP00000000015.1
#5 ENSGACP00000000016.1 ENSLOCP00000016629.1 ENSLOCP00000016629.1    724 ENSGACP00000000016.1

head(puffVstickleRBH, n=5L)
#1 ENSGACP00000000006.1 ENSTNIP00000005398.1 ENSTNIP00000005398.1    356 ENSGACP00000000006.1
#2 ENSGACP00000000008.1 ENSTNIP00000009336.1 ENSTNIP00000009336.1    436 ENSGACP00000000008.1
#3 ENSGACP00000000011.1 ENSTNIP00000005401.1 ENSTNIP00000005401.1    251 ENSGACP00000000011.1
#4 ENSGACP00000000014.1 ENSTNIP00000005402.1 ENSTNIP00000005402.1    127 ENSGACP00000000014.1
#5 ENSGACP00000000015.1 ENSTNIP00000005403.1 ENSTNIP00000005403.1     96 ENSGACP00000000015.1

#7. Briefly explain why you think the number of gar-puffer, gar-stickleback, and pufferstickleback
#orthologs are/are not different. (4 points)

#The first thing to note is that they are both fairly close to each other, only about ~1000 genes appart.
#You would think that it discerns the species relationships, puffVstickle being the most closely related,
#followed by stickle V gar, and the least related combo of these fish are the puffVgar. So the stickle
#serves as a good intermediary to study relationships within the two.

#8. Plot the distributions of percent sequence identity for the stickleback-puffer and
#stickleback-gar RBBH orthologs side-by-side in a boxplot. Do the distributions
#appear to differ? Why might this be? (5 points)

#Make appropriate number of rows and distance the tick mark for the title to show alone
par(mgp=c(3, 1.5, 0))
par(mfrow=c(1,1))

#Assign a varialbe for the plot names and the colors
boxplot1names = c("PuffVStickleRBH","GarVStickleRBH")
boxplot1colors = c("red","blue")

#Create a boxplot of the puffVstickle and garVstickle percentage of identical matches
pdf("Homework3_Figures.pdf")
boxplot(puffVstickleRBH$pident.x, garVstickleRBH$pident.x, 
        ylab = "percentage of identical matches", 
        names = boxplot1names, col = boxplot1colors, main="PuffvStickle and GarvStickle Percent Identical Matches")
dev.off()

#Do the distributions appear to differ? Why might this be?

#They do appear to differ, PuffVStickle has a significantly higher percentage of matches
#as opposed to GarVstickle, which supports the previous statement that PuffVStickle are more closely related
#than GarVStickle

#9. Extract relevant information from the headers in the gar and stickleback
#pep.all.fa.gz files, and combine it with your gar-stickleback RBBH information to
#produce an orthology dot plot for gar chromosome 11.


#Made the preprocessing file in unix with:
#cat Lepisosteus_oculatus.LepOcu1.pep.all.fa | grep "^>" | grep "chromosome" | cut -f 1,3 -d " " | grep "chromosome" | cut -f 3 -d ":" > GarLG
#cat Lepisosteus_oculatus.LepOcu1.pep.all.fa | grep "^>" | grep "chromosome" | cut -f 1,3 -d " " | grep "chromosome" | cut -f 1 -d " " > GarGene

#cat Gasterosteus_aculeatus.BROADS1.pep.all.fa | grep "^>" | cut -f 1,3 -d " " | grep "group" | cut -f 1 -d " " > StickleGene
#cat Gasterosteus_aculeatus.BROADS1.pep.all.fa | grep "^>" | cut -f 1,3 -d " " | grep "group" | cut -f 3 -d ":" > StickleGroup

#Read in the two files into one data frame with protein ID and chromosome number
GarFastaGene <- read.table('GarGene', sep = "\n", col.names = "SeqID")
GarFastaLG <- read.table('GarLG', sep = "\n", col.names = "GarChromosome")
GarStartPos <- read.table('GarStartPos.txt', sep = "\n", col.names = "GarStartPos")
GarFasta <- cbind.data.frame(GarFastaGene, GarFastaLG, GarStartPos)

StickleFastaGene <- read.table("StickleGene", sep = "\n", col.names = "SeqID")
StickleFastaGroup <- read.table("StickleGroupFix", sep = "\n", col.names ="StickleChromosome")
StickleFasta <- cbind.data.frame(StickleFastaGene, StickleFastaGroup)

#Made two different data frames, one with the Chrome 11 from Gar then merged that with the group from stickle
garVstickleRBBH1 <-merge(x=garVstickleRBH, y=GarFasta, by.x="qseqid.x", by.y="SeqID")[]
garVstickleRBBH2 <-merge(x=garVstickleRBBH1, y=StickleFasta, by.x = "sseqid.x", by.y="SeqID")[]

#Make a plot of the gar start site of all proteins on chromosome 11 vs where they are on stickle
pdf("Figure2.pdf")
plot(garVstickleRBBH2$GarStartPos, garVstickleRBBH2$StickleChromosome,
     xlab = "Gar Protein Start Position", ylab = "Stickleback Chromosome Position",
     ylim = c(1,21), main = "Gar Chromosome 11 Protein Start Site vs. Sticklback Chromosome Paralog")
dev.off()
#10. How are the gar chromosome 11 genes distributed across the stickleback genome?
#Why is this expected/unexpected? (5 points)

#They seem to most all be evenly distributed between chromosome 10 and 20 on the stickleback genome.
#This is an expected result due to the species undergoing a genome duplication, so the 10th
#chromosome was duplicated and allowed to diverge, leading to Gar hits on both.