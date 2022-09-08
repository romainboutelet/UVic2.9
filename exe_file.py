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
from EnKFfield_UVic import EnKFhome
#from EnKFcluster_UVic import EnKFhome
from write_files import write_files
from write_kalman import write_kalman
#from d13C import d13C
from run_done import run_done
from write_control import write_control
from merge_stats import merge_nofwf_stats


              #Number of ensemble members



lvar0=[] 
lvar1=[]          #list of variables used in the Kalman Filter (1st sublist is for atmosheric components, 2nd sublist is for oceanic components)

lvar1.append('temp1')
lvar1.append('temp2')
lvar1.append('salt1')
lvar1.append('salt2')
#lvar1.append('dic1')
#lvar1.append('dic2')
#lvar1.append('dic131')
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
Q = 0.5
R = 2.5
startyear = 44903
runtime = 20
runstep = 1
tsiint = 30
tavgint = 30
runname = '05r5tbiais05field_lgm20yr'
dirpath = '../ens_50lgm20yr'
ensname = 'ens_lgm20yr'
datadir = 'data05tbiais05_lgm20yr'
execname = 'c14.q' 

def exe(n,Q,R,startyear,runtime,runstep,tsiint,tavgint,lvar0,lvar1,dirpath,ensname,datadir,execname,runname):

	output = 'pr_' + runname
	os.system('cp ' + dirpath + '/' + ensname + '0/data/restartb.nc ' + dirpath + '/' + ensname + '0/data/restart.nc')
	os.system('for i in {1..49}; do cp ' + dirpath + '/' + ensname + '0/data/restart.nc "' + dirpath + '/' + ensname + '$i/data";  done')
	os.system('rm ' + dirpath + '/' + ensname + '*/tsi.*')
	os.system('rm ' + dirpath + '/' + ensname + '*/tavg.*')
	os.system('rm ' + dirpath + '/' + ensname + '*/data/restartnew.nc')
	os.system('rm ' + dirpath + '/' + ensname + '*/tsi' + runname + '.nc') 
	os.system('rm ' + dirpath + '/' + ensname + '*/tavg' + runname + '.nc') 	


	write_control(n,dirpath,ensname,runstep,tsiint,tavgint,runstep)
	
	f = open(output,'w')	
	os.system('rm ' + dirpath + '/kalman.nc')
	step=0
	for i in range(startyear,startyear+runtime,runstep):
		step+=1
		if i < 10:	
			yr = '0000' + str(i)
		elif i < 100:
			yr = '000' + str(i)
		elif i < 1000:
			yr = '00' + str(i)
		elif i < 10000:
			yr = '0' + str(i)
		else:
			yr=str(i)
		#d13c=d13C(n,dirpath,ensname)
		x=read_files(n,lvar0,lvar1,dirpath,ensname)
		y=read_data(yr,lvar0,lvar1,dirpath,datadir)

		xnew=EnKFhome(x,y,Q,R,n,lvar0,lvar1,dirpath,ensname)

		f.write('EnKF done\n')
		
		#write_kalman(k,n,lvar0,lvar1,dirpath,ensname)

		write_files(xnew,n,i,lvar0,lvar1,dirpath,ensname)
		if (i + runstep)//runstep*runstep < 10:	
			yr = '0000' + str((i + runstep)//runstep*runstep)
		elif (i + runstep)//runstep*runstep < 100:
			yr = '000' + str((i + runstep)//runstep*runstep)
		elif (i + runstep)//runstep*runstep < 1000:
			yr = '00' + str((i + runstep)//runstep*runstep)
		elif (i + runstep)//runstep*runstep < 10000:
			yr = '0' + str((i + runstep)//runstep*runstep)
		else:
			yr=str((i + runstep)//runstep*runstep)
		copy=[Popen(["nccopy","-k1",dirpath + "/" + ensname + str(j) + "/data/restartnew.nc",dirpath + "/" + ensname + str(j) + "/data/restart.nc"]) for j in range(50)]
		copywait=[copy[j].wait() for j in range(50)]
		time.sleep(3)
		remove=[Popen(["rm",dirpath + "/" + ensname + str(j) + "/data/restartnew.nc"]) for j in range(50)]
		chmod=[Popen(["chmod","+x",dirpath + "/" + ensname + str(j) + "/data/restart.nc"]) for j in range(50)]
		
		chmodwait=[chmod[j].wait() for j in range(50)]
		removewait=[remove[j].wait() for j in range(50)]	
	
		print('Restart files for year'+yr+ 'rewritten\n')
		f.write('Restart files for year'+yr+ 'rewritten\n')
		for j in range(n):
			jstr=str(j)
			os.system('qsub ' + dirpath + '/' + ensname + jstr+'/' + execname)
		print('Run '+str(step)+' launched')
		a,b,c,d=str(0),str(1),str(2),str(3)
		thres=0
		done=False
		time.sleep(180)
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
	f.write('The Kalman Filter has done its work!\n')
	f.close()
	os.system('for i in {0..' + str(n-1) + '}; do ncrcat -h "' + dirpath + '/' + ensname + '$i"/tsi.* "' + dirpath + '/' + ensname + '$i"/tsi' + runname + '.nc ; done') 
	os.system('for i in {0..' + str(n-1) + '}; do ncrcat -h "' + dirpath + '/' + ensname + '$i"/tavg.* "' + dirpath + '/' + ensname + '$i"/tavg' + runname + '.nc ; done')
	os.system('nces ' + dirpath + '/' + ensname + '*/' + 'tsi' + runname + '.nc ' + dirpath + '/tsi' + runname + 'stat.nc')
	merge_nofwf_stats(n,dirpath,ensname,runname)
	return ('The Kalman Filter has done its work!')

exe(n,Q,R,startyear,runtime,runstep,tsiint,tavgint,lvar0,lvar1,dirpath,ensname,datadir,execname,runname)
