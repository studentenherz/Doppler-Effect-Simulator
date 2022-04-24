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

		self._reception_t, self._wave = self._calculate(self._receptor)

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
		self._ax2.set_xlim([0, 6])
		# self._ax2.yaxis.tick_right()
		# self._ax2.yaxis.set_label_position('right')
 
		self._t = []
		self._distance = []
		self._distance_line, = self._ax2.plot([], [])

		# Lower right panel, sound wave
		self._ax3 = plt.subplot(224)
		self._ax3.set_xlabel('time (s)')    
		self._ax3.get_yaxis().set_visible(False)

		self._wave_line, = self._ax3.plot(self._reception_t, self._wave)

		interval = 20 # in ms
		self._time = 0
		self._phase = 0

		def update_lines(i):
			self._time += interval / 1000
			x0, y0 = self._receptor
			x1, y1 = self._source(self._phase + self._time)

			self._t.append(self._time)
			self._distance.append(np.sqrt((x1 - x0)**2 + (y1 - y0)**2))
			self._distance_line.set_data(self._t, self._distance)

			if self._t[-1] > self._ax2.get_xlim()[1]:
				self._t = self._t[1:]
				self._distance = self._distance[1:]
				self._ax2.set_xlim([self._t[0], self._t[-1]])

			self._ax2.relim()
			self._ax2.autoscale_view()

			self._source_line.set_data(*self._source(self._phase + self._time))

			return [self._source_line, self._receptor_line, self._distance_line]

		self._anim = 	FuncAnimation(self._fig, update_lines, interval=interval, blit = True)
		self._playing = True

		def toggle():
			if self._playing:
				self._anim.pause()
				self._playing = False
			else:
				self._anim.resume()
				self._playing = True
				self._mouse_scrolling = False
				self._source_line.set(alpha=1)

		def start():
			# self._t = []
			# self._distance = []
			self._reception_t, self._wave = self._calculate(self._receptor)
			self._distance_line.set_data(self._t, self._distance)
			self._wave_line.set_data(self._reception_t, self._wave)
			self._ax2.relim()
			self._ax2.autoscale_view()
			plt.draw()
			self._anim.resume()
			self._playing = True
			self._mouse_scrolling = False
			self._source_line.set(alpha=1)

		def onclick(event):
			if event.button == 1:
				self._anim.pause()
				self._playing = False

				self._receptor = (event.xdata, event.ydata)
				self._receptor_line.set_data(*self._receptor)
				
				self._mouse_scrolling = False
				self._source_line.set(alpha=1)
				plt.draw()

				if event.dblclick:
					start()
			elif event.button == 2:
				start()
			elif event.button == 3:
				toggle()

		self._mouse_scrolling = False
		def onscroll(event):
			if not self._mouse_scrolling:
				self._cached_bg = self._fig.canvas.copy_from_bbox(self._fig.bbox)
				self._source_line.set(alpha=0.5)
				self._mouse_scrolling = True

			self._anim.pause()
			self._playing = False

			self._fig.canvas.restore_region(self._cached_bg)
			self._phase += event.step * interval / 1000

			self._source_line.set_data(*self._source(self._phase + self._time))
			self._ax1.draw_artist(self._source_line)
			self._fig.canvas.blit(self._fig.bbox)
			self._fig.canvas.flush_events()

		def onkeypress(event):
			# Toggle play/pause with spacebar
			if event.key == ' ':
				toggle()
			# Hit Enter to play the sound from current position
			if event.key == 'enter':
				start()
		
		
		self._fig.canvas.mpl_connect('button_press_event', onclick)
		self._fig.canvas.mpl_connect('scroll_event', onscroll)
		self._fig.canvas.mpl_connect('key_press_event', onkeypress)

	def show(self):
		plt.show()