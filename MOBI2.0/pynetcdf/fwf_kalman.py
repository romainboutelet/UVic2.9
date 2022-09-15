#! /usr/bin/python

import numpy as np

def sea_lev_rise(fwfflx):
	vol_water = 1e6*fwfflx*3600*24*365/1e9                #(km³ of water added in a year at for fwfflx Sv during this year)
	surf_water = 361.9*1e6                                #Surface of ocean on Earth
	return 1000*vol_water/surf_water                      #Recalibrated to be in m

def fwf_kalman(n,fwfinit,xnew,randamp,dirpath,step,runstep):
	
	if step == 0:
		kal = xnew - fwfinit
		kalnew = np.array([[kal[i] for j in range(runstep)] for i in range(n)])
		kalnew.shape = (n,1,runstep)
		
		stoch = np.random.normal(0,randamp,n)
		fwfstoch = np.array([[stoch[i] for j in range(runstep)] for i in range(n)])
		fwfstoch.shape = (n,1,runstep)
		
		hist = np.load(dirpath + '/fwf_hist.npz')

		np.savez(dirpath + '/fwf_hist', kal = kalnew, stoch = fwfstoch, sealev = hist['sealev'])



	else:
		hist = np.load(dirpath + '/fwf_hist.npz')
		
		kal = xnew - fwfinit - hist['stoch'][:,-1,-1]
		kalnew = hist['kal'][:,-1]
		kalnew += np.array([[kal[i] for j in range(runstep)] for i in range(n)])
		kalnew.shape = (n,1,runstep)
		
		stoch = np.random.normal(0,randamp,n)
		fwfstoch = np.array([[stoch[i] for j in range(runstep)] for i in range(n)])
		fwfstoch.shape = (n,1,runstep)
		

		np.savez(dirpath + '/fwf_hist', trend = hist['trend'], stoch = np.concatenate((hist['stoch'],fwfstoch),axis=1), kal = np.concatenate((hist['kal'],kalnew),axis=1), sealev = hist['sealev'])

	return
	
def fwf_2kalman(n,fwfinit1,fwfinit2,fwfinit1new,fwfinit2new,randamp1,randamp2,dirpath,step,runstep):
	
	if step == 0:
		kal1 = fwfinit1new - fwfinit1
		kal2 = fwfinit2new - fwfinit2
		kal1new = np.array([[kal1[i] for j in range(runstep)] for i in range(n)])
		kal2new = np.array([[kal2[i] for j in range(runstep)] for i in range(n)])
		kal1new.shape = (n,1,runstep)
		kal2new.shape = (n,1,runstep)
		
		stoch1 = np.random.normal(0,randamp1,n)
		fwfstoch1 = np.array([[stoch1[i] for j in range(runstep)] for i in range(n)])
		fwfstoch1.shape = (n,1,runstep)
		
		stoch2 = np.random.normal(0,randamp2,n)
		fwfstoch2 = np.array([[stoch2[i] for j in range(runstep)] for i in range(n)])
		fwfstoch2.shape = (n,1,runstep)
			
		hist=np.load(dirpath + '/fwf_hist.npz')

		np.savez(dirpath + '/fwf_hist', kal1 = kal1new, kal2 = kal2new, stoch1 = fwfstoch1, stoch2 = fwfstoch2, sealev = hist['sealev'])



	else:
		hist = np.load(dirpath + '/fwf_hist.npz')
		
		kal1 = fwfinit1new - fwfinit1 - hist['stoch1'][:,-1,-1]
		kal2 = fwfinit2new - fwfinit2 - hist['stoch2'][:,-1,-1]
		kal1new = hist['kal1'][:,-1]
		kal2new = hist['kal2'][:,-1]
		kal1new += np.array([[kal1[i] for j in range(runstep)] for i in range(n)])
		kal2new += np.array([[kal2[i] for j in range(runstep)] for i in range(n)])
		kal1new.shape = (n,1,runstep)
		kal2new.shape = (n,1,runstep)
		
		stoch1 = np.random.normal(0,randamp1,n)
		fwfstoch1 = np.array([[stoch1[i] for j in range(runstep)] for i in range(n)])
		fwfstoch1.shape = (n,1,runstep)
		
		stoch2 = np.random.normal(0,randamp2,n)
		fwfstoch2 = np.array([[stoch2[i] for j in range(runstep)] for i in range(n)])
		fwfstoch2.shape = (n,1,runstep)
		
		np.savez(dirpath + '/fwf_hist', trend1 = hist['trend1'], stoch1 = np.concatenate((hist['stoch1'],fwfstoch1),axis=1), kal1 = np.concatenate((hist['kal1'],kal1new),axis=1), trend2 = hist['trend2'], stoch2 = np.concatenate((hist['stoch2'],fwfstoch2),axis=1), kal2 = np.concatenate((hist['kal2'],kal2new),axis=1), sealev = hist['sealev'], cumul1 = hist['cumul1'], cumul2 = hist['cumul2'])

	return

if __name__ == '__main__':
	from d13C import d13C, d13Cobs
	from EnKF_fwf import EnKFfwf
	n = 50
	Q = 5
	R = 1
	fwf_init = 0.7
	randamp = 0.005
	startyear = 44910
	runtime = 500
	runstep = 10
	tsiint = 30                   # in days
	tavgint = 30
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	datadir = '../target_rest'
	execname = 'fwfnobio.q'
	runname = 'fwf500yrkalpi'
	#fwfobs = 1* np.array([-0.003/4,-0.003/4,0.005,0.002,-0.006,0.003,-0.003,0.003,-0.002,-0.001,0.0005,0.0005,0.003,-0.004,0.002,0.002,0.0005,0.0005,-0.001,-0.001])
	fwfobs = np.zeros(int(runtime//runstep))
	step = 2
	d13c = d13C(n,dirpath,ensname)
	d13cobs = d13Cobs(dirpath,datadir,'44950')
	xnew = EnKFfwf(d13c,d13cobs,Q,R,randamp,n,dirpath,ensname) 
	hist = np.load(dirpath + '/fwf_hist.npz')
	fwfinit = hist['trend'][:,-1,-1] + hist['kal'][:,-1,-1]
	kal = xnew - fwfinit
	kalnew = np.array([[kal[i] for j in range(runstep)] for i in range(n)])
	kalnew.shape = (n,1,runstep)
	fwfkal = hist['kal']
	kalnew[:,0] = kalnew[:,0] + [[fwfkal[i,-1,-1] for j in range(runstep)] for i in range(n)]
	np.concatenate((fwfkal,kalnew),axis=1)
	print(newkal,newkal.shape)
	
	
	
	


