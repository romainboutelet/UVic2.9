#! /usr/bin/python

#


import numpy as np


def get_slens(slage,n,dirpath,agerel):
	
	slens = np.zeros((len(slage),n))
	ind_age = np.array(agerel-np.array(slage),dtype = int)
	for j in range(len(slage)):
		hist = np.load(dirpath + '/fwf_hist.npz')
		slens[j] = hist['sealev'][:,-1,-ind_age[j]-1]

	return slens

if __name__ == '__main__':	
	slage = [36524,36528]
	agerel = 36520
	n = 50
	dirpath = '../ens_50fwfnb200yr'
	slens = get_slens(slage,n,dirpath,agerel)
	print(slens)
