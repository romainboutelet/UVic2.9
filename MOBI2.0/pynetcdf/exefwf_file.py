#! /home/romainboutelet/miniconda3/bin/python

#Run the Ensemble Kalman Filter on the UVic 2.9 model. 

#This needs the creation of n (the number of ensemble members) directories each containing the UVic2.9 model that need to be run. The creation of these directories can be done by the 'mkdir.py' file from a directory containing the UVic2.9 model adjusted with the right conditions and parameters. 

#The main function is exe(n,startyear,endyear,runstep,lvar0,lvar1,dirpath,ensname,datadir,execname) where : 
# - n is the number of ensemble members for the EnKF
# - runstep indicates the time interval (in yr) between each call to the EnKF
# - lvar0 and lvar1 specify which variables will be used for the EnKF
# - dirpath is the path to the directory where the n ensemble members directories are stored
# - ens_name is the name given to the ensemble members directories (the directories has to be named as 'ens_name0 ,ens_name1,  ... , ens_name'n')
# - datadir specifies the directory in which the data can be found. The files containing the data should be formatted the same way as the restart files and named such as to be found at : dirpath + "/" + datadir + "/rest."+ yr +".01.01.nc" , (yr being such as yr = startyear + k*runstep, k=1,...,nbstep). The data can be incorporated in an other way but then the line of the write_data function should be masked and the data need to be an array of shape (n, len(lvar0)*102*102+len(lvar1)*19*102*102) where the order of the appended variables follow the order in the restart.nc file.
# - execname is the name of the executable that needs to be run with 'qsub' (use the same execname for all the ensemble member directories)




import os
import time
import numpy as np
from subprocess import Popen
from read_files import read_files, read_data
#from EnKFno_UVic import EnKFhome
#from EnKFfield_UVic import EnKFhome
#from EnKFcluster_UVic import EnKFhome
from EnKF_fwf import EnKFfwf
from write_files import write_files
from write_kalman import write_kalman
from fwf_change import fwf_change
from fwf_file import fwf_file
from run_done import run_done
from write_control import write_control
from fwf_merge import fwf_merge
from d13C import d13C, d13Cobs
from fwf_kalman import fwf_kalman
from merge_stats import merge_stats
from string_yr import string_yr

              #Number of ensemble members



lvar0=[] 
lvar1=[]          #list of variables used in the Kalman Filter (1st sublist is for atmosheric components, 2nd sublist is for oceanic components)

lvar0.append('slat')

lvar1.append('temp1')
#lvar1.append('temp2')
#lvar1.append('salt1')
#lvar1.append('salt2')
lvar1.append('dic')
#lvar1.append('dic2')
lvar1.append('dic13')
#lvar1.append('dic132')
#lvar1.append('c141')
#lvar1.append('c142')
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

