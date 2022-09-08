#! /home/romainboutelet/miniconda3/bin/python



from netCDF4 import Dataset
import numpy as np
import os
from init_slgap import init_slgap

def get_slobs(slgap,dirpath,datadir,yr):
	tsifile = Dataset(dirpath + '/' + datadir +'/tsi.44910.01.31.nc')
	index = np.argmin(np.abs(tsifile['time'][:].data[tsifile['time'][:].data < yr]-yr))
	sltsi = tsifile['O_dsealev'][:].data[index]
	slobs = np.mean(slgap,axis=0) + sltsi
	return np.array([slobs])

def get_slobsrun(dirpath,datadir,yr):
	tsifile = Dataset(dirpath + '/' + datadir +'/tsisl_data.nc')
	index = np.argmin(np.abs(tsifile['time'][:].data[tsifile['time'][:].data < yr]-yr))
	sltsi = tsifile['sealev'][:].data[index]
	return np.array([sltsi])

if __name__ == '__main__':
	n = 50
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	yr = '44910'
	init_sealev = np.fromfunction(lambda i: np.random.normal(-132.8+0*i,0.00001),(n,))	
	slgap = init_slgap(n,dirpath,ensname,init_sealev,yr)
	yr = '44970'
	print(get_slobsrun(slgap,dirpath,datadir,yr))
