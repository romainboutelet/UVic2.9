#! /home/romainboutelet/miniconda3/bin/python

import os
import numpy as np

def write_control(n,dirpath,ensname,runstep,tsiint,tavgint,tavgper):
	for i in range(n):
		cont=open(dirpath + '/' + ensname + str(i) +'/control.in','r')
		contnew=open(dirpath + '/' + ensname + str(i) +'/controlbis.in','w')

		line1 = " &contrl init=.false., runlen=" + str(runstep*365) + "., rununits='days',\n"
		line2 = " &diagn  tsiint=" + str(tsiint) + "., tsiper=" + str(tsiint) + ".,\n"
		line3 = "         timavgint=" + str(tavgint*365) + "., timavgper=" + str(tavgper) + ".,\n"

		for line in cont:
			if '&contrl' in line:
				contnew.write(line1)
			elif '&diagn' in line:
				contnew.write(line2)
			elif 'timavgint' in line:
				contnew.write(line3)
			else:
				contnew.write(line)

		cont.close()
		contnew.close()
		os.system('mv ' + dirpath + '/' + ensname + str(i) + '/controlbis.in ' + dirpath + '/' + ensname + str(i) +'/control.in')

	return

def write_runobs_control(dirpath,ensname,runstep,tsiint,tavgint,tavgper):

	cont=open(dirpath + '/' + ensname  +'/control.in','r')
	contnew=open(dirpath + '/' + ensname +'/controlbis.in','w')

	line1 = " &contrl init=.false., runlen=" + str(runstep*365) + "., rununits='days',\n"
	line2 = " &diagn  tsiint=" + str(tsiint) + "., tsiper=" + str(tsiint) + ".,\n"
	line3 = "         timavgint=" + str(tavgint*365) + "., timavgper=" + str(tavgper) + ".,\n"

	for line in cont:
		if '&contrl' in line:
			contnew.write(line1)
		elif '&diagn' in line:
			contnew.write(line2)
		elif 'timavgint' in line:
			contnew.write(line3)
		else:
			contnew.write(line)

	cont.close()
	contnew.close()
	os.system('mv ' + dirpath + '/' + ensname + '/controlbis.in ' + dirpath + '/' + ensname +'/control.in')

	return
