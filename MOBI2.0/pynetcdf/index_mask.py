#! /usr/bin/python

import numpy as np

#These functions take the data from dictionaries collecting information about the goegraphical positions of the observations locations and produce masks in the form of arrays to be used in the 'EnKF_(2)fwf.py' file. More particularly the dictionaries have the variables 'lonind', 'latind', 'depind' that are the closest grid points from the real-world observations locations.

def index_mask(dirpath,ensname):

	temp_sur_mask = np.ones((100,100), dtype = 'int')
	tempsur_dico = np.load(dirpath + '/temp_data_nature10915.npy', allow_pickle= True)
	tempsur_data = tempsur_dico[()]

	ind = np.zeros((2,len(tempsur_data['lonind'])),dtype = 'int')
	ind[0] = tempsur_data['lonind']
	ind[1] = tempsur_data['latind']
	for i in range(len(tempsur_data['lonind'])):
		temp_sur_mask[ind[1,i],ind[0,i]] = 0

	
	rad_mask = np.ones((19,102,102),dtype = 'int')
	rad_dico = np.load(dirpath + '/rad_data.npy', allow_pickle = True)
	rad_data = rad_dico[()]

	for cle in rad_data:
		for var in rad_data[cle]:
			if var == 'lonind':
				xind = rad_data[cle][var]
			if var == 'latind':
				yind = rad_data[cle][var]
			if var == 'depind':
				zind = rad_data[cle][var]
		rad_mask[zind,yind,xind] = 0
	
	d13_mask = np.ones((19,102,102), dtype = 'int')
	d13_dico = np.load(dirpath + '/d13_data.npy', allow_pickle = True)
	d13_data = d13_dico[()]

	for cle in d13_data:
		for var in d13_data[cle]:
			if var == 'lonind':
				xind = d13_data[cle][var]
			if var == 'latind':
				yind = d13_data[cle][var]
			if var == 'depind':
				zind = d13_data[cle][var]
		d13_mask[zind,yind,xind] = 0

	return (temp_sur_mask == 0), (rad_mask == 0), (d13_mask == 0)
	
if __name__ == '__main__':
	ensname = ''
	dirpath = '../../../../Documents/Stage'
	ind, oui, non = index_mask(dirpath,ensname)
	print(np.sum(ind))
	ind_loc = np.zeros((100,100,2))
	for i in range(100):
		for j in range(100):
			if ind[i,j] == 1:
				ind_loc[i,j] = np.array([i,j])
	print(ind_loc[ind])
