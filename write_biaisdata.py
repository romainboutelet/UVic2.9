#! /home/romainboutelet/miniconda3/bin/python

from netCDF4 import Dataset
import numpy as np
import os

def position(file_name,var1):
	i=0
	for var in iter(file_name.variables):
		if var == var1:
			return i
		i+=1
	return('Cannot find'+ var)

def noise(var,lvar0,lvar1,covR):
	if var in lvar0:
		ind=lvar0.index(var)
	elif var in lvar1:
		ind=lvar1.index(var)
	else:
		return ('the variable is not in the list given')
	return covR[ind]
	
def biais(dev,var):
	if var=='temp1' or var =='temp2':
		return dev
	else:
		return 0
	
lvar0=[]
lvar1=[]          #list of variables used in the Kalman Filter (1st sublist is for atmosheric components, 2nd sublist is for oceanic components)

lvar1.append('temp')
lvar1.append('salt')
lvar1.append('dic')
lvar1.append('dic13')
lvar1.append('c14')
#lvar1.append('alk1')
#lvar1.append('alk2')
#lvar1.append('o21')
#lvar1.append('o22')
#lvar1.append('po41')
#lvar1.append('po42')
#lvar1.append('phyt1')
#lvar1.append('phyt2')
#lvar1.append('zoop1')
#lvar1.append('zoop2')
#lvar1.append('detr1')
#lvar1.append('detr2')
#lvar1.append('cocc1')
#lvar1.append('cocc2')
#lvar1.append('caco31')
#lvar1.append('caco32')
#lvar1.append('dop1')
#lvar1.append('dop2')
#lvar1.append('no31')
#lvar1.append('no32')
#lvar1.append('don1')
#lvar1.append('don2')
#lvar1.append('diaz1')
#lvar1.append('diaz2')
#lvar1.append('din151')
#lvar1.append('din152')
#lvar1.append('don151')
#lvar1.append('don152')
#lvar1.append('phytn151')
#lvar1.append('phytn152')
#lvar1.append('coccn151')
#lvar1.append('coccn152')
#lvar1.append('zoopn151')
#lvar1.append('zoopn152')
#lvar1.append('detrn151')
#lvar1.append('detrn152')
#lvar1.append('diazn151')
#lvar1.append('diazn152')
#lvar1.append('dfe1')
#lvar1.append('dfe2')
#lvar1.append('detrfe1')
#lvar1.append('detrfe2')
#lvar1.append('phytc131')
#lvar1.append('phytc132')
#lvar1.append('coccc131')
#lvar1.append('coccc132')
#lvar1.append('caco3c131')
#lvar1.append('caco3c132')
#lvar1.append('zoopc131')
#lvar1.append('zoopc132')
#lvar1.append('detrc131')
#lvar1.append('detrc132')
#lvar1.append('doc131')
#lvar1.append('doc132')
#lvar1.append('diazc131')
#lvar1.append('diazc132')
#lvar1.append('u1')
#lvar1.append('u2')
#lvar1.append('v1')
#lvar1.append('v2')

n=20
dirname='ens_50lgm20yr'
dataname='data_lgm20yr'
lon0=102*102
lon1=19*102*102
R=0.5
covR=np.array([3e-1,5e-6,6e-3,6e-5,4e-15])*R
file_name=[]
newfile=[]
dev = 0.
for i in range(20):
	yr=str(44903+i)
	file_name.append(Dataset('../'+dirname+'/'+dataname+'/rest.'+yr+'.01.01.nc' , 'r+', format='NETCDF4'))	
	newfile.append(Dataset('../'+dirname+'/data05tbiais_lgm20yr/rest.'+yr+'.01.01.nc' , 'w', format='NETCDF4'))

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

		elif position(file_name[i],var) == position(file_name[i],lvar1[j1]+'1') and j0>=len(lvar0):
			outvar=newfile[i].createVariable(var,file_name[i].variables[lvar1[j1]+'1'].datatype,file_name[i].variables[var].dimensions)

			outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})

			outvar[:]=(file_name[i][lvar1[j1]+'1'][:]!=0)*(file_name[i][lvar1[j1]+'1'][:]+np.fromfunction(lambda i,j,k,l:np.random.normal(0*i*j*k*l+biais(dev,var),noise(lvar1[j1],lvar0,lvar1,covR)),file_name[i][lvar1[j1]+'1'][:].shape))

		elif position(file_name[i],var) == position(file_name[i],lvar1[j1]+'2') and j0>=len(lvar0):
			outvar=newfile[i].createVariable(var,file_name[i].variables[lvar1[j1]+'2'].datatype,file_name[i].variables[var].dimensions)

			outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})

			outvar[:]=newfile[i][lvar1[j1]+'1'][:] + file_name[i][lvar1[j1]+'2'][:] - file_name[i][lvar1[j1]+'1'][:]

			j1=j1+1

		elif position(file_name[i],var) != position(file_name[i],lvar1[j1]+'1') and j0>= len(lvar0):
			outvar=newfile[i].createVariable(var,file_name[i].variables[var].datatype,file_name[i].variables[var].dimensions)
			outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})
			outvar[:]=file_name[i].variables[var][:]

		elif position(file_name[i],var) == position(file_name[i],lvar0[j0]+'1'):	
			outvar=newfile[i].createVariable(var,file_name[i].variables[lvar0[j0]+'1'].datatype,file_name[i].variables[var].dimensions)
			outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})
			outvar[:]=(file_name[i][lvar0[j0]+'1'][:]!=0)*(file_name[i][lvar0[j0]+'1'][:]+np.fromfunction(lambda i,j,k,l:np.random.normal(0*i*j*k*l+biais(dev,var),noise(lvar0[j0],lvar0,lvar1,covR)),file_name[i][lvar0[j0]+'1'][:].shape))

		elif position(file_name[i],var) == position(file_name[i],lvar0[j0]+'2'):
			outvar=newfile[i].createVariable(var,file_name[i].variables[lvar0[j0]+'2'].datatype,file_name[i].variables[var].dimensions)

			outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})

			outvar[:]=newfile[i][lvar0[j0]+'1'][:] + file_name[i][lvar0[j0]+'2'][:] - file_name[i][lvar0[j0]+'1'][:]

			j0=j0+1


		else:	
			outvar=newfile[i].createVariable(var,file_name[i].variables[var].datatype,file_name[i].variables[var].dimensions)
			outvar.setncatts({k: file_name[i].variables[var].getncattr(k) for k in file_name[i].variables[var].ncattrs()})
			outvar[:]=file_name[i].variables[var][:]

	file_name[i].close()
	newfile[i].close()


			

