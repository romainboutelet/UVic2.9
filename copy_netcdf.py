#! /usr/bin/env python3

from netCDF4 import Dataset
import numpy as np
import os
import cProfile

sudoPassword='654987Picard'
def write_files(x,n,step):
	#x.shape=(n,2,1,19,102,102)
	file_name=[]
	newfile=[]
	for z in range(13):
		for i in range(n):
			a=str(i)
			file_name.append(Dataset('../test_nc'+a+'/data/restart.nc' , 'r+', format='NETCDF4'))	
			newfile.append(Dataset('../test_nc'+a+'/data/restartnew.nc' , 'w', format='NETCDF4'))

		#Copy dimensions
			for dim in iter(file_name[i].dimensions):
				newfile[i].createDimension(dim,len(file_name[i].dimensions[dim]) if not file_name[i].dimensions[dim].isunlimited() else None)

		#Copy variables
			for var in iter(file_name[i].variables):
				if position(file_name[i],var) != position(file_name[i],'temp1') and position(file_name[i],var) != position(file_name[i],'temp2'):	
					outvar=newfile[i].createVariable(var,file_name[i].variables[var].datatype,file_name[i].variables[var].dimensions)
					outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})
					outvar[:]=file_name[i].variables[var][:]
			file_name[i].close()
			newfile[i].close()
	b=str(step)
	return 'Step '+b+' done'

def position(file_name,var1):
	i=0
	for var in iter(file_name.variables):
		if var == var1:
			return i
		i+=1
	return('Cannot find'+ var)

cProfile.run('write_files(0,4,1)','copystats')

