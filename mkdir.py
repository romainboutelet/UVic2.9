#! /home/romainboutelet/miniconda3/bin/python

import os 

for i in range(0,50):
	#os.system('cp -r ../testpi ../test_pi'+str(i))
	f=open('../ensbis_50fwfnb200yr/ens_fwfnb200yr'+str(i)+'/fwfnobio.q','w')
	f.write('#!/bin/bash\n')
	f.write('ulimit -s unlimited \n')
	f.write('cd /home/romainboutelet/models/UVic2.9/MOBI2.0/ensbis_50fwfnb200yr/ens_fwfnb200yr'+str(i)+'\n')
	f.write('time ./UVic_ESCM > pr')
	f.close()



