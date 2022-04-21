import numpy as np
import argparse
from scipy.io.wavfile import write

from util import digest_audio
from doppler import doppler
from gui import GUI

VERSION = 1.0

def main():
	parser = argparse.ArgumentParser(description='Simulates the sound from a source moving in a circle taking Doppler effect into account.')

	parser.add_argument('-a', '--input', dest='fin', type=str, help='Input audio file in WAV format')
	parser.add_argument('-R', '--radius', action='store', dest='R', type=float, default=100, help='Radius of source\'s trajectory in meters (default = 100)')
	parser.add_argument('-v', '--velocity', action='store', dest='v', type=float, default=30, help='Speed of the source in peters per second (default = 30)')
	parser.add_argument('--x0', action='store', dest='x0', type=float, default=0, help='Initial x position of receptor in meters (default = 0)')
	parser.add_argument('--y0', action='store', dest='y0', type=float, default=0, help='Initial y position of receptor in meters (default = 0)')
	parser.add_argument('-o', '--output', action='store', dest='fout', type=str, default='doppler.wav', help='Output file')
	parser.add_argument('-i', '--interactive', action='store_true', dest='interactive', default=False, help='Interactive mode')

	parser.add_argument('-V', '--version', action='version', version='%(prog)s version {}'.format(VERSION))

	args = parser.parse_args()

	if not args.fin:
		parser.error('Input file is mandatory')

	receptor = (args.x0, args.y0)

	samplerate, data = digest_audio(args.fin)

	omega = args.v / args.R
	circle = lambda t : (args.R * np.cos(omega * t), args.R * np.sin(omega * t))

	def calculate(receptor = (0., 0.)):
		return doppler(data, samplerate, circle, receptor)

	if args.interactive:
		gui = GUI(circle, 2 * np.pi / omega, calculate, receptor)
		gui.show()
	else:
		_, (_, new_wave) = calculate(receptor)
		write(args.fout, samplerate, new_wave)

if __name__ == '__main__':
	main()