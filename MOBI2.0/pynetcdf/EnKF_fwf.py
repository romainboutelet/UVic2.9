#! /usr/bin/python

#This is defining the EnKF function.


import numpy as np
import scipy.sparse as sp
import scipy.linalg as lin
from FyeldGenerator import generate_field
from write_kalman import write_kalman
import numba
import os
from index_mask import index_mask
from choose_obs import choose_obs
from d13C import d13C, d13Cobs
from get_slens import get_slens
from read_files import readtempoc_tavg, readtempocobs_tavg, readtempsur_tavg, readtempsurobs_tavg, readdic_tavg, readdicobs_tavg, readdic13_tavg, readdic13obs_tavg #,readc14_tavg, readc14obs_tavg
from get_sldata import get_sldata
from get_slobs import get_slobs, get_slobsrun

#@numba.jit
def covar(x,m):
	U = x- np.transpose(np.array([m for i in range(len(x[0]))]))
	return U@np.transpose(U)/(len(x[0])-1)

#@numba.jit
def crossvar(x,y,mp,mu):
	U = x - np.transpose(np.array([mp for i in range(len(x[0]))]))
	V = np.transpose(y) - np.array([mu for i in range(len(y[0]))])
	return U@V/(len(x[0])-1)


def hd13(dic13,dic):
	rc13std = 0.0112372
	d13c = (dic13/(dic-dic13)/rc13std - 1)*1000
	return d13c

def hsl(fwf,runstep):	
	surf_water = 361.9*1e6 
	vol_water = 1e6*fwf*3600*24*365*runstep/1e9
	slrise = 1000*vol_water/surf_water
	return np.array(slrise)



def EnKFfwf(Q,R,randamp,slstart,n,dirpath,ensname,datadir,runname,yr,agerel,runstep,step,tavgint,tavgfile):

	mask_tempoc, mask_tempsur, mask_c14, mask_d13c = index_mask(dirpath,ensname)

	masktavg_tempoc = mask_tempoc[:,1:-1,1:-1]	 
	masktavg_tempsur = mask_tempsur[1:-1,1:-1]
	masktavg_c14 = mask_c14[:,1:-1,1:-1]	 
	masktavg_d13c = mask_d13c[:,1:-1,1:-1]	    #converting the mask over restart.nc   								     files to a mask over tavg.nc files
	masktavgens_tempoc = np.array([masktavg_tempoc for i in range(n)])
	masktavgens_tempsur = np.array([masktavg_tempsur for i in range(n)])
