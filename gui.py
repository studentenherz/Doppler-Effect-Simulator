from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime

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
		self._period = period
		self._calculate = calculate
		self._receptor = receptor

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
		self._source_line, = self._ax1.plot(sx0, sy0, 'o', animated=True)

		self._receptor_line, = self._ax1.plot(receptor[0], receptor[1], 'og')

		# Upper right panel, distance
		self._ax2 = plt.subplot(222)
		self._ax2.set_xlabel('time (s)')
		self._ax2.xaxis.tick_top()
		self._ax2.xaxis.set_label_position('top')
		self._ax2.set_ylabel('distance (m)')
		self._ax2.set_xlim([0, self._period])

 
		self._t = []
		self._distance = []
		self._distance_line, = self._ax2.plot([], [])

		# Lower right panel, sound wave
		self._ax3 = plt.subplot(224)
		self._ax3.set_xlabel('time (s)')    
		self._ax3.set_ylabel('amplitude (relative units)')
		self._ax3.set_ylim([-1, 1])

		self._wave_line, = self._ax3.plot([], [])

		self._interval = 20 # in ms
		self._time = 0
		self._t0_datetime = datetime.now()
		self._phase = 0

		def d(t):
			x0, y0 = self._receptor
			x1, y1 = self._source(self._phase + t)

			return np.sqrt((x1 - x0)**2 + (y1 - y0)**2)

		def resume():
			self._t0_datetime = datetime.now()
			self._anim.resume()
			self._playing = True
			self._mouse_scrolling = False
			self._source_line.set(alpha=1)

		def pause():
			self._phase += self._time
			self._anim.pause()
			self._playing = False

		def start():
			self._t = np.arange(0, self._period, self._interval	/ 1000)
			self._distance = [d(t) for t in self._t]
			self._distance_line.set_data(self._t, self._distance)
			self._ax2.set_ylim([np.min(self._distance), np.max(self._distance)])

			reception_t, wave = self._calculate(self._receptor, self._phase)
			self._wave_line.set_data(reception_t, wave)
			self._ax3.set_xlim([np.min(reception_t), np.max(reception_t)])

			self._fig.canvas.draw()
			resume()
			

		def update_lines(i):
			self._time = (datetime.now() - self._t0_datetime).total_seconds()
			
			# self._distance_line.set_data(self._t, self._distance)

			self._source_line.set_data(*self._source(self._phase + self._time))
			return [self._source_line, self._receptor_line]


		self._anim = 	FuncAnimation(self._fig, update_lines, interval=self._interval, blit = True)
		self._playing = True

		def toggle():
			if self._playing:
				pause()
			else:
				resume()

		def onclick(event):
			if event.button == 1:
				if event.inaxes == self._ax1:
					pause()

					self._receptor = (event.xdata, event.ydata)
					self._receptor_line.set_data(*self._receptor)
					
					self._mouse_scrolling = False
					self._source_line.set(alpha=1)
					plt.draw()

					if event.dblclick:
						start()
			elif event.button == 2:
				if self._playing:
					pause()
				start()
			elif event.button == 3:
				toggle()

		self._mouse_scrolling = False
		def onscroll(event):
			if not self._mouse_scrolling:
				if self._playing:
					pause()
				self._cached_bg = self._fig.canvas.copy_from_bbox(self._fig.bbox)
				self._source_line.set(alpha=0.5)
				self._mouse_scrolling = True


			self._fig.canvas.restore_region(self._cached_bg)
			self._phase += event.step * self._interval / 1000

			self._source_line.set_data(*self._source(self._phase))
			self._ax1.draw_artist(self._source_line)
			self._fig.canvas.blit(self._fig.bbox)
			self._fig.canvas.flush_events()

		def onkeypress(event):
			# Toggle play/pause with spacebar
			if event.key == ' ':
				toggle()
			# Hit Enter to play the sound from current position
			if event.key == 'enter':
				if self._playing:
					pause()
				start()
		
		
		self._fig.canvas.mpl_connect('button_press_event', onclick)
		self._fig.canvas.mpl_connect('scroll_event', onscroll)
		self._fig.canvas.mpl_connect('key_press_event', onkeypress)

		start()

	def show(self):
		plt.show()