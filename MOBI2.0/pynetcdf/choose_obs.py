#! /usr/bin/python

#This is defining the EnKF function.


import numpy as np


def choose_obs(dirpath,ensname, agerel,runstep):
	tempsur_dico = np.load(dirpath + '/tempsur_data.npy', allow_pickle= True)
	tempsur_data = tempsur_dico[()]
	rad_dico = np.load(dirpath + '/rad_data.npy', allow_pickle= True)
	rad_data = rad_dico[()]
	d13_dico = np.load(dirpath + '/d13_data.npy', allow_pickle= True)
	d13_data = d13_dico[()]
	sealev_dico = np.load(dirpath + '/sealev_data.npy', allow_pickle= True)
	sealev_data = sealev_dico[()]

	
	ltempsur = [[],[],[],[]]

	for cle in tempsur_data:
		lage = tempsur_data[cle]['age'][((agerel-runstep) < tempsur_data[cle]['age'])*(tempsur_data[cle]['age'] <= agerel)]
		lageerr = tempsur_data[cle]['ageerr'][((agerel-runstep) < tempsur_data[cle]['age'])*(tempsur_data[cle]['age'] <= agerel)]
		lval = tempsur_data[cle]['temp'][((agerel-runstep) < tempsur_data[cle]['age'])*(tempsur_data[cle]['age'] <= agerel)]
		for i in range(len(lage)):
			ltempsur[0].append(cle)
			ltempsur[1].append(lage[i])
			ltempsur[2].append(lageerr[i])
			ltempsur[3].append(lval[i])

	lrad = [[],[],[],[]]

	for cle in rad_data:
		lage = rad_data[cle]['age'][((agerel-runstep) < np.array(rad_data[cle]['age']))*(np.array(rad_data[cle]['age']) <= agerel)]
		lageerr = rad_data[cle]['ageerr'][((agerel-runstep) < rad_data[cle]['age'])*(rad_data[cle]['age'] <= agerel)]
		lval = rad_data[cle]['d14C'][((agerel-runstep) < rad_data[cle]['age'])*(rad_data[cle]['age'] <= agerel)]
		for i in range(len(lage)):
			lrad[0].append(cle)
			lrad[1].append(lage[i])
			lrad[2].append(lageerr[i])
			lrad[3].append(lval[i])

	ld13 = [[],[],[],[]]
	
	for cle in d13_data:
		lage = d13_data[cle]['age'][((agerel-runstep) < d13_data[cle]['age'])*(d13_data[cle]['age'] <= agerel)]
		lageerr = d13_data[cle]['ageerr'][((agerel-runstep) < d13_data[cle]['age'])*(d13_data[cle]['age'] <= agerel)]
		for i in range(len(lage)):
			ld13[0].append(cle)
			ld13[1].append(lage[i])
			ld13[2].append(lageerr[i])


	lsealev = [[],[],[],[]]

	lage = sealev_data['age'][((agerel-runstep) < sealev_data['age'])*(sealev_data['age'] <= agerel)]
	lvalerr = sealev_data['slerr'][((agerel-runstep) < sealev_data['age'])*(sealev_data['age'] <= agerel)]
	lval = sealev_data['sl'][((agerel-runstep) < sealev_data['age'])*(sealev_data['age'] <= agerel)]
	for i in range(len(lage)):
		lsealev[0].append(lage[i])
		lsealev[1].append(lvalerr[i])
		lsealev[2].append(lval[i])
	lsealev[3] = sealev_data['mag']

	return ltempoc, ltempsur, lrad, ld13, lsealev

if __name__ == '__main__':	
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	agerel = 19755
	runstep = 100
	choose_obs(dirpath,ensname,agerel,runstep)
