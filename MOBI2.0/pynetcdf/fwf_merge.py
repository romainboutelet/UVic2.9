#! /home/romainboutelet/miniconda3/bin/python

import os
import numpy as np
from netCDF4 import Dataset

def fwf_merge(n,dirpath,ensname,runtime,runstep,runname,tsiint):	
	
	hist = np.load(dirpath + '/fwf_hist.npz')

	trend = hist['trend']
	trend.shape=(n,runtime)
	stoch = hist['stoch']
	stoch.shape=(n,runtime)
	kal = hist['kal']
	kal.shape = (n,runtime)
	sealev = hist['sealev'][:,1:,:]
	sealev.shape = (n,runtime)

	y=np.zeros((n,(runtime*365)//tsiint))
	tsiday = 0
	ntsi = 0
	ptsi = 0

	trendtsi = np.zeros((n,(runtime*365)//tsiint))
	stochtsi = np.zeros((n,(runtime*365)//tsiint))
	kaltsi = np.zeros((n,(runtime*365)//tsiint))
	sealevtsi = np.zeros((n,(runtime*365)//tsiint))
	for i in range(0,runtime):
		tsiday += 365
		ntsi = tsiday // tsiint
		
		kaltsi[:,ptsi:(ptsi+ntsi)] = np.array([[kal[j,i] for k in range(ntsi)] for j in range(n)])
		trendtsi[:,ptsi:(ptsi+ntsi)] = np.array([[trend[j,i] for k in range(ntsi)] for j in range(n)])
		stochtsi[:,ptsi:(ptsi+ntsi)] = np.array([[stoch[j,i] for k in range(ntsi)] for j in range(n)])
		sealevtsi[:,ptsi:(ptsi+ntsi)] = np.array([[sealev[j,i] for k in range(ntsi)] for j in range(n)])
		ptsi += ntsi
		tsiday = tsiday%tsiint	
	y = trendtsi + stochtsi + kaltsi
	for j in range(n):
		fwf_file = Dataset(dirpath + '/' + ensname + str(j) + '/tsi' + runname + '.nc' , 'r+', format='NETCDF4')

		outvar1=fwf_file.createVariable('fwfflx','float64',('time'))
		outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater flux input at tau'})
		outvar1[:]=y[j]

		outvar2=fwf_file.createVariable('fwftrend','float64',('time'))
		outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater flux trend input at tau'})
		outvar2[:]=trendtsi[j]

		outvar3=fwf_file.createVariable('fwfstoch','float64',('time'))
		outvar3.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater stochastic flux input at tau'})
		outvar3[:]=stochtsi[j]

		outvar4=fwf_file.createVariable('fwfkal','float64',('time'))
		outvar4.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater kalman filter total flux input at tau'})
		outvar4[:]=kaltsi[j]

		outvar5=fwf_file.createVariable('sealev','float64',('time'))
		outvar5.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Sea level at tau'})
		outvar5[:]=sealevtsi[j]
		
		fwf_file.close()
	return
	
	
def fwf_2merge(n,dirpath,ensname,runtime,runstep,runname,tsiint):	
	
	hist = np.load(dirpath + '/fwf_hist.npz')

	trend1 = hist['trend1']
	trend1.shape=(n,runtime)
	stoch1 = hist['stoch1']
	stoch1.shape=(n,runtime)
	kal1 = hist['kal1']
	kal1.shape = (n,runtime)

	trend2 = hist['trend2']
	trend2.shape=(n,runtime)
	stoch2 = hist['stoch2']
	stoch2.shape=(n,runtime)
	kal2 = hist['kal2']
	kal2.shape = (n,runtime)
	
	sealev = hist['sealev'][:,1:,:]
	sealev.shape = (n,runtime)
	cumul1 = hist['cumul1'][:,:,:]
	cumul1.shape = (n,runtime)
	cumul2 = hist['cumul2'][:,:,:]
	cumul2.shape = (n,runtime)

	y1=np.zeros((n,(runtime*365)//tsiint))
	y2=np.zeros((n,(runtime*365)//tsiint))
	tsiday = 0
	ntsi = 0
	ptsi = 0

	trend1tsi = np.zeros((n,(runtime*365)//tsiint))
	stoch1tsi = np.zeros((n,(runtime*365)//tsiint))
	kal1tsi = np.zeros((n,(runtime*365)//tsiint))

	trend2tsi = np.zeros((n,(runtime*365)//tsiint))
	stoch2tsi = np.zeros((n,(runtime*365)//tsiint))
	kal2tsi = np.zeros((n,(runtime*365)//tsiint))

	sealevtsi = np.zeros((n,(runtime*365)//tsiint))
	cumul1tsi = np.zeros((n,(runtime*365)//tsiint))
	cumul2tsi = np.zeros((n,(runtime*365)//tsiint))
	for i in range(0,runtime):
		tsiday += 365
		ntsi = tsiday // tsiint
		
		kal1tsi[:,ptsi:(ptsi+ntsi)] = np.array([[kal1[j,i] for k in range(ntsi)] for j in range(n)])
		trend1tsi[:,ptsi:(ptsi+ntsi)] = np.array([[trend1[j,i] for k in range(ntsi)] for j in range(n)])
		stoch1tsi[:,ptsi:(ptsi+ntsi)] = np.array([[stoch1[j,i] for k in range(ntsi)] for j in range(n)])
		kal2tsi[:,ptsi:(ptsi+ntsi)] = np.array([[kal2[j,i] for k in range(ntsi)] for j in range(n)])
		trend2tsi[:,ptsi:(ptsi+ntsi)] = np.array([[trend2[j,i] for k in range(ntsi)] for j in range(n)])
		stoch2tsi[:,ptsi:(ptsi+ntsi)] = np.array([[stoch2[j,i] for k in range(ntsi)] for j in range(n)])
		sealevtsi[:,ptsi:(ptsi+ntsi)] = np.array([[sealev[j,i] for k in range(ntsi)] for j in range(n)])
		cumul1tsi[:,ptsi:(ptsi+ntsi)] = np.array([[cumul1[j,i] for k in range(ntsi)] for j in range(n)])
		cumul2tsi[:,ptsi:(ptsi+ntsi)] = np.array([[cumul2[j,i] for k in range(ntsi)] for j in range(n)])
		ptsi += ntsi
		tsiday = tsiday%tsiint	
		
	y1 = trend1tsi + stoch1tsi + kal1tsi
	y2 = trend2tsi + stoch2tsi + kal2tsi
	
	for j in range(n):
		fwf_file = Dataset(dirpath + '/' + ensname + str(j) + '/tsi' + runname + '.nc' , 'r+', format='NETCDF4')

		outvar1=fwf_file.createVariable('fwfflx1','float64',('time'))
		outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater flux input in North Atlantic Ocean at tau'})
		outvar1[:]=y1[j]

		outvar2=fwf_file.createVariable('fwftrend1','float64',('time'))
		outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater flux trend input in North Atlantic Ocean at tau'})
		outvar2[:]=trend1tsi[j]

		outvar3=fwf_file.createVariable('fwfstoch1','float64',('time'))
		outvar3.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater stochastic flux input in North Atlantic Ocean at tau'})
		outvar3[:]=stoch1tsi[j]

		outvar4=fwf_file.createVariable('fwfkal1','float64',('time'))
		outvar4.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater kalman filter total flux in North Atlantic Ocean input at tau'})
		outvar4[:]=kal1tsi[j]
		
		outvar5=fwf_file.createVariable('fwfflx2','float64',('time'))
		outvar5.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater flux input in Southern Ocean at tau'})
		outvar5[:]=y2[j]

		outvar6=fwf_file.createVariable('fwftrend2','float64',('time'))
		outvar6.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater flux trend input in Southern Ocean at tau'})
		outvar6[:]=trend2tsi[j]

		outvar7=fwf_file.createVariable('fwfstoch2','float64',('time'))
		outvar7.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater stochastic flux input in Southern Ocean at tau'})
		outvar7[:]=stoch2tsi[j]

		outvar8=fwf_file.createVariable('fwfkal2','float64',('time'))
		outvar8.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'freshwater kalman filter total flux in Southern Ocean input at tau'})
		outvar8[:]=kal2tsi[j]

		outvar9=fwf_file.createVariable('sealev','float64',('time'))
		outvar9.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Sea level at tau'})
		outvar9[:]=sealevtsi[j]
		
		outvar10=fwf_file.createVariable('cumul1','float64',('time'))
		outvar10.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Cumulative Freshwater input in the North Atkantic at tau'})
		outvar10[:]=cumul1tsi[j]
		
		outvar11=fwf_file.createVariable('cumul2','float64',('time'))
		outvar11.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Cumulative Freshwater input in the Southern Ocean at tau'})
		outvar11[:]=cumul2tsi[j]
		
		fwf_file.close()
	return
	
	
if __name__=='__main__':
	n = 50
	Q = 0.5
	R = 0.5
	fwf_init = 0.09
	#fwfobs = np.array([-0.003/4,-0.003/4,0.005,0.002,-0.006,0.003,-0.003,0.003,-0.002,-0.001,0.0005,0.0005,0.003,-0.004,0.002,0.002,0.0005,0.0005,-0.001,-0.001])
		
	startyear = 4000
	runtime = 500
	runstep = 50
	fwfobs = np.zeros(int(runtime//runstep))
	tsiint = 30                   # in days
	tavgint = 30
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	datadir = 'see later'
	execname = 'fwfnobio.q'
	runname = 'fwf_diff0.025kalpi500yr_r5_q1_tavgint50slopeall'
	fwf_merge(n,dirpath,ensname,runtime,runstep,runname,tsiint)