n = 50
Q = 1
R = 5
fwf_init = 0.
startyear = 4000
runtime = 500
runstep = 50
tsiint = 30                   # in days
tavgper = 30                  # in days
tavgint = 50                  # in years
dirpath = '../ens_50fwfnb200yr'
ensname = 'ens_fwfnb200yr'
datadir = 'data_slopedrop'
execname = 'fwfnobio.q'
runname = 'fwf0.05kalpi500yr_r5_q1_tavgint50slopeslsigma2.5diff'
fwfobs = np.zeros(int(runtime//runstep))
initage = 19755
randamp = 0.05
slstart = -132.8
tavgfile = 'tavg.04050.01.01.nc'


def exe(n,Q,R,fwf_init,fwfobs,slstart,randamp,initage, startyear,runtime,runstep,tsiint,tavgint,tavgper,tavgfile,lvar0,lvar1,dirpath,ensname,datadir,execname,runname):
	output = 'pr_' + runname
	os.system('cp ' + dirpath + '/' + ensname + '0/data/restartb.nc ' + dirpath + '/' + ensname + '0/data/restart.nc')
	os.system('for i in {1..49}; do cp ' + dirpath + '/' + ensname + '0/data/restart.nc "' + dirpath + '/' + ensname + '$i/data";  done')
	os.system('rm ' + dirpath + '/' + ensname + '*/tsi.*')
	os.system('rm ' + dirpath + '/' + ensname + '*/tavg.*')
	os.system('rm ' + dirpath + '/' + ensname + '*/data/restartnew.nc')
	os.system('rm ' + dirpath + '/' + ensname + '*/random.dat')
	os.system('rm ' + dirpath + '/' + ensname + '*/tsi' + runname + '.nc') 
	os.system('rm ' + dirpath + '/' + ensname + '*/tavg' + runname + '.nc')
	os.system('rm ' + dirpath + '/' + ensname + '*/randamp.dat')
	os.system('rm ' + dirpath + '/kal_hist' + runname + '.npz')

	for i in range(n):
		np.savetxt(dirpath + '/' + ensname + str(i) + '/randamp.dat',np.array([randamp]),fmt = '%10.8f')

	write_control(n,dirpath,ensname,runstep,tsiint,tavgint,tavgper)
	
	f = open(output,'w')	
	#os.system('rm ' + dirpath + '/kalman.nc')
	step=0

	init_sealev = np.fromfunction(lambda i: np.random.normal(slstart+0*i,0.00001),(n,))
	for i in range(startyear,startyear+runtime,runstep):
		agerel = initage - (i - startyear)
		yr = string_yr(i)
		

		fwfinit,fwfrate = fwf_change(n,fwf_init,fwfobs,dirpath,ensname,runstep,step,init_sealev)

		if step > 0:
			fwfinitnew = EnKFfwf(Q,R,randamp,slstart,n,dirpath,ensname,datadir, runname,yr,agerel,runstep,step,tavgint,tavgfile)
			f.write('EnKF done\n')
			fwf_kalman(n,fwfinit,fwfinitnew,randamp,dirpath,step,runstep)
			fwfinit = fwfinitnew
		else:
			fwf_kalman(n,fwfinit,fwfinit,randamp,dirpath,step,runstep)

		
		fwf_file(n,fwfinit,fwfrate,dirpath,ensname,i,runstep)
		#write_files(xnew,n,i,lvar0,lvar1,dirpath,ensname)
		yr = string_yr((i + runstep)//runstep*runstep)
	
		f.write('Restart files for year'+yr+ 'rewritten\n')
		for j in range(n):
			jstr=str(j)
			os.system('qsub ' + dirpath + '/' + ensname + jstr+'/' + execname)
		step+=1
		print('Run '+str(step)+' launched')
		a,b,c,d=str(0),str(1),str(2),str(3)
		thres=0
		done=False
		time.sleep(120)
		while not done:
			done = True 
			for j in range(n):
				done = done and run_done(dirpath,ensname,j)
			time.sleep(1)
			thres+=1
			if thres >=1200*runstep:
				f.write('UVic2.9 model did not converge')
				return('UVic2.9 model did not converge')
		time.sleep(3)
		print('out of sleep')
		os.system('rm ' + execname + '.*')
	fwf_change(n,fwf_init,fwfobs,dirpath,ensname,runstep,step,init_sealev)
	os.system('for i in {0..' + str(n-1) + '}; do ncrcat -h "' + dirpath + '/' + ensname + '$i"/tsi.* "' + dirpath + '/' + ensname + '$i"/tsi' + runname + '.nc ; done') 
	os.system('for i in {0..' + str(n-1) + '}; do ncrcat -h "' + dirpath + '/' + ensname + '$i"/tavg.* "' + dirpath + '/' + ensname + '$i"/tavg' + runname + '.nc ; done') 
	fwf_merge(n,dirpath,ensname,runtime,runstep,runname,tsiint)
	os.system('nces ' + dirpath + '/' + ensname + '*/' + 'tsi' + runname + '.nc ' + dirpath + '/tsi' + runname + 'stat.nc')
	merge_stats(n,dirpath,ensname,runname)
	f.write('The Kalman Filter has done its work!\n')
	f.close()
	return ('The Kalman Filter has done its work!')

exe(n,Q,R,fwf_init,fwfobs,slstart,randamp,initage,startyear,runtime,runstep,tsiint,tavgint,tavgper,tavgfile,lvar0,lvar1,dirpath,ensname,datadir,execname,runname)
