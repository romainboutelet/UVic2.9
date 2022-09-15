#! /home/romainboutelet/miniconda3/bin/python


def string_yr(i):
	if i < 10:	
		yr = '0000' + str(i)
	elif i < 100:
		yr = '000' + str(i)
	elif i < 1000:
		yr = '00' + str(i)
	elif i < 10000:
		yr = '0' + str(i)
	else:
		yr=str(i)
	return yr
	
if __name__ == '__main__':
	print(string_yr(4050))
