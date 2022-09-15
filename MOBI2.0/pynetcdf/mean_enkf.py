#! /usr/bin/python

import numpy as np
from EnKF_fwf import EnKFfwf

def mean_enkf(N,Q,R,randamp,slstart,n,dirpath,ensname,datadir,runname,yr,agerel,runstep,step,tavgint,tavgfile):
	x = []
	for i in range(N):
		x.append(np.mean(EnKFfwf(Q,R,randamp,slstart,n,dirpath,ensname,datadir,runname,yr,agerel,runstep,step,tavgint,tavgfile)))
	return x, np.mean(x)

if __name__ == '__main__':
	from fwf_change import fwf_change
	from d13C import d13C, d13Cobs

	n = 50
	Q = 1
	R = 5
	fwf_init = 0
	slstart = -132.8
	randamp = 0.025
	startyear = 4000
	runtime = 500
	runstep = 50
	tsiint = 30                   # in days
	tavgint = 5                   # in years
	tavgfile = 'tavgeqtavgint5.nc'
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	datadir = 'data_slopedrop'
	execname = 'fwfnobio.q'
	runname = 'fwf100yrsingkalpi_amp01_r1_q5'


	agerel = 19740
	step = 9

	yr = '04450'
	init_sealev = np.fromfunction(lambda i: np.random.normal(-132.8+0*i,0.00001),(n,))	
	N = 30
	x,xmean=mean_enkf(N,Q,R,randamp,slstart,n,dirpath,ensname,datadir, runname,yr, agerel, runstep,step,tavgint,tavgfile)
	print(x,xmean)
