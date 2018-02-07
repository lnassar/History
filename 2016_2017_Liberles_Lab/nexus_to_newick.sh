#!/bin/bash
#Convert Nexus format trees to Newick format

for i in *_for_mb_good
	do cd ${i}
	for j in *mafft_bayes
		do cd ${j}
			if [ -a ${j/.mafft_bayes/.mafft.nex.con.tre} ]
				then
					#nexus_to_newick.py ${j/.mafft_bayes/.mafft.nex.con.tre}
					#nexus_to_newick_convert.py ${j/.mafft_bayes/.mafft.nex.con.tre}
					tree_format_converter.py ${j/.mafft_bayes/.mafft.nex.con.tre} ${j/.mafft_bayes/.mafft.aln.tre}
			fi
			cd ../
			done
		cd ../
	done
