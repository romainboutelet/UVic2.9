#! /home/romainboutelet/miniconda3/bin/python

import os 
import time
import pandas as pd
import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from write_control import write_runobs_control
from fwf_file import fwf_obsfile


def hsl(fwf,runstep):	
	surf_water = 361.9*1e6 
	vol_water = 1e6*fwf*3600*24*365*runstep/1e9
	slrise = 1000*vol_water/surf_water
	return np.array(slrise)

def addobs_sldata(dirpath,ensname,execname,inityear,tsiint,tavgint,tsifile):

	ageobs = np.array([4000,4050,4200,4350,4500])
	fwfobs = np.array([0.,0.15,0.15,0.,0.])
	fwfrate = (fwfobs[1:]-fwfobs[:-1])/(ageobs[1:]-ageobs[:-1])

	infile = Dataset(dirpath + '/' + ensname + '/' + tsifile)
	lon = len(infile['time'][:].data)
	runlen = int(ageobs[-1]-ageobs[0])
	fwfout = np.zeros(lon)
	f = interp1d(ageobs,fwfobs)
	x = infile['time'][:].data
	for i in x:
		fwfout[(infile['time'][:].data>=i)*(infile['time'][:].data<(i+1))] = f(i)
	print('done')
	outfile = Dataset(dirpath + '/' + ensname + '/' + tsifile,'r+')
	outvar1=outfile.createVariable('fwfflx','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Freshwater input at tau'})
	outvar1[:]=fwfout
	outfile.close()


	slout = np.array([-132.8])
	for i in range(len(fwfout)-1):	
		slout = np.concatenate((slout,np.array([slout[-1] + hsl(fwfout[i],runlen/lon)])),axis = 0)


	outfile = Dataset(dirpath + '/' + ensname + '/' + tsifile,'r+')
	outvar1=outfile.createVariable('sealev','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Sea level at tau'})
	outvar1[:]=slout
	outfile.close()
	
	return('fini')

def addobs_2sldata(dirpath,ensname,execname,inityear,tsiint,tavgint,tsifile):

	ageobs = np.array([4000,4200,4350,4600,4700,4850,4900,5050,5300,5350,5400,5500,5600,5800,5850,6000,6050,6100,6150,6300,6400,6500,6750,6800,6950,7000])
	fwfobs1 = np.array([0.0,0.03,0.08,0.12,0.02,0.04,0.05,0.09,0.01,0.00,0.02,0.06,0.09,0.08,0.01,0.11,0.10,0.09,0.11,0.1,0.02,0.05,0.11,0.02,0.03,0.02])
	fwfrate1 = (fwfobs1[1:]-fwfobs1[:-1])/(age[1:]-age[:-1])
	fwfobs2 = np.array([0.00,0.01,0.02,0.04,0.005,0.,0.03,0.06,0.09,0.08,0.07,0.09,0.10,0.12,0.09,0.06,0.06,0.05,0.06,0.08,0.05,0.03,0.02,0.04,0.03,0.05])
	fwfrate2 = (fwfobs2[1:]-fwfobs2[:-1])/(age[1:]-age[:-1])

	infile = Dataset(dirpath + '/' + ensname + '/' + tsifile)
	lon = len(infile['time'][:].data)
	runlen = int(ageobs[-1]-ageobs[0])
	fwfout1 = np.zeros(lon)
	fwfout2 = np.zeros(lon)
	f1 = interp1d(ageobs,fwfobs1)
	f2 = interp1d(ageobs,fwfobs2)
	x = infile['time'][:].data
	for i in x:
		fwfout1[(infile['time'][:].data>=i)*(infile['time'][:].data<(i+1))] = f1(i)
		fwfout2[(infile['time'][:].data>=i)*(infile['time'][:].data<(i+1))] = f2(i)
	print('done')
	outfile = Dataset(dirpath + '/' + ensname + '/' + tsifile,'r+')
	outvar1=outfile.createVariable('fwfflx1','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Freshwater input in North Atlantic Ocean at tau'})
	outvar1[:]=fwfout1
	outfile.close()
	
	outfile = Dataset(dirpath + '/' + ensname + '/' + tsifile,'r+')
	outvar1=outfile.createVariable('fwfflx2','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Freshwater input in Southern Ocean at tau'})
	outvar1[:]=fwfout2
	outfile.close()
	
	cumul1out = np.array([0.])
	for i in range(len(fwfout1)-1):	
		cumul1out = np.concatenate((cumul1out,np.array([cumul1out[-1] + hsl(fwfout1[i],runlen/lon)])),axis = 0)
	
	outfile = Dataset(dirpath + '/' + ensname + '/' + tsifile,'r+')
	outvar1=outfile.createVariable('cumul1','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Cumulative freshwater input in the North Atlantic at tau'})
	outvar1[:]=cumul1out
	outfile.close()
	
	cumul2out = np.array([0.])
	for i in range(len(fwfout2)-1):	
		cumul2out = np.concatenate((cumul2out,np.array([cumul2out[-1] + hsl(fwfout2[i],runlen/lon)])),axis = 0)
	
	outfile = Dataset(dirpath + '/' + ensname + '/' + tsifile,'r+')
	outvar1=outfile.createVariable('cumul2','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Cumulative freshwater input in the Southern Ocean at tau'})
	outvar1[:]=cumul2out
	outfile.close()
	

	fwfout = fwfout1 + fwfout2
	slout = np.array([-132.8])
	for i in range(len(fwfout)-1):	
		slout = np.concatenate((slout,np.array([slout[-1] + hsl(fwfout[i],runlen/lon)])),axis = 0)


	outfile = Dataset(dirpath + '/' + ensname + '/' + tsifile,'r+')
	outvar1=outfile.createVariable('sealev','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Sea level at tau'})
	outvar1[:]=slout
	outfile.close()
	
	return('fini')
	

#if __name__ == '__main__':
inityear = 4000
tsiint = 30
tavgint = 30
dirpath = '../ensbis_50fwfnb200yr'
ensname = 'target_3000yr'
execname = 'fwfnobio.q'
tsifile = 'tsi3000yr.nc'
addobs_2sldata(dirpath,ensname,execname,inityear,tsiint,tavgint,tsifile)