#	masktavgens_c14 = np.array([masktavg_c14 for i in range(n)])
	masktavgens_d13c = np.array([masktavg_d13c for i in range(n)])
	
	ltempoc, ltempsur, lc14, ld13, lsealev = choose_obs(dirpath,ensname, agerel,runstep)     			#Lists of attributes of observations   ( [[names of cores],[age],
		#[ageerr],[values]] except for lsealev : [indexes] )++


	#nsl = len(lsealev[0])
	#slobs = np.zeros(nsl)
	#slerr = np.zeros(nsl)
	#for i in range(nsl):
		#slobs = np.array(lsealev[2])
		#slerr = np.array(lsealev[1])
	#slmag = lsealev[3]
	

	hist = np.load(dirpath + '/fwf_hist.npz')

	#slens, tsiyr = get_sldata(n,dirpath,ensname,str(int(yr)-runstep))
	slens = np.array(hist['sealev'][:,-1,-1])
	slens.shape = (n,1)
	slens = np.transpose(slens)
	slmag = 0.1
	sldiffens = np.array(hist['sealev'][:,-1,-1]-hist['sealev'][:,-2,-1])
	sldiffens.shape = (n,1)
	sldiffens = np.transpose(sldiffens)


	fwf = np.array(hist['trend'][:,-1,:] + hist['stoch'][:,-1,:] + hist['kal'][:,-1,:])
	fwfmean = np.mean(fwf,axis = 1)
	fwfinit = np.array(hist['trend'][:,-1,-1] + hist['kal'][:,-1,-1] + hist['stoch'][:,-1,-1])
	fwfmean.shape = (n,1)
	fwfinit.shape = (n,1)
	fwfmean=np.transpose(fwfmean)
	fwfinit = np.array(np.transpose(fwfinit))

	tempocens = readtempoc_tavg(n,dirpath,ensname,yr,runstep,tavgint)
	tempocens = tempocens[masktavgens_tempoc]
	tempocens.shape = (n,len(tempocens)//n)
	tempocens = np.transpose(tempocens)

	tempsurens = readtempsur_tavg(n,dirpath,ensname,yr,runstep,tavgint)
	tempsurens = tempsurens[masktavgens_tempsur]
	tempsurens.shape = (n,len(tempsurens)//n)
	tempsurens = np.transpose(tempsurens)

#	c14ens = readc14_tavg(n,dirpath,ensname,yr,runstep,tavgint)
#	c14ens = c14ens[masktavgens_c14]
#	c14ens.shape = (n,len(c14ens)//n)
#	c14ens = np.transpose(c14ens)

	#dicens = readdic_tavg(n,dirpath,ensname,yr,runstep,tavgint)
	#dicens = dicens[masktavgens_d13c]
	#dicens.shape = (n,len(dicens)//n)
	#dicens = np.transpose(dicens)

	#dic13ens = readdic13_tavg(n,dirpath,ensname,yr,runstep,tavgint)
	#dic13ens = dic13ens[masktavgens_d13c]
	#dic13ens.shape = (n,len(dic13ens)//n)
	#dic13ens = np.transpose(dic13ens)

	
	linvar = [fwfinit]
	x = np.transpose(np.array([[] for i in range(n)]))
	print(x)

	for i in linvar:
		x = np.concatenate((x,i),axis = 0)

	linmod = []
	xmod = np.transpose(np.array([[] for i in range(n)]))

	for i in linmod:
		xmod = np.concatenate((xmod,i),axis = 0)


	diagcovQ = np.array([])
	diagcovQ = np.concatenate((diagcovQ,np.array([randamp for i in range(len(fwfinit))])),axis = 0)
	#diagcovQ = np.concatenate((diagcovQ,np.array([0.5*Q for i in range(len(slens))])),axis = 0)
	#diagcovQ = np.concatenate((diagcovQ,np.array([0.05*Q for i in range(len(tempocens))])),axis = 0)
	#diagcovQ = np.concatenate((diagcovQ,np.array([0.75*Q for i in range(len(tempsurens))])),axis = 0)
	#diagcovQ = np.concatenate((diagcovQ,np.array([0.005*Q for i in range(len(dicens))])),axis = 0)
	#diagcovQ = np.concatenate((diagcovQ,np.array([0.00005*Q for i in range(len(dic13ens))])),axis = 0)


	#can find a way to optimize how to construct diagcovQ-R

	covQ=np.diag(diagcovQ)**2


	#slobs = get_slobsrun(dirpath,datadir,int(yr))  #5800YR

	fwfobs = np.array([0.075,0.15,0.15,0.15,0.125,0.075,0.025,0.,0.,0.])
	sltraj = np.array([slstart])
	for i in range(len(fwfobs)-1):	
		sltraj = np.concatenate((sltraj,np.array([sltraj[-1] + hsl(fwfobs[i],runstep)])),axis = 0)
	slobs = np.array([sltraj[step]])
	slerr = np.array([0.5*R])
	sldiffobs = np.array([sltraj[step]-sltraj[step-1]])
	sldifferr = np.array([0.5*R*0.5])

	tempocobs = readtempocobs_tavg(dirpath,datadir,yr,tavgfile)
	tempocobs = tempocobs[masktavg_tempoc]

	tempsurobs = readtempsurobs_tavg(dirpath,datadir,yr,tavgfile)
	tempsurobs = tempsurobs[masktavg_tempsur]

#	c14obs = readc14obs_tavg(dirpath,datadir,yr,tavgfile)
#	c14obs = c14obs[masktavg_c14]

	#dicobs = readdicobs_tavg(dirpath,datadir,yr,tavgfile)
	#dicobs = dicobs[masktavg_d13c]

	#dic13obs = readdic13obs_tavg(dirpath,datadir,yr,tavgfile)
	#dic13obs = dic13obs[masktavg_d13c]
	
	#d13cobs = hd13(dic13obs,dicobs)
	

	lobs = [slobs,sldiffobs]
	xobs = np.transpose(np.array([]))
	for i in lobs:
		xobs = np.concatenate((xobs,i),axis = 0)

	diagcovR = np.array([])
	diagcovR = np.concatenate((diagcovR,slerr),axis=0)
	diagcovR = np.concatenate((diagcovR,sldifferr),axis=0)
	#diagcovR = np.concatenate((diagcovR,np.array([0.2*R for i in range(len(tempocobs))])),axis=0)
	#diagcovR = np.concatenate((diagcovR,np.array([0.2*R for i in range(len(tempsurobs))])),axis=0)
	#diagcovR = np.concatenate((diagcovR,np.array([0.005*R for i in range(len(d13cobs))])),axis=0)

	covR=np.diag(diagcovR)**2

	randR = np.sqrt(covR)@np.fromfunction(lambda i,j: np.random.normal(0*i*j,1),(len(diagcovR),n))



	#x = x + randQ
	mp=np.mean(x,axis=1)

	P = covar(x,mp)

	#Update
#	xm = x

	#fwfrand = randQ[0]
	
	#tempocens= tempocens + 0.05*Q*np.fromfunction(lambda i,j: np.random.normal(0*i*j,1),tempocens.shape)
	#tempsurens = tempsurens + 0.75*Q*np.fromfunction(lambda i,j: np.random.normal(0*i*j,1),tempsurens.shape)
	#dic13ens = dic13ens + 0.00005*Q*np.fromfunction(lambda i,j: np.random.normal(0*i*j,1),dic13ens.shape)
	#dicens = dicens + 0.005*Q*np.fromfunction(lambda i,j: np.random.normal(0*i*j,1),dicens.shape)

	#d13cens = hd13(dic13ens,dicens)

	xm = np.array([[] for i in range(n)])
	xm.shape = (0,n)
	xm = np.concatenate((xm,slens),axis = 0)
	xm = np.concatenate((xm,sldiffens), axis = 0)
	#xm = np.concatenate((xm,tempocens),axis=0)
	#xm = np.concatenate((xm,tempsurens),axis=0)
	#xm = np.concatenate((xm,c14ens),axis=0)
	#xm = np.concatenate((xm,d13cens),axis=0)
	
	mu = np.mean(xm,axis=1)
	Pu = covar(xm,mu)

	diaginfl = np.array([])
	diaginfl = np.concatenate((diaginfl,slerr/2.5),axis=0)
	diaginfl = np.concatenate((diaginfl,[0]),axis=0)
	diaginfl = np.concatenate((diaginfl,np.array([0.2*R for i in range(len(tempocobs))])),axis=0)
	diaginfl = np.concatenate((diaginfl,np.array([0.2*R for i in range(len(tempsurobs))])),axis=0)
	#diaginfl = np.concatenate((diaginfl,np.array([0.005*R for i in range(len(d13cobs))])),axis=0)

	#infl=np.diag(diaginfl)**2

	#Pu = Pu + infl
	Pu = Pu + covR


	Puinv = np.linalg.pinv(Pu)
	C = crossvar(x,xm,mp,mu)



	#Filter

	K = C@Puinv

	#norm1b = np.sum(np.sum(np.abs(K)))
	#newK = np.copy(K)
	#newK[0,0] = 5*newK[0,0]
	#norm2b = np.sum(np.sum(np.abs(newK)))

	#K = newK*norm1b/norm2b





	y = np.transpose(np.array([xobs for i in range(n)]))-randR

	kalcorr = K@(y-xm)
	xnew = np.empty(x.shape)


	xnew = x + kalcorr

	
	fwfinit = xnew[0]

	P=P - K@(Pu +covR)@np.transpose(K)
	
	#Writing the covariance matrices and Kalman gains in a .npz file


	if os.path.exists(dirpath + '/kal_hist' + runname + '.npy'):
		hist = np.load(dirpath + '/kal_hist' + runname + '.npy',allow_pickle = True)[()]
		hist['K']['step ' + str(step)] = K
		hist['Pu']['step ' + str(step)] = Pu
		hist['C']['step ' + str(step)] = C
		hist['P']['step ' + str(step)] = P
		hist['Puinv']['step ' + str(step)] = Puinv
		hist['kalcorr']['step ' + str(step)] = kalcorr
		hist['xnew']['step ' + str(step)] = xnew
		np.save(dirpath + '/kal_hist' + runname + '.npy',hist)

	else:
		hist = {}
		hist['K'] = {}
		hist['Pu'] = {}
		hist['C'] = {}
		hist['P'] = {}
		hist['Puinv'] = {}
		hist['kalcorr'] = {}
		hist['xnew'] = {}
		hist['K']['step ' + str(step)] = K
		hist['Pu']['step ' + str(step)] = Pu
		hist['C']['step ' + str(step)] = C
		hist['P']['step ' + str(step)] = P
		hist['Puinv']['step ' + str(step)] = Puinv
		hist['kalcorr']['step ' + str(step)] = kalcorr
		hist['xnew']['step ' + str(step)] = xnew
		np.save(dirpath + '/kal_hist' + runname + '.npy',hist)

	

	return fwfinit


if __name__ == '__main__':
	from fwf_change import fwf_change
	from d13C import d13C, d13Cobs

	n = 50
	Q = 1
	R = 5
	fwf_init = 0
	slstart = -132.8
	randamp = 0.025
	startyear = 4000
	runtime = 500
	runstep = 50
	tsiint = 30                   # in days
	tavgint = 50                  # in years
	tavgfile = 'tavg.04050.01.01.nc'
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	datadir = 'data_slopedrop'
	execname = 'fwfnobio.q'
	runname = 'fwf100yrsingkalpi_amp01_r1_q5'


	agerel = 19740
	step = 9

	yr = '04450'
	init_sealev = np.fromfunction(lambda i: np.random.normal(-132.8+0*i,0.00001),(n,))	

	xnew=EnKFfwf(Q,R,randamp,slstart,n,dirpath,ensname,datadir, runname,yr, agerel, runstep,step,tavgint,tavgfile)
	print(xnew,np.mean(xnew))

