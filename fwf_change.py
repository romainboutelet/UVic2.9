#! /home/romainboutelet/miniconda3/bin/python

import os
import numpy as np

def sea_lev_rise(fwfflx):
	vol_water = 1e6*fwfflx*3600*24*365/1e9                #(km³ of water added in a year at for fwfflx Sv during this year)
	surf_water = 361.9*1e6                                #Surface of ocean on Earth
	return 1000*vol_water/surf_water                      #Recalibrated to be in m

def fwf_value(n,fwftrend, fwfkal):
	fwfvalue = fwftrend[:,-1,-1] + fwfkal[:,-1,-1]
	return fwfvalue

def fwf_change(n,fwf_init,fwf_rate,dirpath,ensname,runstep,step,init_sealev):
	if step == 0:
		fwfinit=np.array([fwf_init for i in range(n)])
		fwfrate = np.array([[fwf_rate[step]] for i in range(n)])
		sealev = np.array([[init_sealev[j] for i in range(runstep)] for j in range(n)])
		sealev.shape = (n,1,runstep)
		
		np.savez(dirpath + '/fwf_hist', sealev = sealev)

	
	elif step == 1:
		fwfrate = np.array([[fwf_rate[step]] for i in range(n)]) 
		
		hist=np.load(dirpath + '/fwf_hist.npz')

		kal = np.array(hist['kal'][:,-1])
		kal.shape = (n,1,runstep)
		fwfstoch = np.array(hist['stoch'][:,-1])
		fwfstoch.shape = (n,1,runstep)

		fwftrend = np.array([[fwf_init for i in range(runstep)] for j in range(n)]) + np.array([np.arange(runstep)*fwf_rate[step-1] for j in range(n)])

		fwftrend.shape = (n,1,runstep)

		fwfflx = kal + fwftrend + fwfstoch

		sealev = np.zeros((n,1,runstep))
		sealev[:,0,0] = hist['sealev'][:,-1,-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx[j,0,0] + 0*j),(n,),dtype = int)
		for i in range(1,runstep):
			sealev[:,0,i] = sealev[:,0,i-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx[j,0,i]),(n,),dtype=int)


		np.savez(dirpath + '/fwf_hist', trend = fwftrend, stoch = hist['stoch'], kal = hist['kal'], sealev = np.concatenate((hist['sealev'],sealev),axis=1))

		fwfinit = fwf_value(n,fwftrend,kal)

	
	
	elif step > 1 :
		if step >= len(fwf_rate):
			fwfrate = np.array([[fwf_rate[0]] for i in range(n)])
		else: 
			fwfrate = np.array([[fwf_rate[step]] for i in range(n)])
		hist=np.load(dirpath + '/fwf_hist.npz')

		kal = np.array(hist['kal'][:,-1])
		kal.shape = (n,1,runstep)
		fwfstoch = np.array(hist['stoch'][:,-1])
		fwfstoch.shape = (n,1,runstep)

		fwftrend = np.array([[hist['trend'][i,-1,-1] for k in range(runstep)] for i in range(n)]) + np.array([np.arange(runstep)*fwf_rate[step-1] for j in range(n)])
		fwftrend.shape = (n,1,runstep)

		fwfflx = fwftrend + fwfstoch + kal		

		sealev = np.zeros((n,1,runstep))
		sealev[:,0,0] = hist['sealev'][:,-1,-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx[j,0,0] + 0*j),(n,),dtype = int)
		for i in range(1,runstep):
			sealev[:,0,i] = sealev[:,0,i-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx[j,0,i]),(n,),dtype=int)


		np.savez(dirpath + '/fwf_hist', trend = np.concatenate((hist['trend'],fwftrend), axis=1), stoch = hist['stoch'], kal = hist['kal'],sealev = np.concatenate((hist['sealev'],sealev),axis=1))

		fwfinit = fwf_value(n,fwftrend, kal )
		
	fwfrate.shape=n
	
	return fwfinit, fwfrate

