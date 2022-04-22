from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class GUI:
	'''
		A class to encapsulate the visual elements in the interactive mode
	of the program.
	'''

	def __init__(self,
			source : callable([[float], tuple[float, float]]),
			period : float,
			calculate : callable([[tuple[float, float]], tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]]),
			receptor : tuple[float, float] = (0., 0.),
		) -> 'GUI':

		self._fig = plt.figure(figsize=[16.34,  7.53]) 
		# figsize is a quick'n'dirty way of getting the left panel to be squared 
		# and same height as the two panels to the right stacked. This obviously 
		# breaks when the user resizes the window, and since the window itself 
		# is backend specific I won't force fixed size.

		self._source = source
		self._calculate = calculate
		self._receptor = receptor

		(self._t, self._distance), (self._reception_t, self._wave) = self._calculate(self._receptor)

		# Left panel, animation of the experiment
		self._ax1 = plt.subplot(121)
		self._ax1.set_aspect('equal')
		self._ax1.axis('off')

		# Circular rail, for other functions would be hard to know
		# what the shape will be, maybe if I finally generalyse this
		# I'll just make it have a "ghost tail" and/or a "tail ahead"
		t = np.linspace(0, period, 100)
		vec_source = np.vectorize(source)
		s = vec_source(t)
		self._ax1.plot(s[0], s[1], '--')

		# Source marker
		sx0, sy0 = self._source(0)
		self._source_line, = self._ax1.plot(sx0, sy0, 'o')

		self._receptor_line, = self._ax1.plot(receptor[0], receptor[1], 'og')

		# Upper right panel, distance
		self._ax2 = plt.subplot(222)
		self._ax2.set_xlabel('time (s)')
		self._ax2.xaxis.tick_top()
		self._ax2.xaxis.set_label_position('top')
		self._ax2.set_ylabel('distance (m)')
		self._ax2.yaxis.tick_right()
		self._ax2.yaxis.set_label_position('right')
 
		self._distance_line, = self._ax2.plot(self._t, self._distance)

		# Lower right panel, sound wave
		self._ax3 = plt.subplot(224)
		self._ax3.set_xlabel('time (s)')    
		self._ax3.get_yaxis().set_visible(False)

		self._wave_line, = self._ax3.plot(self._reception_t, self._wave)

		interval = 20 # in ms

		def update_lines(i):
			self._source_line.set_data(*self._source(i * interval / 1000))
			return [self._source_line, self._receptor_line]

		self._anim = 	FuncAnimation(self._fig, update_lines, interval=interval, blit = True)

		def onclick(event):
			self._receptor = (event.xdata, event.ydata)
			self._receptor_line.set_data(*self._receptor)
			(self._t, self._distance), (self._reception_t, self._wave) = self._calculate(self._receptor)
			self._distance_line.set_data(self._t, self._distance)
			self._wave_line.set_data(self._reception_t, self._wave)
			plt.draw()
		
		self._fig.canvas.mpl_connect('button_press_event', onclick)

	def show(self):
		plt.show()