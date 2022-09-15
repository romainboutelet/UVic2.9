import numpy as np
import numpy.fft as fft
from scipy.special import gamma

def distrib(shape):
	return 1 * np.exp(1j * np.random.rand(*shape) * 2*np.pi)


def spectr(alpha,omega,mu):
	def Pk(k):
		#return omega*alpha/((omega**2+k**2)**(mu+0.5))
		return 4*np.pi*gamma(3/2)/(gamma(1/2)*1/omega)*(omega**2 + 4*np.pi**2*k**2)**-(1)
	return Pk

def gauss_field(shape,alpha,omega,mu,unit_length):
	
	# Compute the k grid
	all_k = [fft.fftfreq(s, d=unit_length) for s in shape[:-1]] + \
	[fft.rfftfreq(shape[-1], d=unit_length)]

	kgrid = np.meshgrid(*all_k, indexing='ij')
	knorm = np.sqrt(np.sum(np.power(kgrid, 2), axis=0))
	
	fftfield = distrib(knorm.shape)
	
	spectr_k = np.where(omega**2 + knorm**2 == 0 , 0 , spectr(alpha,omega,mu)(knorm))

	fftfield *= spectr_k

	return fft.irfftn(fftfield)
	

if __name__ == '__main__':
		
	import matplotlib.pyplot as plt
	shape=(502,502)
	alpha=1
	omega=0.01
	mu=0.5
	field = gauss_field(shape,alpha,omega,mu,1)
	print(field,np.sqrt(np.mean(field**2)))
	plt.imshow(field,cmap='seismic')
	plt.show()

