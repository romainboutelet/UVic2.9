#! /home/romainboutelet/miniconda3/bin/python

#Get the data from the restart.nc or tavg.$date.nc files of each ensemble member directory 

from netCDF4 import Dataset
import numpy as np
import os
from string_yr import string_yr


def read_files(n,lvar0,lvar1,dirpath,ensname):
	lon0=1*1*102*102
	lon1=1*19*102*102
	file_name=[]
	xnew=np.empty((n,len(lvar0)*lon0+len(lvar1)*lon1))
	for i in range(n):
		a=str(i)		
		file_name.append(Dataset(dirpath + '/' + ensname + a +'/data/restart.nc' , 'r+', format='NETCDF4'))
		
		
		gen0=(lvar0[j] for j in range(len(lvar0)))
		xold0=np.array([file_name[i][j][:].data for j in gen0])
		xold0.shape=len(lvar0)*lon0
		gen1=(lvar1[j] for j in range(len(lvar1)))
		xold1=np.array([file_name[i][j][:].data for j in gen1])
		xold1.shape=len(lvar1)*lon1
		file_name[i].close()

		xnew[i][:len(lvar0)*lon0]=xold0
		xnew[i][len(lvar0)*lon0:]=xold1

	xnew.shape=(n,len(lvar0)*lon0 + len(lvar1)*lon1)

	return xnew
	

def read_data(yr,lvar0,lvar1,dirpath,datadir):
	file_name=Dataset(dirpath + "/" + datadir + "/rest."+yr+".01.01.nc" , 'r+', format='NETCDF4')

	lon0=1*1*102*102
	gen0=(lvar0[j] for j in range(len(lvar0)))
	x0=np.array([file_name[j][:].data for j in gen0])
	x0.shape=len(lvar0)*lon0
	lon1=1*19*102*102
	gen1=(lvar1[j] for j in range(len(lvar1)))
	x1=np.array([file_name[j][:].data for j in gen1])
	x1.shape=len(lvar1)*lon1
	file_name.close()
	x=np.concatenate((x0,x1))

	return x

def readtempsur_tavg(n,dirpath,ensname,yr,runstep,tavgint):
	yr = int(yr)
	year = string_yr(yr-runstep+tavgint)
	temp = np.zeros((n,100,100))
	for i in range(n):
		tavg = Dataset(dirpath + '/' + ensname + str(i) + '/tavg.' + year + '.01.01.nc')
		index = np.argmin(np.abs(tavg['time'][:].data[tavg['time'][:].data < yr]-yr))
		temptavg = np.array(tavg['O_temp'][:].data[index,0])
		temptavg.shape = (100,100)
		temp[i] = temptavg
	return temp
	
def readtempsurobs_tavg(dirpath,datadir,yr,tavgfile):
	yr = int(yr)
	tavg = Dataset(dirpath + '/' + datadir + '/' + tavgfile)
	index = np.argmin(np.abs(tavg['time'][:].data[tavg['time'][:].data < yr]-yr))
	temp = tavg['O_temp'][index,0].data
	return temp

def readc14_tavg(n,dirpath,ensname,yr,runstep,tavgint):
	yr = int(yr)
	year = string_yr(yr-runstep+tavgint)
	c14 = np.zeros((n,19,100,100))
	for i in range(n):
		tavg = Dataset(dirpath + '/' + ensname + str(i) + '/tavg.' + year + '.01.01.nc')
		index = np.argmin(np.abs(tavg['time'][:].data[tavg['time'][:].data < yr]-yr))
		c14tavg = np.array(tavg['O_c14'][:].data[index])
		c14tavg.shape = (19,100,100)
		c14[i] = c14tavg
	return c14
	
def readc14obs_tavg(dirpath,datadir,yr,tavgfile):
	yr = int(yr)
	c14 = Dataset(dirpath + '/' + datadir + '/' + tavgfile)
	index = np.argmin(np.abs(tavg['time'][:].data[tavg['time'][:].data < yr]-yr))
	c14 = tavg['O_c14'][index].data
	return c14

def readdic_tavg(n,dirpath,ensname,yr,runstep,tavgint):
	yr = int(yr)
	year = string_yr(yr-runstep+tavgint)
	dic = np.zeros((n,19,100,100))
	for i in range(n):
		tavg = Dataset(dirpath + '/' + ensname + str(i) + '/tavg.' + year + '.01.01.nc')
		index = np.argmin(np.abs(tavg['time'][:].data[tavg['time'][:].data < yr]-yr))
		dictavg = np.array(tavg['O_dic'][:].data[index])
		dictavg.shape = (19,100,100)
		dic[i] = dictavg
	return dic
	
def readdicobs_tavg(dirpath,datadir,yr,tavgfile):
	yr = int(yr)
	tavg = Dataset(dirpath + '/' + datadir + '/' + tavgfile)
	index = np.argmin(np.abs(tavg['time'][:].data[tavg['time'][:].data < yr]-yr))
	dic = tavg['O_dic'][index].data
	return dic

def readdic13_tavg(n,dirpath,ensname,yr,runstep,tavgint):
	yr = int(yr)
	year = string_yr(yr-runstep+tavgint)
	dic13 = np.zeros((n,19,100,100))
	for i in range(n):
		tavg = Dataset(dirpath + '/' + ensname + str(i) + '/tavg.' + year + '.01.01.nc')
		index = np.argmin(np.abs(tavg['time'][:].data[tavg['time'][:].data < yr]-yr))
		dic13tavg = np.array(tavg['O_dic13'][:].data[index])
		dic13tavg.shape = (19,100,100)
		dic13[i] = dic13tavg
	return dic13
	
def readdic13obs_tavg(dirpath,datadir,yr,tavgfile):
	yr = int(yr)
	tavg = Dataset(dirpath + '/' + datadir + '/' + tavgfile)
	index = np.argmin(np.abs(tavg['time'][:].data[tavg['time'][:].data < yr]-yr))
	dic13 = tavg['O_dic13'][index].data
	return dic13




