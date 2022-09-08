#! /usr/bin/python

#This is defining the EnKF function.


import numpy as np
import scipy.sparse as sp
import scipy.linalg as lin
from scipy.interpolate import interp1d
from FyeldGenerator import generate_field
from write_kalman import write_kalman
import numba
import os
from index_mask import index_mask
from choose_obs import choose_obs
from d13C import d13C, d13Cobs
from get_slens import get_slens
from read_files import readtempsur_tavg, readtempsurobs_tavg, readdic_tavg, readdicobs_tavg, readdic13_tavg, readdic13obs_tavg #,readc14_tavg, readc14obs_tavg
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



def EnKF2fwf(tempsigma,slsigma,randamp1,randamp2,slstart,n,dirpath,ensname,datadir,runname,yr,agerel,runstep,step,tavgint,tavgfile):

	masktavg_tempsur, mask_c14, mask_d13c = index_mask(dirpath,ensname) 

	masktavg_c14 = mask_c14	 
	masktavg_d13c = mask_d13c	    #converting the mask over restart.nc   								     files to a mask over tavg.nc files
	masktavgens_tempsur = np.array([masktavg_tempsur for i in range(n)])
	#masktavgens_c14 = np.array([masktavg_c14 for i in range(n)])
	#masktavgens_d13c = np.array([masktavg_d13c for i in range(n)])
	
	#ltempsur, lc14, ld13, lsealev = choose_obs(dirpath,ensname, agerel,runstep)     			#Lists of attributes of observations   ( [[names of cores],[age],
		#[ageerr],[values]] except for lsealev : [indexes] )++




	hist = np.load(dirpath + '/fwf_hist.npz')

	#slens, tsiyr = get_sldata(n,dirpath,ensname,str(int(yr)-runstep))
	
	# We here give the write the observations that we used for the target run
	slens = np.array(hist['sealev'][:,-1,-1])
	slens.shape = (n,1)
	slens = np.transpose(slens)
	if step == 1:
		sldiffens = np.array(hist['sealev'][:,-1,-1]-hist['sealev'][:,-2,-1])
	else:
		sldiffens = np.array(hist['sealev'][:,-1,-1]-hist['sealev'][:,-3,-1])
	sldiffens.shape = (n,1)
	sldiffens = np.transpose(sldiffens)

	fwf1 = np.array(hist['trend1'][:,-1,:] + hist['stoch1'][:,-1,:] + hist['kal1'][:,-1,:])
	fwfmean1 = np.mean(fwf1,axis = 1)
	fwfinit1 = np.array(hist['trend1'][:,-1,-1] + hist['kal1'][:,-1,-1] + hist['stoch1'][:,-1,-1])
	fwfmean1.shape = (n,1)
	fwfinit1.shape = (n,1)
	fwfmean1=np.transpose(fwfmean1)
	fwfinit1 = np.array(np.transpose(fwfinit1))

	fwf2 = np.array(hist['trend2'][:,-1,:] + hist['stoch2'][:,-1,:] + hist['kal2'][:,-1,:])
	fwfmean2 = np.mean(fwf2,axis = 1)
	fwfinit2 = np.array(hist['trend2'][:,-1,-1] + hist['kal2'][:,-1,-1] + hist['stoch2'][:,-1,-1])
	fwfmean2.shape = (n,1)
	fwfinit2.shape = (n,1)
	fwfmean2=np.transpose(fwfmean2)
	fwfinit2 = np.array(np.transpose(fwfinit2))
	
	
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

	
	linvar = [fwfinit1,fwfinit2]
	x = np.transpose(np.array([[] for i in range(n)]))

	for i in linvar:
		x = np.concatenate((x,i),axis = 0)

	linmod = []
	xmod = np.transpose(np.array([[] for i in range(n)]))

	for i in linmod:
		xmod = np.concatenate((xmod,i),axis = 0)


	diagcovQ = np.array([])
	diagcovQ = np.concatenate((diagcovQ,np.array([randamp1 for i in range(len(fwfinit1))])),axis = 0)
	diagcovQ = np.concatenate((diagcovQ,np.array([randamp2 for i in range(len(fwfinit2))])),axis = 0)
	#diagcovQ = np.concatenate((diagcovQ,np.array([slsigma for i in range(len(slens))])),axis = 0)
	#diagcovQ = np.concatenate((diagcovQ,np.array([tempsigma for i in range(len(tempsurens))])),axis = 0)
	#diagcovQ = np.concatenate((diagcovQ,np.array([dicsigma for i in range(len(dicens))])),axis = 0)
	#diagcovQ = np.concatenate((diagcovQ,np.array([dic13sigma for i in range(len(dic13ens))])),axis = 0)


	#can find a way to optimize how to construct diagcovQ-R

	covQ=np.diag(diagcovQ)**2


	#slobs = get_slobsrun(dirpath,datadir,int(yr))  #5800YR

	fwfobs1 = np.array([0.075,0.15,0.15,0.125,0.075,0.025,0.,0.,0.,0.])
	fwfobs2 = np.array([0.,0.,0.,0.025,0.075,0.125,0.075,0.,0.,0])
	#fwf1 = np.array([0.0,0.03,0.08,0.12,0.02,0.04,0.05,0.09,0.01,0.00,0.02,0.06,0.09,0.08,0.01,0.11,0.10,0.09,0.11,0.1,0.02,0.05,0.11,0.02,0.03,0.02])
	#fwf2 = np.array([0.00,0.01,0.02,0.04,0.005,0.,0.03,0.06,0.09,0.08,0.07,0.09,0.10,0.12,0.09,0.06,0.06,0.05,0.06,0.08,0.05,0.03,0.02,0.04,0.03,0.05])
	#age = np.array([4000,4200,4350,4600,4700,4850,4900,5050,5300,5350,5400,5500,5600,5800,5850,6000,6050,6100,6150,6300,6400,6500,6750,6800,6950,7000])
	#f1 = interp1d(age,fwf1)
	#fwfobs1 = (f1(np.arange(4000,7050,50))[1:]+f1(np.arange(4000,7050,50))[:-1])/2	
	#f2 = interp1d(age,fwf2)
	#fwfobs2 = (f2(np.arange(4000,7050,50))[1:]+f2(np.arange(4000,7050,50))[:-1])/2
	
	sltraj = np.array([slstart])
	for i in range(len(fwfobs1)-1):	
		sltraj = np.concatenate((sltraj,np.array([sltraj[-1] + hsl(fwfobs1[i],50) + hsl(fwfobs2[i],50)])),axis = 0)
	slobs = np.array([sltraj[step]])
	if step == 1:
		sldiffobs = np.array([sltraj[step]-sltraj[step-1]])
	else:
		sldiffobs = np.array([sltraj[step]-sltraj[step-2]])
	sldifferr = np.array([2*slsigma])

	tempsurobs = readtempsurobs_tavg(dirpath,datadir,yr,tavgfile)
	tempsurobs = tempsurobs[masktavg_tempsur]

