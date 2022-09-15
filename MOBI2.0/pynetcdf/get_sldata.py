#! /home/romainboutelet/miniconda3/bin/python



from netCDF4 import Dataset
import numpy as np
import os
from get_tsiname import get_tsipath
from init_slgap import init_slgap

def get_sldata(n,slgap,dirpath,ensname,yr):
	slens = np.zeros(n)
	for i in range(n):
		tsipath = get_tsipath(dirpath,ensname,i,yr)
		tsifile = Dataset(tsipath)
		sltsi = tsifile['O_dsealev'][:].data[-1]
		slens[i] = slgap[i] + sltsi
		tsiyr = tsifile['time'][:].data[-1]
	return slens,tsiyr

if __name__ == '__main__':
	n = 50
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	yr = '44910'
	init_sealev = np.fromfunction(lambda i: np.random.normal(-132.8+0*i,0.00001),(n,))	
	slgap = init_slgap(n,dirpath,ensname,init_sealev,yr)
	yr = '44970'
	print(get_sldata(n,slgap,dirpath,ensname,yr))
