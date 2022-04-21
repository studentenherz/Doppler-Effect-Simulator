import numpy as np
from scipy.io.wavfile import read

def convert_to_float32(a : np.ndarray) -> np.ndarray:
	'''
		Returns audio data in float32 numpy format.

		Parameters
		----------
		a : np.ndarray
			Sound data in single channel

		Returns
		-------
		a : np.ndarray
			Sound data in float32 numpy type (or higher amount of bits float)
	'''
	if a.dtype == np.int16:
		return a.astype(np.float32) / 32767
	if a.dtype == np.int32:
		return a.astype(np.float32) / 2147483647
	if a.dtype == np.int8:
		return -1 + 2 * a.astype(np.float32) / 256
	return a

def digest_audio(audio : str) -> tuple[int, np.ndarray]:
	'''
		Reads a sound file and gives the sound data after handeling 
		multichannel and converting to float data type

		Parameters
		----------
		audio : str
			File to be read

		Returns
		-------
		samplerate : int
			Samplerate of the read audio
		data : np.ndarray
			Sound data in float32 numpy type (or higher amount of bits float)
	'''
	samplerate, data = read(audio)

	N_channels = 1 if len(data.shape) == 1 else data.shape[1]
	if N_channels > 1:
		data = (convert_to_float32(data[:,0]) + convert_to_float32(data[:,1])) / 2
	else:
		data = convert_to_float32(data)

	return samplerate, data