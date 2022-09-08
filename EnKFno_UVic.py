#! /usr/bin/python

#This is defining the EnKF function.


import numpy as np
import scipy.sparse as sp
import scipy.linalg as lin
from FyeldGenerator import generate_field
import numba
from write_kalman import write_kalman

#@numba.jit
def Pkgen(n):
    def Pk(k):
        return np.power(k, -n)

    return Pk

#Draw samples from a normal distribution
@numba.jit
def distrib(shape):
    a = np.random.normal(loc=0, scale=1, size=shape)
    b = np.random.normal(loc=0, scale=1, size=shape)
    return a + 1j * b

@numba.jit
def construct_cov(Q,R,lvar0,lvar1):
	
	list=['temp1','salt1','dic1','dic131','c141','alk1','o21','po41','phyt1','zoop1'\
,'detr1','cocc1','caco31','dop1','no31','don1','diaz1','din151','don151'\
,'phytn151','coccn151','zoopn151','detrn151','diazn151','dfe1','detrfe1','phytc131'\
,'coccc131','caco3c131','zoopc131','detrc131','doc131','diazc131','u1','v1']
	orders=[1e0,1e-5,1e-1,1e-3,1e-13,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,\
0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1,0e1]
	cov=np.empty(len(lvar1))
	ind=0
	for a in lvar1:
		cov[ind]=orders[list.index(a)]
		ind+=1
	return cov

@numba.jit
def covar(x,m):
	l=len(x)
	diag=np.zeros(len(m))
	for i in range(l):
		for j in range(len(m)):
			diag[j]+=(x[i,j]-m[j])**2
	return diag/(l-1)

@numba.jit
def crossvar(x,y,mp,mu):
	l=len(x)
	lm=min(len(mp),len(mu))
	diag=np.zeros(lm)
	for i in range(l):
		for k in range(lm):
			diag[k]+=(x[i,k]-mp[k])*(y[i,k]-mu[k])
	return diag/(l-1)


def EnKFhome(xold,y,Q,R,n,lvar0,lvar1,dirpath,ensname):
	l1=len(lvar1)
	lon1=19*102*102
	x=np.empty((n,int(len(xold[0])/2)))
	covQ=np.empty(x[0].shape)
	covR=np.empty(x[0].shape)
	cov=np.array([1e0,1e-5,1e-1,1e-3,1e-13])
	for i in range(int(l1/2)):
		x[:,i*lon1:(i+1)*lon1]=xold[:,2*i*lon1:(2*i+1)*lon1]
		covQ[i*lon1:(i+1)*lon1]=cov[i]*Q
		covR[i*lon1:(i+1)*lon1]=cov[i]*R

	lilmask=np.array(x[0]!=0)
	lmask=np.sum(lilmask*1)
	mask=np.array(x!=0)

	diff=np.empty(x.shape)
	for i in range(int(l1/2)):
		diff[:,i*lon1:(i+1)*lon1]=xold[:,(2*i+1)*lon1:(2*i+2)*lon1]-xold[:,2*i*lon1:(2*i+1)*lon1]

	randQ=np.empty((n,int(l1/2),19,102,102))
	randR=np.empty((n,int(l1/2),19,102,102))
	shape=(19,102,102)
	for i in range(n):
		for j in range(len(randQ[0])):
			randQ[i][j]=generate_field(distrib,Pkgen(2),shape)
			randQ[i][j]=randQ[i][j]/np.sqrt(np.mean(randQ[i][j]**2))*cov[j]*Q
			randR[i][j]=generate_field(distrib,Pkgen(2),shape)
			randR[i][j]=randR[i][j]/np.sqrt(np.mean(randR[i][j]**2))*cov[j]*R
	randQ.shape=(n,int(l1/2)*lon1)
	randR.shape=(n,int(l1/2)*lon1)
	
	x[mask] = x[mask] + randQ[mask]
	mp = np.mean(x,axis=0)
	P = covar(x,mp) 

	#Update
	xm=np.array(x)
	mu=np.mean(xm,axis=0)
	Pu=covar(xm,mu) 
	Pu = Pu + covR**2
	C=crossvar(x,xm,mp,mu)
	#Filter

	K=np.empty(P.shape)
	K = P/Pu
	K[np.isnan(K)]=0.

	ytr = np.empty(x[0].shape)
	for i in range(int(l1/2)):
		ytr[i*lon1:(i+1)*lon1]=y[2*i*lon1:(2*i+1)*lon1]
	ybis = np.array([ytr for i in range(n)])
	#x[mask] = x[mask] + (ybis[mask]-xm[mask])*np.array([K for i in range(n)])[mask]
	
	x[mask]=x[mask]+randR[mask]*np.array([K for i in range(n)])[mask]
	
	xnew=np.zeros(xold.shape)
	for i in range(int(l1/2)):
		xnew[:,2*i*lon1:(2*i+1)*lon1]=x[:,i*lon1:(i+1)*lon1]
		xnew[:,(2*i+1)*lon1:(2*i+2)*lon1]=xnew[:,2*i*lon1:(2*i+1)*lon1]+diff[:,i*lon1:(i+1)*lon1]

	P=P - K*(P + covQ**2 +covR**2)*K
	write_kalman(P,n,lvar0,lvar1,dirpath,ensname)
	return xnew


