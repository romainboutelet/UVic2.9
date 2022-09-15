#! /home/romainboutelet/miniconda3/bin/python

import os

def run_done(dirpath,ensname,j):

	with open(dirpath + '/' + ensname + str(j) + '/pr', 'r') as f:
		lines = f.read().splitlines()
		last_line = lines[-1]
		done = '==>  UVIC_ESCM integration is complete.' in last_line
	return done




