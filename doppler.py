import numpy as np
from scipy.interpolate import interp1d

def doppler(
		data : np.ndarray,
		samplerate : int,
		source : callable([[float], tuple[float, float]]),
		receptor : tuple[float, float] = (0., 0.),
		c : float = 300,
		invsqr : bool = True
	) -> tuple[np.ndarray, np.ndarray]:
	'''
		Transforms data representing a sound into what will be heard from coming from the source in the receptor.

		Parameters
		----------
		data : np.ndarray
			Sound data in a numpy array of np.float(32 or more)
		samplerate: int
			Sample rate of the sound
		source: callable
			A callable that returns the position (x, y) of the source when evaluated on the time t. (x, y) in meters and t in seconds.
		x0 : float
			x position of receptor
		y0 : float
			y position of receptor
		c : float
			Speed of the sound on the medium
		invsqrt: bool
			True if the sound should take into account the inverse square relation between sound intensity and distance (because of energy conservation)

		Returns
		-------
		newdata: np.ndarray
			Sound data after Doppler effect is applied
	'''
	
	N_samples = len(data)
	t = np.arange(0, N_samples) / samplerate

	def distance(t):
		x0, y0 = receptor
		x1, y1 = source(t)

		return np.sqrt((x1 - x0)**2 + (y1 - y0)**2)

	vec_distance = np.vectorize(distance)
	
	d = vec_distance(t)

	# rec_t are the times in which every sample reach the receptor
	rec_t = t + d / c

	# data with inverse sqr the original intensity corresponds to the
	# closest point
	if invsqr:
		data = data * np.min(d) / d

	# calculate interpolation
	f = interp1d(rec_t, data, kind='cubic')

	t0 = np.min(rec_t)
	t1 = np.max(rec_t)
	rec_t_fixed_rate = np.linspace(t0, t1, int((t1 - t0) * samplerate))

	# interpolate data to fixed rate samples
	newdata = f(rec_t_fixed_rate)

	return rec_t_fixed_rate, newdata