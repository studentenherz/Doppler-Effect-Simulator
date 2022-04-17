from doppler import doppler
from util import convert_to_float32
from scipy.io.wavfile import read, write
import argparse

VERSION = 1.0

def main():
	parser = argparse.ArgumentParser(description='Simulates the sound from a source moving in a circle taking Doppler effect into account.')
	parser.add_argument('-V', '--version', action='version', version='%(prog)s version {}'.format(VERSION))

	parser.add_argument('-R', '--radius', action='store', dest='R', default=100, help='Radius of source\'s trajectory in meters (default = 100)')
	parser.add_argument('-v', '--velocity', action='store', dest='v', default=30, help='Speed of the source in peters per second (default = 30)')
	parser.add_argument('--x0', action='store', dest='x0', default=0, help='Initial x position of receptor in meters (default = 0)')
	parser.add_argument('--y0', action='store', dest='y0', default=0, help='Initial y position of receptor in meters (default = 0)')
	parser.add_argument_group()

	parser.add_argument('fin', type=str, help='Input audio file in WAV format')

	args = parser.parse_args()

	if not args.fin:
		parser.error('Input file is mandatory')
	samplerate, data = read(args.fin)
	N_channels = 1 if len(data.shape) == 1 else data.shape[1]

	if N_channels > 1:
		data = data[:,0]

	data = convert_to_float32(data)

	new_interp = doppler(data, samplerate, lambda t : (100 - 30 * t, 10))
	write('doppler.wav', samplerate, new_interp)

if __name__ == '__main__':
	main()