#! /home/romainboutelet/miniconda3/bin/python

import os 
import time
import numpy as np

def fwf_file(n,fwfinit,fwfrate,dirpath,ensname,year,runstep):
	hist=np.load(dirpath + '/fwf_hist.npz')
	for i in range(n):
		init=fwfinit[i] + hist['stoch'][i,-1,-1]
		rate=fwfrate[i]
		start = year 
		end = year + runstep
		line1 = "         fwaflxi=" + f"{init:.4f}," #The first line that we need to change
		line2 = "         fwayri=" + str(start) + ".,fwayrf=" + str(end) + ".,fwarate=" + f"{rate:.4f},\n"       #The first line that we need to change
		cont=open(dirpath + '/' + ensname + str(i) +'/control.in','r')
		contnew=open(dirpath + '/' + ensname + str(i) +'/controlbis.in','w')

		for line in cont:
			if 'fwaflxi' in line:
				contnew.write(line1)
			elif 'fwayri' in line:
				contnew.write(line2)
			else:
				contnew.write(line)
		cont.close()
		contnew.close()
		os.system('mv ' + dirpath + '/' + ensname + str(i) + '/controlbis.in ' + dirpath + '/' + ensname + str(i) +'/control.in')


	return 

def fwf_2file(n,fwfinit1,fwfinit2,fwfrate,dirpath,ensname,year,runstep):
	hist=np.load(dirpath + '/fwf_hist.npz')
	for i in range(n):
		init1=fwfinit1[i] + hist['stoch1'][i,-1,-1]
		init2=fwfinit2[i] + hist['stoch2'][i,-1,-1]
		rate=fwfrate[i]
		start = year 
		end = year + runstep
		flx1 = "         fwaflxi1=" + f"{init1:.4f},fwayri1=" + str(start) + ".,fwayrf1=" + str(end) + ".,fwarate1=" + f"{rate:.4f}" + ",\n"       #The first line that we need to change
		flx2 = "         fwaflxi2=" + f"{init2:.4f},fwayri2=" + str(start) + ".,fwayrf2=" + str(end) + ".,fwarate2=" + f"{rate:.4f}" + ",\n"       #The first line that we need to change
		cont=open(dirpath + '/' + ensname + str(i) +'/control.in','r')
		contnew=open(dirpath + '/' + ensname + str(i) +'/controlbis.in','w')

		for line in cont:
			if 'fwaflxi1' in line:
				contnew.write(flx1)
			elif 'fwaflxi2' in line:
				contnew.write(flx2)
			else:
				contnew.write(line)
		cont.close()
		contnew.close()
		os.system('mv ' + dirpath + '/' + ensname + str(i) + '/controlbis.in ' + dirpath + '/' + ensname + str(i) +'/control.in')


	return 

def fwf_obsfile(fwfinit,fwfrate,dirpath,ensname,year,runstep):

	init=fwfinit
	rate=fwfrate
	flx1 = "         fwaflxi=" + f"{init:.4f}" + ",\n"       #The first line that we need to change
	start = year 
	end = year + runstep
	flx2 = "         fwayri=" + str(start) + "., fwayrf=" + str(end) + "., fwarate=" + f"{rate:.4f}" + ",\n"       #The second line that we need to change
	cont=open(dirpath + '/' + ensname +'/control.in','r')
	contnew=open(dirpath + '/' + ensname +'/controlbis.in','w')

	for line in cont:
		if 'fwaflxi' in line:
			contnew.write(flx1)
		elif 'fwayri' in line:
			contnew.write(flx2)
		else:
			contnew.write(line)
	cont.close()
	contnew.close()
	os.system('mv ' + dirpath + '/' + ensname + '/controlbis.in ' + dirpath + '/' + ensname + '/control.in')


	return 
	
def fwf_2obsfile(fwfinit1,fwfinit2,fwfrate1,fwfrate2,dirpath,ensname,year,runstep):

	start = year 
	end = year + runstep

	flx1 = "         fwaflxi1=" + f"{fwfinit1:.4f},fwayri1=" + str(start) + ".,fwayrf1=" + str(end) + ".,fwarate1=" + f"{fwfrate1:.4f}" + ",\n"       #The first line that we need to change
	flx2 = "         fwaflxi2=" + f"{fwfinit2:.4f},fwayri2=" + str(start) + ".,fwayrf2=" + str(end) + ".,fwarate2=" + f"{fwfrate2:.4f}" + ",\n"       #The first line that we need to change
	cont=open(dirpath + '/' + ensname +'/control.in','r')
	contnew=open(dirpath + '/' + ensname +'/controlbis.in','w')

	for line in cont:
		if 'fwaflxi1' in line:
			contnew.write(flx1)
		elif 'fwaflxi2' in line:
			contnew.write(flx2)
		else:
			contnew.write(line)
	cont.close()
	contnew.close()
	os.system('mv ' + dirpath + '/' + ensname + '/controlbis.in ' + dirpath + '/' + ensname +'/control.in')


	return 
	
if __name__ == '__main__':
	n = 50
	fwfinit1 = np.array([i/100 for i in range(50)])
	fwfinit2 = np.array([i/200 for i in range(50)])
	fwfrate = np.zeros(50)
	dirpath = "../ensbis_50fwfnb200yr"
	ensname = "ens_fwfnb200yr"
	year = 44910
	runstep = 50
	fwf_file(n,fwfinit1,fwfinit2,fwfrate,dirpath,ensname,year,runstep)
