#! /home/romainboutelet/miniconda3/bin/python



from netCDF4 import Dataset
import numpy as np
import os



def get_tsipath(dirpath,ensname,i,yr):
	os.system('rm name_file')
	os.system('ls ' + dirpath + '/' + ensname + str(i) + '/tsi.' + yr + '* >> name_file')
	f = open('name_file')
	for i in f:
		tsiname = i
		break
	f.close()
	os.system('rm name_file')
	tsiname = tsiname.rstrip('\n')
	return tsiname

if __name__ == '__main__':
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	i = 25
	yr = '44920'
	print(get_tsipath(dirpath,ensname,i,yr))
