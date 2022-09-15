#! /home/romainboutelet/miniconda3/bin/python


#Write the output of the EnKF into the restartnew.nc files of each ensemble member directory

from netCDF4 import Dataset
import numpy as np
import os

sudoPassword='654987Picard'
def write_files(x,n,step,lvar0,lvar1,dirpath,ensname):
	lon0=102*102
	lon1=19*102*102
	x0=x[:,:len(lvar0)*lon0]
	x1=x[:,len(lvar0)*lon0:]
	if len(lvar0)>0:
		x0.shape=(n,len(lvar0),1,1,102,102)
	if len(lvar1)>0:
		x1.shape=(n,len(lvar1),1,19,102,102)
	file_name=[]
	newfile=[]
	for i in range(n):
		a=str(i)
		file_name.append(Dataset(dirpath + '/' + ensname + a +'/data/restart.nc' , 'r+', format='NETCDF4'))	
		newfile.append(Dataset(dirpath + '/' + ensname + a +'/data/restartnew.nc' , 'w', format='NETCDF4'))

	#Copy dimensions
		for dim in iter(file_name[i].dimensions):
			newfile[i].createDimension(dim,len(file_name[i].dimensions[dim]) if not file_name[i].dimensions[dim].isunlimited() else None)

	#Copy variables
		j0=0
		j1=0
		for var in iter(file_name[i].variables):
	
			if j0>=len(lvar0) and j1>=len(lvar1):
				outvar=newfile[i].createVariable(var,file_name[i].variables[var].datatype,file_name[i].variables[var].dimensions)
				outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})
				outvar[:]=file_name[i].variables[var][:]

			elif position(file_name[i],var) == position(file_name[i],lvar1[j1]) and j0>=len(lvar0):
				outvar=newfile[i].createVariable(var,file_name[i].variables[lvar1[j1]].datatype,file_name[i].variables[var].dimensions)
				outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})
				outvar[:]=x1[i,j1]
				j1+=1

			elif position(file_name[i],var) != position(file_name[i],lvar1[j1]) and j0>=len(lvar0):
				outvar=newfile[i].createVariable(var,file_name[i].variables[lvar1[j1]].datatype,file_name[i].variables[var].dimensions)
				outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})
				outvar[:]=file_name[i].variables[var][:]

			elif position(file_name[i],var) == position(file_name[i],lvar0[j0]):	
				outvar=newfile[i].createVariable(var,file_name[i].variables[lvar0[j0]].datatype,file_name[i].variables[var].dimensions)
				outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})
				outvar[:]=x0[i,j0]
				j0+=1


			else:	
				outvar=newfile[i].createVariable(var,file_name[i].variables[var].datatype,file_name[i].variables[var].dimensions)
				outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})
				outvar[:]=file_name[i].variables[var][:]

		file_name[i].close()
		newfile[i].close()
	b=str(step)
	print('Step '+b+' done')
	return 'Step '+b+' done'

def write_sl_files(sl,n,dirpath,ensname):
	for i in range(n):
		a=str(i)
		file_name = (Dataset(dirpath + '/' + ensname + a +'/data/restart.nc' , 'r+', format='NETCDF4'))	
		newfile = (Dataset(dirpath + '/' + ensname + a +'/data/restartnew.nc' , 'w', format='NETCDF4'))

	#Copy dimensions
		for dim in iter(file_name.dimensions):
			newfile.createDimension(dim,len(file_name.dimensions[dim]) if not file_name.dimensions[dim].isunlimited() else None)

	#Copy variables
		j0=0
		j1=0
		for var in iter(file_name.variables):
	
			if var != 'sealev':
				outvar=newfile.createVariable(var,file_name.variables[var].datatype,file_name.variables[var].dimensions)
				outvar.setncatts({k: file_name.variables[var].getncattr(k) for k in file_name.variables[var].ncattrs()})
				outvar[:]=file_name.variables[var][:]


			else:	
				outvar=newfile.createVariable(var,file_name.variables[var].datatype,file_name.variables[var].dimensions)
				outvar.setncatts({k: file_name.variables[var].getncattr(k) for k in file_name.variables[var].ncattrs()})
				outvar[:]=np.array([sl[i]])

		file_name.close()
		newfile.close()

	return 

def position(file_name,var1):
	i=0
	for var in iter(file_name.variables):
		if var == var1:
			return i
		i+=1
	return('Cannot find'+ var)
			

