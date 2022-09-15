#! /home/romainboutelet/miniconda3/bin/python

from netCDF4 import Dataset
import numpy as np
import os
from scipy import stats



def merge_stats(n,dirpath,ensname,runname):
	infile = Dataset(dirpath + '/' + ensname + '0/tsi' + runname + '.nc')
	lon = len(infile['fwfflx'][:].data)
	shape = infile['O_temp'][:].data.shape
	mask = infile['O_temp'][:].data < 5e36
	ensmask = np.array([mask for i in range(n)])
	fwfflx = np.zeros((n,lon))
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		fwfflx[i] = infile['fwfflx'][:].data
	std = np.std(fwfflx,axis = 0)

	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+')
	outvar1=outfile.createVariable('std_fwfflx','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'standard error of ensemble members for freshwater flux input at tau'})
	outvar1[:]=std
	outfile.close()

	sl = np.array([np.zeros(shape) for i in range (n)])
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		sl[i] = infile['sealev'][:].data
	slmsk = sl[ensmask]
	slmsk.shape = ((n,shape[0]))
	mean = np.mean(slmsk,axis = 0)
	print(mean,mean.shape)
	std = np.std(slmsk,axis = 0)	
	print(std,std.shape)


	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar2=outfile.createVariable('std_sealev','float64',('time'))
	outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error of ensemble members for sea level at tau'})
	outvar2[:]=np.array(std)
	outfile.close()

	motmax = np.array([np.zeros(shape) for i in range (n)])
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		motmax[i] = infile['O_motmax'][:].data
	motmaxmsk = motmax[ensmask]
	motmaxmsk.shape = ((n,shape[0]))
	mean = np.mean(motmaxmsk,axis = 0)
	print(mean,mean.shape)
	std = np.std(motmaxmsk,axis = 0)	
	print(std,std.shape)


	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar2=outfile.createVariable('avstd_motmax','float64',('time'))
	outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error of ensemble members for mean maximum MOC at tau'})
	outvar2[:]=np.array(std)
	outfile.close()
	
	return

def merge_2stats(n,dirpath,ensname,runname):
	infile = Dataset(dirpath + '/' + ensname + '0/tsi' + runname + '.nc')
	lon = len(infile['fwfflx1'][:].data)
	shape = infile['O_temp'][:].data.shape
	mask = infile['O_temp'][:].data < 5e36
	ensmask = np.array([mask for i in range(n)])
	
	
	fwfflx1 = np.zeros((n,lon))
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		fwfflx1[i] = infile['fwfflx1'][:].data
	std = np.std(fwfflx1,axis = 0)

	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+')
	outvar1=outfile.createVariable('std_fwfflx1','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'standard error of ensemble members for freshwater flux input in North Atlantic Ocean at tau'})
	outvar1[:]=std
	outfile.close()
	
	fwfflx2 = np.zeros((n,lon))
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		fwfflx2[i] = infile['fwfflx2'][:].data
	std = np.std(fwfflx2,axis = 0)

	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+')
	outvar1=outfile.createVariable('std_fwfflx2','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'standard error of ensemble members for freshwater flux input in Southern Ocean at tau'})
	outvar1[:]=std
	outfile.close()

	sl = np.array([np.zeros(shape) for i in range (n)])
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		sl[i] = infile['sealev'][:].data
	slmsk = sl[ensmask]
	slmsk.shape = ((n,shape[0]))
	mean = np.mean(slmsk,axis = 0)
	print(mean,mean.shape)
	std = np.std(slmsk,axis = 0)	
	print(std,std.shape)


	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar2=outfile.createVariable('std_sealev','float64',('time'))
	outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error of ensemble members for sea level at tau'})
	outvar2[:]=np.array(std)
	outfile.close()

	cumul1 = np.array([np.zeros(shape) for i in range (n)])
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		cumul1[i] = infile['cumul1'][:].data
	cumul1msk = cumul1[ensmask]
	cumul1msk.shape = ((n,shape[0]))
	mean = np.mean(cumul1msk,axis = 0)
	print(mean,mean.shape)
	std = np.std(cumul1msk,axis = 0)	
	print(std,std.shape)


	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar2=outfile.createVariable('std_cumul1','float64',('time'))
	outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error of ensemble members for cumulative Freshwater input in the North Atlantic at tau'})
	outvar2[:]=np.array(std)
	outfile.close()
	
	cumul2 = np.array([np.zeros(shape) for i in range (n)])
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		cumul2[i] = infile['cumul2'][:].data
	cumul2msk = cumul2[ensmask]
	cumul2msk.shape = ((n,shape[0]))
	mean = np.mean(cumul2msk,axis = 0)
	print(mean,mean.shape)
	std = np.std(cumul2msk,axis = 0)	
	print(std,std.shape)


	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar2=outfile.createVariable('std_cumul2','float64',('time'))
	outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error of ensemble members for cumulative Freshwater input in the Southern Ocean at tau'})
	outvar2[:]=np.array(std)
	outfile.close()
	
	motmax = np.array([np.zeros(shape) for i in range (n)])
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		motmax[i] = infile['O_motmax'][:].data
	motmaxmsk = motmax[ensmask]
	motmaxmsk.shape = ((n,shape[0]))
	mean = np.mean(motmaxmsk,axis = 0)
	print(mean,mean.shape)
	std = np.std(motmaxmsk,axis = 0)	
	print(std,std.shape)


	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar2=outfile.createVariable('avstd_motmax','float64',('time'))
	outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error of ensemble members for mean maximum MOC at tau'})
	outvar2[:]=np.array(std)
	outfile.close()
	
	return


def merge_nofwf_stats(n,dirpath,ensname,runname):
	infile = Dataset(dirpath + '/' + ensname + '0/tsi' + runname + '.nc')
	shape = infile['O_temp'][:].data.shape
	mask = infile['O_temp'][:].data < 5e36
	ensmask = np.array([mask for i in range(n)])
	temp = np.array([np.zeros(shape) for i in range (n)])
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		temp[i] = infile['O_temp'][:].data
	tempmsk = temp[ensmask]
	tempmsk.shape = ((n,shape[0]))
	mean = np.mean(tempmsk,axis = 0)
	print(mean,mean.shape)
	std = np.std(tempmsk,axis = 0)	
	print(std,std.shape)


	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar1=outfile.createVariable('avstd_temp','float64',('time'))
	outvar1.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error of ensemble members for ocean temperature at tau'})
	outvar1[:]=np.array(std)
	outfile.close()

	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar1b=outfile.createVariable('av_temp','float64',('time'))
	outvar1b.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average ensemble members for ocean temperature at tau'})
	outvar1b[:]=np.array(mean)
	outfile.close()

	sal = np.array([np.zeros(shape) for i in range (n)])
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		sal[i] = infile['O_sal'][:].data
	salmsk = sal[ensmask]
	salmsk.shape = ((n,shape[0]))
	mean = np.mean(salmsk,axis = 0)
	print(mean,mean.shape)
	std = np.std(salmsk,axis = 0)	
	print(std,std.shape)


	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar2=outfile.createVariable('avstd_sal','float64',('time'))
	outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error of ensemble members for mean ocean salinity at tau'})
	outvar2[:]=np.array(std)
	outfile.close()

	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar2b=outfile.createVariable('av_sal','float64',('time'))
	outvar2b.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average ensemble members for ocean salinity at tau'})
	outvar2b[:]=np.array(mean)
	outfile.close()
	
	motmax = np.array([np.zeros(shape) for i in range (n)])
	for i in range(n):
		infile = Dataset(dirpath + '/' + ensname + str(i) + '/tsi' + runname + '.nc')
		motmax[i] = infile['O_motmax'][:].data
	motmaxmsk = motmax[ensmask]
	motmaxmsk.shape = ((n,shape[0]))
	mean = np.mean(motmaxmsk,axis = 0)
	print(mean,mean.shape)
	std = np.std(motmaxmsk,axis = 0)	
	print(std,std.shape)


	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar3=outfile.createVariable('avstd_motmax','float64',('time'))
	outvar3.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error of ensemble members for the maximum of the MOC at tau'})
	outvar3[:]=np.array(std)
	outfile.close()

	outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
	outvar3b=outfile.createVariable('av_motmax','float64',('time'))
	outvar3b.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average ensemble members for the maximum of the MOC at tau'})
	outvar3b[:]=np.array(mean)
	outfile.close()

	return
	
if __name__ == '__main__':
	#n=50
	#dirpath = '../ens_50fwfnb200yr'
	#ensname = 'ens_fwfnb200yr'
	#runname = 'fwf100yrdicsltkalpi_amp01_r25_q1targ'
	#merge_stats(n,dirpath,ensname,runname)

	n=50
	runname = 'fwf_diff0.025kalpi500yr_r5_q1_tavgint50slopeall'
	dirpath = '../ens_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	merge_stats(n,dirpath,ensname,runname)
