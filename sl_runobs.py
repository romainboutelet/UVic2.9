#! /home/romainboutelet/miniconda3/bin/python

import os 
import time
import pandas as pd
import numpy as np
from write_control import write_runobs_control
from fwf_file import fwf_obsfile, fwf_2obsfile

def runobs_sldata3000(dirpath,ensname,execname,inityear,tsiint,tavgint,tavgper):
	
	os.system('rm ' + dirpath + '/' + ensname + '/data/restart.nc')
	os.system('nccopy -k1 ' + dirpath + '/' + ensname + '/data/restartb.nc ' + dirpath + '/' + ensname + '/data/restart.nc')
	age = np.array([4000,4200,4350,4600,4700,4850,4900,5050,5300,5350,5400,5500,5600,5800,5850,6000,6050,6100,6150,6300,6400,6500,6750,6800,6950,7000])
	fwf1 = np.array([0.0,0.03,0.08,0.12,0.02,0.04,0.05,0.09,0.01,0.00,0.02,0.06,0.09,0.08,0.01,0.11,0.10,0.09,0.11,0.1,0.02,0.05,0.11,0.02,0.03,0.02])
	fwfrate1 = (fwf1[1:]-fwf1[:-1])/(age[1:]-age[:-1])
	fwf2 = np.array([0.00,0.01,0.02,0.04,0.005,0.,0.03,0.06,0.09,0.08,0.07,0.09,0.10,0.12,0.09,0.06,0.06,0.05,0.06,0.08,0.05,0.03,0.02,0.04,0.03,0.05])
	fwfrate2 = (fwf2[1:]-fwf2[:-1])/(age[1:]-age[:-1])
	diffyear = inityear - age[0]
	np.savez(dirpath + '/' + ensname + '/fwfobs_hist', fwf1 = fwf1, fwfrate1 = fwfrate1, fwf2= fwf2, fwfrate2 = fwfrate2, age = age)
	for i in range(0,len(age)-1):
		modelyear = int(diffyear + ageobs[i])
		runstep = int(age[i+1]-age[i])
		write_runobs_control(dirpath,ensname,runstep,tsiint,tavgint,tavgper)
		fwf_2obsfile(fwf1[i],fwf2[i],fwfrate1[i],fwfrate2[i],dirpath,ensname,modelyear,runstep)
		os.system('qsub ' + dirpath + '/' + ensname + '/' + execname)
		time.sleep(60)
		done = False
		while not done : 		
			time.sleep(1)
			with open(dirpath + '/' + ensname + '/pr', 'r') as f:
				lines = f.read().splitlines()
				last_line = lines[-1]
				done = '==>  UVIC_ESCM integration is complete.' in last_line
		time.sleep(10)
		os.system('rm ' + execname + '.*')
	return
		
		
def runobs_sldata(dirpath,ensname,execname,inityear,tsiint,tavgint,tavgper):
	
	os.system('rm ' + dirpath + '/' + ensname + '/data/restart.nc')
	os.system('nccopy -k1 ' + dirpath + '/' + ensname + '/data/restartb.nc ' + dirpath + '/' + ensname + '/data/restart.nc')

	ageobs = np.array([4000,4050,4200,4350,4500])
	fwfobs = np.array([0.,0.15,0.15,0.,0.])
	fwfrate = (fwfobs[1:]-fwfobs[:-1])/(ageobs[1:]-ageobs[:-1])
	diffyear = inityear - ageobs[0]
	np.savez(dirpath + '/' + ensname + '/fwfobs_hist', fwf = fwfobs, fwfrate = fwfrate, age = ageobs)
	for i in range(0,len(ageobs)-1):
		modelyear = int(diffyear + ageobs[i])
		runstep = int(ageobs[i+1]-ageobs[i])
		write_runobs_control(dirpath,ensname,runstep,tsiint,tavgint,tavgper)
		fwf_obsfile(fwfobs[i],fwfrate[i],dirpath,ensname,modelyear,runstep)
		os.system('qsub ' + dirpath + '/' + ensname + '/' + execname)
		time.sleep(60)
		done = False
		while not done : 		
			time.sleep(1)
			with open(dirpath + '/' + ensname + '/pr', 'r') as f:
				lines = f.read().splitlines()
				last_line = lines[-1]
				done = '==>  UVIC_ESCM integration is complete.' in last_line
		time.sleep(10)
		os.system('rm ' + execname + '.*')
	return


def runobs_2sldata(dirpath,ensname,execname,inityear,tsiint,tavgint,tavgper):
	
	os.system('rm ' + dirpath + '/' + ensname + '/data/restart.nc')
	os.system('nccopy -k1 ' + dirpath + '/' + ensname + '/data/restartb.nc ' + dirpath + '/' + ensname + '/data/restart.nc')


	ageobs = np.array([4000,4050,4150,4300,4350,4500])
	fwfobs1 = np.array([0.,0.15,0.15,0.,0.,0.])
	fwfobs2 = np.array([0.,0.,0.,0.15,0.,0.])
	fwfrate1 = (fwfobs1[1:]-fwfobs1[:-1])/(ageobs[1:]-ageobs[:-1])
	fwfrate2 = (fwfobs2[1:]-fwfobs2[:-1])/(ageobs[1:]-ageobs[:-1])
	diffyear = inityear - ageobs[0]
	np.savez(dirpath + '/' + ensname + '/fwfobs_hist', fwf1 = fwfobs1, fwf2 = fwfobs2, fwfrate1 = fwfrate1, fwfrate2 = fwfrate2, age = ageobs)
	for i in range(0,len(ageobs)-1):
		modelyear = int(diffyear + ageobs[i])
		runstep = int(ageobs[i+1]-ageobs[i])
		write_runobs_control(dirpath,ensname,runstep,tsiint,tavgint,tavgper)
		fwf_2obsfile(fwfobs1[i],fwfobs2[i],fwfrate1[i],fwfrate2[i],dirpath,ensname,modelyear,runstep)
		os.system('qsub ' + dirpath + '/' + ensname + '/' + execname)
		time.sleep(60)
		done = False
		while not done : 		
			time.sleep(1)
			with open(dirpath + '/' + ensname + '/pr', 'r') as f:
				lines = f.read().splitlines()
				last_line = lines[-1]
				done = '==>  UVIC_ESCM integration is complete.' in last_line
		time.sleep(10)
		os.system('rm ' + execname + '.*')
	return

		
		






if __name__ == '__main__':
	inityear = 4000
	tsiint = 30             # in days
	tavgper = 30            # in days
	tavgint = 50             # in years
	dirpath = '../ensbis_50fwfnb200yr'
	ensname = 'target_3000yr'
	execname = 'fwfnobio.q'
	runobs_sldata3000(dirpath,ensname,execname,inityear,tsiint,tavgint,tavgper)
