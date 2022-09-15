#! /home/romainboutelet/miniconda3/bin/python

from netCDF4 import Dataset
import numpy as np
import os
import time
from write_control import write_runobs_control

def run_obs(dirpath,datadir,rundir,startyear,runtime,runstep,tsiint,tavgint,execname):
	os.system('rm ' + dirpath + '/' + rundir + '/tsi.*')
	os.system('rm ' + dirpath + '/' + rundir + '/tavg.*')
	write_runobs_control(dirpath,rundir,runstep,tsiint,tavgint)
	for i in range(startyear,startyear+runtime,runstep):
		os.system('rm ' + dirpath + '/' + rundir + '/data/restart.nc')
		os.system('nccopy -k1 ' + dirpath + '/' + datadir + '/rest.' + str(i) + '.01.01.nc ' + dirpath + '/' + rundir + '/data/restart.nc')
		
		os.system('qsub ' + dirpath + '/' + rundir + '/' + execname)
		time.sleep(60)
		done = False
		while not done : 		
			time.sleep(1)
			with open(dirpath + '/' + rundir + '/pr', 'r') as f:
				lines = f.read().splitlines()
				last_line = lines[-1]
				done = '==>  UVIC_ESCM integration is complete.' in last_line
		time.sleep(10)
		os.system('rm ' + execname + '.*')
	return

if __name__ == '__main__':
	startyear = 44903
	runtime = 20
	runstep = 1
	tsiint = 30
	tavgint = 30
	runname = '05tbiais05cluster_lgm20yr'
	dirpath = '../ens_50lgm20yr'
	rundir = 'obs_run'
	datadir = 'data05tbiais05_lgm20yr'
	execname = 'c14.q' 
	run_obs(dirpath,datadir,rundir,startyear,runtime,runstep,tsiint,tavgint,execname)
			
	
