#! /usr/bin/python

import os
import numpy as np
import time

dirpath = "../ens_50lgm20yr"
dataname = 'data05tbiais_lgm20yr'
datapath = dirpath + '/' + dataname + '/'
ensname = 'obs_run'
enspath = dirpath + '/' + ensname + '/'
startyear = 44903
runtime = 20
runstep = 1
execname = 'c14.q'
tsiint = 10

def run_done(enspath):

	with open(enspath +  'pr', 'r') as f:
		lines = f.read().splitlines()
		last_line = lines[-1]
		done = '==>  UVIC_ESCM integration is complete.' in last_line
	return done


def write_control(enspath,runstep,tsiint):

	cont=open(enspath +'control.in','r')
	contnew=open(enspath +'controlbis.in','w')

	line1 = "&contrl init=.false., runlen=" + str(runstep*365) + "., rununits='days',\n"
	line2 = "&diagn  tsiint=" + str(tsiint) + "., tsiper=" + str(tsiint) + ".,\n"
	line3 = "        timavgint=" + str(runstep*365) + "., timavgper=" + str(runstep*365) + ".,\n"

	for line in cont:
		if '&contrl' in line:
			contnew.write(line1)
		elif '&diagn' in line:
			contnew.write(line2)
		elif 'timavgint' in line:
			contnew.write(line3)
		else:
			contnew.write(line)

	cont.close()
	contnew.close()
	os.system('mv ' + enspath + 'controlbis.in ' + enspath +'control.in')
	os.system('chmod +x '+ enspath + 'control.in')

	return

def exe_obs(startyear,runtime,runstep,dirpath,datapath,enspath,execname,tsiint):
	write_control(enspath,runstep,tsiint)
	for i in range(startyear, startyear + runtime, runstep):
		os.system('nccopy -k1 ' + datapath + 'rest.' + str(i) + '.01.01.nc ' + enspath + 'data/restart.nc')
		os.system('qsub ' + enspath +  execname)
		done = False
		time.sleep(60)
		while not done:
			time.sleep(1)
			done = run_done(enspath)
		time.sleep(5)
	return

exe_obs(startyear,runtime,runstep,dirpath,datapath,enspath,execname,tsiint)