def fwf_2change(n,fwf_init1,fwf_init2,fwf_rate,dirpath,ensname,runstep,step,init_sealev):
	if step == 0:
		fwfinit1=np.array([fwf_init1 for i in range(n)])
		fwfinit2=np.array([fwf_init2 for i in range(n)])
		fwfrate = np.array([[fwf_rate[step]] for i in range(n)])
		
		sealev = np.array([[init_sealev[j] for i in range(runstep)] for j in range(n)])
		sealev.shape = (n,1,runstep)
		hist=np.load(dirpath + '/fwf_hist.npz')
		
		np.savez(dirpath + '/fwf_hist',sealev = sealev)

	
	elif step == 1:
		fwfrate = np.array([[fwf_rate[step]] for i in range(n)]) 
		
		hist=np.load(dirpath + '/fwf_hist.npz')

		kal1 = np.array(hist['kal1'][:,-1])
		kal2 = np.array(hist['kal2'][:,-1])		
		kal1.shape = (n,1,runstep)
		kal2.shape = (n,1,runstep)
		
		fwfstoch1 = np.array(hist['stoch1'][:,-1])
		fwfstoch1.shape = (n,1,runstep)
		fwfstoch2 = np.array(hist['stoch2'][:,-1])
		fwfstoch2.shape = (n,1,runstep)

		fwftrend1 = np.array([[fwf_init1 for i in range(runstep)] for j in range(n)]) + np.array([np.arange(runstep)*fwf_rate[step-1] for j in range(n)])
		fwftrend2 = np.array([[fwf_init2 for i in range(runstep)] for j in range(n)]) + np.array([np.arange(runstep)*fwf_rate[step-1] for j in range(n)])

		fwftrend1.shape = (n,1,runstep)
		fwftrend2.shape = (n,1,runstep)

		fwfflx1 = kal1 + fwftrend1 + fwfstoch1
		fwfflx2 = kal2 + fwftrend2 + fwfstoch2

		sealev = np.zeros((n,1,runstep))
		sealev[:,0,0] = init_sealev + np.fromfunction(lambda j: sea_lev_rise(fwfflx1[j,0,0]+ 0*j),(n,),dtype = int) + np.fromfunction(lambda j: sea_lev_rise(fwfflx2[j,0,0]+ 0*j),(n,),dtype = int)
		for i in range(1,runstep):
			sealev[:,0,i] = sealev[:,0,i-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx1[j,0,i]),(n,), dtype = int) + np.fromfunction(lambda j: sea_lev_rise(fwfflx2[j,0,i]),(n,), dtype = int)
			
		cumul1 = np.zeros((n,1,runstep))
		cumul1[:,0,0] = np.fromfunction(lambda j: sea_lev_rise(fwfflx1[j,0,0]+ 0*j),(n,),dtype = int)
		for i in range(1,runstep):
			cumul1[:,0,i] = cumul1[:,0,i-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx1[j,0,i]),(n,), dtype = int)
			
		cumul2 = np.zeros((n,1,runstep))
		cumul2[:,0,0] = np.fromfunction(lambda j: sea_lev_rise(fwfflx2[j,0,0]+ 0*j),(n,),dtype = int)
		for i in range(1,runstep):
			cumul2[:,0,i] = cumul2[:,0,i-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx2[j,0,i]),(n,), dtype = int)

		np.savez(dirpath + '/fwf_hist', trend1 = fwftrend1, stoch1 = hist['stoch1'], kal1 = hist['kal1'], trend2 = fwftrend2, stoch2 = hist['stoch2'], kal2 = hist['kal2'], sealev = np.concatenate((hist['sealev'],sealev),axis=1), cumul1 = cumul1, cumul2 = cumul2)

		fwfinit1 = fwf_value(n,fwftrend1,kal1)
		fwfinit2 = fwf_value(n,fwftrend2,kal2)
	
	
	elif step > 1 :
		if step >= len(fwf_rate):
			fwfrate = np.array([[fwf_rate[0]] for i in range(n)])
		else: 
			fwfrate = np.array([[fwf_rate[step]] for i in range(n)])
		hist=np.load(dirpath + '/fwf_hist.npz')

		kal1 = np.array(hist['kal1'][:,-1])
		kal2 = np.array(hist['kal2'][:,-1])		
		kal1.shape = (n,1,runstep)
		kal2.shape = (n,1,runstep)
		
		fwfstoch1 = np.array(hist['stoch1'][:,-1])
		fwfstoch1.shape = (n,1,runstep)
		fwfstoch2 = np.array(hist['stoch2'][:,-1])
		fwfstoch2.shape = (n,1,runstep)

		fwftrend1 = np.array([[hist['trend1'][i,-1,-1] for k in range(runstep)] for i in range(n)]) + np.array([np.arange(runstep)*fwf_rate[step-1] for j in range(n)])
		fwftrend2 = np.array([[hist['trend2'][i,-1,-1] for k in range(runstep)] for i in range(n)]) + np.array([np.arange(runstep)*fwf_rate[step-1] for j in range(n)])
		fwftrend1.shape = (n,1,runstep)
		fwftrend2.shape = (n,1,runstep)

		fwfflx1 = kal1 + fwftrend1 + fwfstoch1
		fwfflx2 = kal2 + fwftrend2 + fwfstoch2
		
		sealev = np.zeros((n,1,runstep))
		sealev[:,0,0] = hist['sealev'][:,-1,-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx1[j,0,0] + 0*j),(n,),dtype = int) + np.fromfunction(lambda j: sea_lev_rise(fwfflx2[j,0,0] + 0*j),(n,),dtype = int)
		for i in range(1,runstep):
			sealev[:,0,i] = sealev[:,0,i-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx1[j,0,i]),(n,),dtype=int) + np.fromfunction(lambda j: sea_lev_rise(fwfflx2[j,0,i]),(n,),dtype=int)
			
		cumul1 = np.zeros((n,1,runstep))
		cumul1[:,0,0] = hist['cumul1'][:,-1,-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx1[j,0,0] + 0*j),(n,),dtype = int)
		for i in range(1,runstep):
			cumul1[:,0,i] = cumul1[:,0,i-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx1[j,0,i]),(n,),dtype=int)

		cumul2 = np.zeros((n,1,runstep))
		cumul2[:,0,0] = hist['cumul2'][:,-1,-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx2[j,0,0] + 0*j),(n,),dtype = int)
		for i in range(1,runstep):
			cumul2[:,0,i] = cumul2[:,0,i-1] + np.fromfunction(lambda j: sea_lev_rise(fwfflx2[j,0,i]),(n,),dtype=int)


		np.savez(dirpath + '/fwf_hist', trend1 = np.concatenate((hist['trend1'],fwftrend1), axis=1), stoch1 = hist['stoch1'], kal1 = hist['kal1'], trend2 = np.concatenate((hist['trend2'],fwftrend2), axis=1), stoch2 = hist['stoch2'], kal2 = hist['kal2'], sealev = np.concatenate((hist['sealev'],sealev),axis=1),  cumul1 = np.concatenate((hist['cumul1'],cumul1),axis=1),  cumul2 = np.concatenate((hist['cumul2'],cumul2),axis=1))

		fwfinit1 = fwf_value(n,fwftrend1,kal1)
		fwfinit2 = fwf_value(n,fwftrend2,kal2)
		
	fwfrate.shape=n
	
	return fwfinit1,fwfinit2, fwfrate


if __name__=='__main__':
	n = 50
	Q = 20
	R = 25
	fwf_init = 0.09
	randamp = 0.01
	startyear = 44910
	runtime = 100
	runstep = 10
	tsiint = 30                   # in days
	tavgint = 30
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	datadir = dirpath + '/../target_rest'
	execname = 'fwfnobio.q'
	runname = 'fwf100yrd13cfwfbkalpi_amp01_r25_q20targetdat'
	#fwf_rate = 1* np.array([-0.003/4,-0.003/4,0.005,0.002,-0.006,0.003,-0.003,0.003,-0.002,-0.001,0.0005,0.0005,0.003,-0.004,0.002,0.002,0.0005,0.0005,-0.001,-0.001])
	fwf_rate = np.zeros(int(runtime//runstep))
	initage = 21000
	init_sealev = np.fromfunction(lambda i: np.random.normal(-136+0*i,4),(n,))
	step = 1
	fwf_change(n,fwf_init,fwf_rate,dirpath,ensname,runstep,step,init_sealev)

