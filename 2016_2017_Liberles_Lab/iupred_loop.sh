#!/bin/bash
#Runs iupred on all relevant subdirectories

for i in *_for_mb_good
	do cd ${i}
	for j in *mafft_bayes
		do cd ${j}
			if [ -a ${j/.mafft_bayes/.mafft.fas} ]
				then
					run_iupred_on_msa.py ${j/.mafft_bayes/.mafft.fas} -pti ~/bin/iupred/
			fi
			cd ../
			done
		cd ../
	done
