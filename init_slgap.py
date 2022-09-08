#! /home/romainboutelet/miniconda3/bin/python



from netCDF4 import Dataset
import numpy as np
import os
from get_tsiname import get_tsipath

def init_slgap(n,dirpath,ensname,init_sealev,yr):
	slgap = np.zeros((n))
	for i in range(n):
		tsipath = get_tsipath(dirpath,ensname,i,yr)
		tsifile = Dataset(tsipath)
		slgap[i] = init_sealev[i] - tsifile['O_dsealev'][:].data[0]
		
		tsifile.close()
	return slgap
		
if __name__ == '__main__':
	n = 50
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	yr = '44920'
	init_sealev = np.fromfunction(lambda i: np.random.normal(-132.8+0*i,0.00001),(n,))	
	print(init_sealev)
	print(init_slgap(n,dirpath,ensname,init_sealev,yr))
