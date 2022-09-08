import numpy as np
from netCDF4 import Dataset
from index_mask import index_mask

def rmse(n,dirpath,ensname,runname,tavgobs,istempsur,isc14,isd13c):

	tavgobs_file = Dataset(dirpath + '/' + tavgobs)
	ltime = len(tavgobs_file['time'][:])
	mask_tempsur, mask_c14, mask_d13c = index_mask(dirpath,ensname)
	
	
	if istempsur:
		masktavg_tempsur = mask_tempsur[:,:]
		ltempsur = np.sum(masktavg_tempsur*1)
		tempsur = np.zeros((n,ltime,ltempsur))
		tempsurobs = np.zeros((ltime,ltempsur))
		for j in range(ltime):
			tempsurobs[j] = tavgobs_file['A_sat'][j].data[masktavg_tempsur]

		for i in range(n):
			tavgensfile = Dataset(dirpath +'/' + ensname + str(i) + '/tavg' + runname + '.nc')
			for j in range(ltime):
				tempsur[i,j] = tavgensfile['A_sat'][j].data[masktavg_tempsur]
			tavgensfile.close()
		sqerrtempsur = (tempsur - np.array([tempsurobs for i in range(n)]))**2
		rmse_tempsur = np.sqrt(np.mean(sqerrtempsur,axis = 2))
		rmse_tempsur = np.mean(rmse_tempsur,axis = 0)
		
		stdtempsur = np.std(tempsur,axis = 0)
		stdtempsur = np.mean(stdtempsur, axis = 1)
		
		mae_tempsur = np.mean(np.mean(np.abs(tempsur - np.array([tempsurobs for i in range(n)])),axis = 2),axis = 0)
		
		infile = Dataset(dirpath + '/tsi' + runname + 'stat.nc')
		tsitime = infile['time'][:].data
		tavgens_file = Dataset(dirpath +'/' + ensname + '0/tavg' + runname + '.nc')
		tavgtime = tavgens_file['time'][:].data
		
		tsi_stdtempsur = np.zeros(len(tsitime))
		tsi_stdtempsur[:len(tsitime[tsitime<tavgtime[0]])] = stdtempsur[0]
		tsi_rmsetempsur = np.zeros(len(tsitime))
		tsi_rmsetempsur[:len(tsitime[tsitime<tavgtime[0]])] = rmse_tempsur[0]
		tsi_maetempsur = np.zeros(len(tsitime))
		tsi_maetempsur[:len(tsitime[tsitime<tavgtime[0]])] = mae_tempsur[0]
		
		for i in range(ltime-1):
			tsi_stdtempsur[len(tsitime[tsitime<tavgtime[i]]):len(tsitime[tsitime<tavgtime[i+1]])] = stdtempsur[i+1]
			tsi_rmsetempsur[len(tsitime[tsitime<tavgtime[i]]):len(tsitime[tsitime<tavgtime[i+1]])] = rmse_tempsur[i+1]
			tsi_maetempsur[len(tsitime[tsitime<tavgtime[i]]):len(tsitime[tsitime<tavgtime[i+1]])] = mae_tempsur[i+1]
			
		outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
		outvar2=outfile.createVariable('avstd_tempsur','float64',('time'))
		outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average over the observations locations of the standard deviation of surface temperature  at tau'})
		outvar2[:]=np.array(tsi_stdtempsur)
		outfile.close()

		outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
		outvar2=outfile.createVariable('rmse_tempsur','float64',('time'))
		outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Mean over the ensemble members of the RMSE of surface temperature at the observations locations at tau'})
		outvar2[:]=np.array(tsi_rmsetempsur)
		outfile.close()
		
		outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
		outvar2=outfile.createVariable('mae_tempsur','float64',('time'))
		outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Mean over the ensemble members of the MAE of surface temperature at the observations locations at tau'})
		outvar2[:]=np.array(tsi_maetempsur)
		outfile.close()
	
	
	if isc14:
		masktavg_c14 = mask_c14[:,1:-1,1:-1]	 

	
	if isd13c:
		masktavg_d13c = mask_d13c[:,1:-1,1:-1]
		ld13c = np.sum(masktavg_d13c*1)
		dic = np.zeros((n,ltime,ld13c))
		dicobs = np.zeros((ltime,ld13c))
		dic13 = np.zeros((n,ltime,ld13c))
		dic13obs = np.zeros((ltime,ld13c))
		for j in range(ltime):
			dic13obs[j] = tavgobs_file['O_dic13'][j].data[masktavg_d13c]
			dicobs[j] = tavgobs_file['O_dic'][j].data[masktavg_d13c]
			
		for i in range(n):
			tavgensfile = Dataset(dirpath +'/' + ensname + str(i) + '/tavg' + runname + '.nc')
			for j in range(ltime):
				dic[i,j] = tavgensfile['O_dic'][j].data[masktavg_d13c]
				dic13[i,j] = tavgensfile['O_dic13'][j].data[masktavg_d13c]
			tavgensfile.close()
		sqerrdic = (dic - np.array([dicobs for i in range(n)]))**2
		rmse_dic = np.sqrt(np.mean(sqerrdic,axis = 0))
		rmse_dic = np.mean(rmse_dic,axis = 1)

		sqerrdic13 = (dic13 - np.array([dic13obs for i in range(n)]))**2
		rmse_dic13 = np.sqrt(np.mean(sqerrdic13,axis = 0))
		rmse_dic13 = np.mean(rmse_dic13,axis = 1)
		
		stddic13 = np.std(dic13,axis = 0)
		stddic13 = np.mean(stddic13, axis = 1)

		stddic = np.std(dic,axis = 0)
		stddic = np.mean(stddic, axis = 1)
		
		infile = Dataset(dirpath + '/tsi' + runname + 'stat.nc')
		tsitime = infile['time'][:].data
		tavgtime = tavgobs_file['time'][:].data
	
		tsi_stddic = np.zeros(len(tsitime))
		tsi_stddic13 = np.zeros(len(tsitime))
		tsi_stddic[:len(tsitime[tsitime<tavgtime[0]])] = stddic[0]
		tsi_stddic13[:len(tsitime[tsitime<tavgtime[0]])] = stddic13[0]
		tsi_rmsedic = np.zeros(len(tsitime))
		tsi_rmsedic13 = np.zeros(len(tsitime))
		tsi_rmsedic[:len(tsitime[tsitime<tavgtime[0]])] = rmse_dic[0]
		tsi_rmsedic13[:len(tsitime[tsitime<tavgtime[0]])] = rmse_dic13[0]
		
		for i in range(ltime-1):
			tsi_stddic[len(tsitime[tsitime<tavgtime[i]]):len(tsitime[tsitime<tavgtime[i+1]])] = stddic[i+1]
			tsi_stddic13[len(tsitime[tsitime<tavgtime[i]]):len(tsitime[tsitime<tavgtime[i+1]])] = stddic13[i+1]
			tsi_rmsedic[len(tsitime[tsitime<tavgtime[i]]):len(tsitime[tsitime<tavgtime[i+1]])] = rmse_dic[i+1]
			tsi_rmsedic13[len(tsitime[tsitime<tavgtime[i]]):len(tsitime[tsitime<tavgtime[i+1]])] = rmse_dic13[i+1]
		

		outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
		outvar2=outfile.createVariable('avstd_dic','float64',('time'))
		outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard deviation of ensemble members for DIC at the observations locations at tau'})
		outvar2[:]=np.array(tsi_stddic)
		outfile.close()

		outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
		outvar2=outfile.createVariable('avstd_dic13','float64',('time'))
		outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard deviation of ensemble members for DIC13 at the observations locations at tau'})
		outvar2[:]=np.array(tsi_stddic13)
		outfile.close()

		outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
		outvar2=outfile.createVariable('avste_dic','float64',('time'))
		outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error to observations of ensemble members for DIC at the observations locations at tau'})
		outvar2[:]=np.array(tsi_rmsedic)
		outfile.close()

		outfile = Dataset(dirpath + '/tsi' + runname + 'stat.nc','r+',format = 'NETCDF4')
		outvar2=outfile.createVariable('avste_dic13','float64',('time'))
		outvar2.setncatts({'valid_range': np.array([-1.e+20,  1.e+20]), 'FillValue': 9.969209968386869e+36, 'missing_value': 9.969209968386869e+36, 'long_name': 'Average of standard error to observations of ensemble members for DIC13 at the observations locations at tau'})
		outvar2[:]=np.array(tsi_rmsedic13)
		outfile.close()
	
	
	return

if __name__ == '__main__':
	n = 50
	dirpath = '../ensbis_50fwfnb200yr'
	ensname = 'ens_fwfnb200yr'
	tavgobs = 'data_slopedrop/tavg.04050.01.01.nc'
	runname = '2bisfwf2_2infl0.1kalpi500yr_r5_q1_tavgint_50runstep50slopeslsigma10tempsigma2'
	istempsur = True
	isc14 = False
	isd13c = False
	rmse(n,dirpath,ensname,runname,tavgobs,istempsur,isc14,isd13c)