#	c14obs = readc14obs_tavg(dirpath,datadir,yr,tavgfile)
#	c14obs = c14obs[masktavg_c14]

	#dicobs = readdicobs_tavg(dirpath,datadir,yr,tavgfile)
	#dicobs = dicobs[masktavg_d13c]

	#dic13obs = readdic13obs_tavg(dirpath,datadir,yr,tavgfile)
	#dic13obs = dic13obs[masktavg_d13c]
	
	#d13cobs = hd13(dic13obs,dicobs)
	

	lobs = [slobs,tempsurobs]
	xobs = np.transpose(np.array([]))
	for i in lobs:
		xobs = np.concatenate((xobs,i),axis = 0)

	diagcovR = np.array([])
	diagcovR = np.concatenate((diagcovR,np.array([slsigma])),axis=0)
	#diagcovR = np.concatenate((diagcovR,sldifferr),axis=0)
	diagcovR = np.concatenate((diagcovR,np.array([tempsigma for i in range(len(tempsurobs))])),axis=0)
	#diagcovR = np.concatenate((diagcovR,np.array([d13sigma for i in range(len(d13cobs))])),axis=0)

	covR=np.diag(diagcovR)**2

	randR = np.sqrt(covR)@np.fromfunction(lambda i,j: np.random.normal(0*i*j,1),(len(diagcovR),n))



	#x = x + randQ
	mp=np.mean(x,axis=1)

	P = covar(x,mp)

	#Update

	#d13cens = hd13(dic13ens,dicens)

	xm = np.array([[] for i in range(n)])
	xm.shape = (0,n)
	xm = np.concatenate((xm,slens),axis=0)
	#xm = np.concatenate((xm,sldiffens),axis=0)
	xm = np.concatenate((xm,tempsurens),axis=0)
	#xm = np.concatenate((xm,c14ens),axis=0)
	#xm = np.concatenate((xm,d13cens),axis=0)
	
	mu = np.mean(xm,axis=1)
	Pu = covar(xm,mu)

	diaginfl = np.array([])
	diaginfl = np.concatenate((diaginfl,np.array([slsigma*0])),axis=0)
	#diaginfl = np.concatenate((diaginfl,np.array([slsigma*2/10])),axis=0)
	diaginfl = np.concatenate((diaginfl,np.array([tempsigma/5 for i in range(len(tempsurobs))])),axis=0)
	#diaginfl = np.concatenate((diaginfl,np.array([0.005*R for i in range(len(d13cobs))])),axis=0)

	infl=np.diag(diaginfl)**2


	Pu = Pu + infl


	Puinv = np.linalg.pinv(Pu)
	C = crossvar(x,xm,mp,mu)



	#Filter

	K = C@Puinv


	y = np.transpose(np.array([xobs for i in range(n)]))-randR

	kalcorr = K@(y-xm)
	xnew = np.empty(x.shape)


	xnew = x + kalcorr

	
	fwfinit1 = xnew[0]
	fwfinit2 = xnew[1]

	P=P - K@(Pu +covR)@np.transpose(K)
	
	#Writing the covariance matrices and Kalman gains in a .npy file


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


	

	return fwfinit1,fwfinit2


if __name__ == '__main__':

	n = 50
	tempsigma = 1
	slsigma = 5
	fwf_init1 = 0
	fwf_init2 = 0
	randamp1 = 0.1
	randamp2 = 0.1
	slstart = -132.8
	startyear = 4000
	runtime = 500
	runstep = 50
	tsiint = 30                   # in days
	tavgint = 50                  # in years
	tavgfile = 'tavg.04050.01.01.nc'
	dirpath = '../ensbis_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	datadir = 'data_slopedrop'
	execname = 'fwfnobio.q'
	runname = '2fwf1_1infl0.1kalpi3000yr_r5_q1_tavgint_50runstep50slopeslsigma5tempsigma1'



	agerel = 19740
	step = 1

	yr = '04050'

	fwfinit1, fwfinit2 =	EnKF2fwf(tempsigma,slsigma,randamp1,randamp2,slstart,n,dirpath,ensname,datadir,runname,yr,agerel,runstep,step,tavgint,tavgfile)
	print(fwfinit1,np.mean(fwfinit1),fwfinit2,np.mean(fwfinit2))

