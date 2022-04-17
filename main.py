from doppler import doppler
from util import convert_to_float32
from scipy.io.wavfile import read, write

samplerate, data = read('test/data_train-whistle.wav')
N_samples = data.shape[0]
N_channels = 1 if len(data.shape) == 1 else data.shape[1]

if N_channels > 1:
	data = data[:,0]

data = convert_to_float32(data)

new_interp = doppler(data, samplerate, lambda t : (100 - 30 * t, 10))
write('doppler.wav', samplerate, new_interp)
