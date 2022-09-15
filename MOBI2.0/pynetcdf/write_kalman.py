
from netCDF4 import Dataset
import numpy as np
import os
import time


def write_kalman(P,n,lvar0,lvar1,dirpath,ensname):
	lon0=102*102
	lon1=19*102*102
	lvar0=lvar0[::2]
	lvar1=lvar1[::2]
	P0=np.array(P[:len(lvar0)*lon0])
	P1=np.array(P[len(lvar0)*lon0:])
	if len(lvar0)>0:
		P0.shape=(len(lvar0),1,1,102,102)
	if len(lvar1)>0:
		P1.shape=(len(lvar1),1,19,102,102)

	if not os.path.exists(dirpath +'/kalman.nc'):	
		rest=Dataset(dirpath + '/' + ensname + '0/data/restart.nc' , 'r+', format='NETCDF4')	
		kalnew=Dataset(dirpath + '/kalman.nc' , 'w', format='NETCDF4')
		
		#Copy dimensions
		for dim in iter(rest.dimensions):
			kalnew.createDimension(dim,len(rest.dimensions[dim]) if not rest.dimensions[dim].isunlimited() else None)


		j0=0
		j1=0
		for var in iter(rest.variables):
			
			if j0>=len(lvar0) and j1>=len(lvar1):
                                break


			elif position(rest,var) == position(rest,lvar1[j1]) and j0>=len(lvar0):
				outvar=kalnew.createVariable(var+'Kvar',rest.variables[lvar1[j1]].datatype,rest.variables[var].dimensions)
				outvar.setncatts({k: rest.variables[var].getncattr(k) for k in rest.variables[var].ncattrs()})
				outvar[:]=P1[j1]
				j1+=1

			elif j0<len(lvar0):
				if position(rest,var) == position(rest,lvar0[j0]):	
					outvar=kalnew.createVariable(var + 'Kvar',rest.variables[lvar0[j0]].datatype,rest.variables[var].dimensions)
					outvar.setncatts({k: rest.variables[var].getncattr(k) for k in rest.variables[var].ncattrs()})
					outvar[:]=P0[j0]
					j0+=1

		kalnew.close()
		rest.close()

		
	else:
		rest=Dataset(dirpath + '/' + ensname + '0/data/restart.nc' , 'r+', format='NETCDF4')
		kalnew=Dataset(dirpath + '/kalmannew.nc','w')

		#Copy dimensions
		for dim in iter(rest.dimensions):
			kalnew.createDimension(dim,len(rest.dimensions[dim]) if not rest.dimensions[dim].isunlimited() else None)


		j0=0
		j1=0
		for var in iter(rest.variables):
			
			if j0>=len(lvar0) and j1>=len(lvar1):
                                break


			elif position(rest,var) == position(rest,lvar1[j1]) and j0>=len(lvar0):
				outvar=kalnew.createVariable(var+'Kvar',rest.variables[lvar1[j1]].datatype,rest.variables[var].dimensions)
				outvar.setncatts({k: rest.variables[var].getncattr(k) for k in rest.variables[var].ncattrs()})
				outvar[:]=P1[j1]
				j1+=1

			elif j0<len(lvar0):
				if position(rest,var) == position(rest,lvar0[j0]):	
					outvar=kalnew.createVariable(var + 'Kvar',rest.variables[lvar0[j0]].datatype,rest.variables[var].dimensions)
					outvar.setncatts({k: rest.variables[var].getncattr(k) for k in rest.variables[var].ncattrs()})
					outvar[:]=P0[j0]
					j0+=1

		kalnew.close()
		rest.close()
		os.system('ncrcat -h ' + dirpath + '/kalman.nc ' + dirpath + '/kalmannew.nc ' + dirpath + '/kalmanb.nc')

		os.system('mv ' + dirpath + '/kalmanb.nc ' + dirpath + '/kalman.nc')



def position(file_name,var1):
	i=0
	for var in iter(file_name.variables):
		if var == var1:
			return i
		i+=1
	return('Cannot find'+ var)

