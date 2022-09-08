

import os
import time
import numpy as np
from subprocess import Popen
from read_files import read_files, read_data
#from EnKFfield_UVic import EnKFhome
from EnKFcluster_UVic import EnKFhome
from write_files import write_files
from write_kalman import write_kalman
import cProfile
import re


              #Number of ensemble members



lvar0=[] 
lvar1=[]          #list of variables used in the Kalman Filter (1st sublist is for atmosheric components, 2nd sublist is for oceanic components)

lvar1.append('temp1')
lvar1.append('temp2')
lvar1.append('salt1')
lvar1.append('salt2')
lvar1.append('dic1')
lvar1.append('dic2')
lvar1.append('dic131')
lvar1.append('dic132')
lvar1.append('c141')
lvar1.append('c142')
#lvar1.append('alk1')
#lvar1.append('alk2')
#lvar1.append('o21')
#lvar1.append('o22')
#lvar1.append('po41')
#lvar1.append('po42')
#lvar1.append('phyt1')
#lvar1.append('phyt2')
#lvar1.append('zoop1')
#lvar1.append('zoop2')
#lvar1.append('detr1')
#lvar1.append('detr2')
#lvar1.append('cocc1')
#lvar1.append('cocc2')
#lvar1.append('caco31')
#lvar1.append('caco32')
#lvar1.append('dop1')
#lvar1.append('dop2')
#lvar1.append('no31')
#lvar1.append('no32')
#lvar1.append('don1')
#lvar1.append('don2')
#lvar1.append('diaz1')
#lvar1.append('diaz2')
#lvar1.append('din151')
#lvar1.append('din152')
#lvar1.append('don151')
#lvar1.append('don152')
#lvar1.append('phytn151')
#lvar1.append('phytn152')
#lvar1.append('coccn151')
#lvar1.append('coccn152')
#lvar1.append('zoopn151')
#lvar1.append('zoopn152')
#lvar1.append('detrn151')
#lvar1.append('detrn152')
#lvar1.append('diazn151')
#lvar1.append('diazn152')
#lvar1.append('dfe1')
#lvar1.append('dfe2')
#lvar1.append('detrfe1')
#lvar1.append('detrfe2')
#lvar1.append('phytc131')
#lvar1.append('phytc132')
#lvar1.append('coccc131')
#lvar1.append('coccc132')
#lvar1.append('caco3c131')
#lvar1.append('caco3c132')
#lvar1.append('zoopc131')
#lvar1.append('zoopc132')
#lvar1.append('detrc131')
#lvar1.append('detrc132')
#lvar1.append('doc131')
#lvar1.append('doc132')
#lvar1.append('diazc131')
#lvar1.append('diazc132')
#lvar1.append('u1')
#lvar1.append('u2')
#lvar1.append('v1')
#lvar1.append('v2')




def run(n,Q,R,startyear,runtime,runstep,lvar0,lvar1,dirpath,ensname,datadir):
	step=0
	for i in range(startyear,startyear+runtime,runstep):
		step+=1
		yr=str(i)
		print('Start read files')
		x=read_files(n,lvar0,lvar1,dirpath,ensname)
		print('Start read data')
		y=read_data(yr,lvar0,lvar1,dirpath,datadir)
		print('Start EnKF')
		xnew,Pnew,k=EnKFhome(x,y,Q,R,n,lvar0,lvar1)
		print('Start write Kalman')
		write_kalman(k,n,lvar0,lvar1,dirpath,ensname)
		print('Start write files')
		write_files(xnew,n,i,lvar0,lvar1,dirpath,ensname)
		print('step ' + str(step) +' done')
	return 'Done'


cProfile.run('run(50,0.25,0.25,44903,20,1,lvar0,lvar1,"../ens_50lgm20yr","ens_lgm20yr","data025_lgm20yr")', 'stats')
