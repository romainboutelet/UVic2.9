#! /usr/bin/python

import numpy as np
import os
from netCDF4 import Dataset


def d13C(n,dirpath,ensname):
	lon1=19*102*102
	rc13std = 0.0112372
	dicens=np.zeros((n,19,102,102))
	dic13ens = np.zeros((n,19,102,102))
	for i in range(n):
		rest=Dataset(dirpath + '/' + ensname + str(i) + '/data/restart.nc','r')
		dic13=rest['dic131'][:].data
		dic=rest['dic1'][:].data
		dic13.shape = (19,102,102)
		dic.shape = (19,102,102)
		dicens[i] = dic
		dic13ens[i] = dic13

	return dicens,dic13ens

def d13Cobs(dirpath,datadir,year):
	lon1=19*102*102
	rc13std = 0.0112372
	d13c=np.zeros(lon1)
	rest=Dataset(dirpath + '/' + datadir  + '/rest.' + year +'.01.01.nc','r')
	dic13=rest['dic131'][:].data
	dic=rest['dic1'][:].data

	dic13.shape=lon1
	dic.shape=lon1
	mask = (dic13 != 0)
	d13c[mask]=(dic13[mask]/(dic[mask]-dic13[mask])/rc13std-1)*1000	
	d13c.shape=(19,102,102)
	return d13c



if __name__=='__main__':
	dirpath = '../ens_50lgm20yr'
	ensname = 'ens_lgm20yr'
	n=1
	a=d13C(n,dirpath,ensname)
	print(np.mean(a!=0))
		

