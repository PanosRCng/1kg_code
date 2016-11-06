#
#
#	Python implementation of the Force-directed Placement algorithm 
#
#	as described in Graph Drawing by Force-directed Placement
#	(http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.13.8444&rep=rep1&type=pdf)
#
#		
#


try:
	from random import randint
	from math import sqrt
	from math import log

	import Config as Config
except ImportError:
	print 'ForceDirected -- (!) module do not found '	
	exit()


class ForceDirected:

	# constructor
	def __init__(self, G, W=Config.frameWidth, L=Config.frameHeight):

		self.W = W
		self.L = L
		self.G = G

		area = self.W * self.L
		self.k = sqrt( area/len(self.G.vertices()) ) / 2

		self.__initRandomPos()

		self.x = 100
		self.__cool()

		self.iteration_counter = 0


	def iteration(self):
	
		if self.iteration_counter >= Config.iterations:
			return

		self.__calc_repulsive_forces()
		self.__calc_attractive_forces()
		self.__displacement_check()
		self.__cool()

		self.iteration_counter += 1


	# calculate repulsive forces
	def __calc_repulsive_forces(self):

		for v in self.G.vertices():
			v.disp = [0.0, 0.0]
			for u in self.G.vertices():
				if v != u:
					D = self.__diff_vector(v, u)
					Dr = self.__dir_vector(D)
					fr = self.__fr(D)

					v.disp[0] += Dr[0] * fr
					v.disp[1] += Dr[1] * fr


	# calculate attractive forces
	def __calc_attractive_forces(self):

		for e in self.G.edges():
			D = self.__diff_vector(e.v, e.u)
			Dr = self.__dir_vector(D)
			fa = self.__fa(D)

			e.v.disp[0] -= Dr[0] * fa
			e.u.disp[0] += Dr[0] * fa

			e.v.disp[1] -= Dr[1] * fa
			e.u.disp[1] += Dr[1] * fa


	# limit the maximum displacement to the temperature
	# prevent from being displaced outside the frame
	def __displacement_check(self):

		for v in self.G.vertices():
			Dr = self.__dir_vector(v.disp)

			v.x += Dr[0] * min(abs(v.disp[0]), self.t)
			v.y += Dr[1] * min(abs(v.disp[1]), self.t)
		
			v.x = min( (self.W/2)-Config.offset, max(-(self.W/2)+Config.offset, v.x) )
			v.y = min( (self.L/2)-Config.offset, max(-(self.L/2)+Config.offset, v.y) )


	# the vertices are assigned random initial positions
	def __initRandomPos(self):

		for v in self.G.vertices():
			v.x = randint(-(self.W/2)+Config.offset,(self.W/2)-Config.offset)
			v.y = randint(-(self.L/2)+Config.offset,(self.L/2)-Config.offset)


	# attractive force
	def __fa(self, X):
		eu_d = self.__euclid_dist(X[0], X[1])
		if eu_d != 0:
			return (eu_d*eu_d)/self.k
		return 0


	# repulsive force
	def __fr(self, X):
		eu_d = self.__euclid_dist(X[0], X[1])
		if eu_d != 0:
			return ( ((self.k*self.k)/eu_d) )#* (self.__ux((2*self.k)-eu_d)) )
		return 0


	# the u function
	def __ux(self, x):
		return 1 if (x > 0) else 0


	# cooling schedule - reduces the temperature as the layout approaches a better configuration
	def __cool(self):
		self.x -= 1
		if self.x >= 2:
			self.t = log(self.x,10)


	# calculates the difference vector between the positions of the two vertices
	def __diff_vector(self, v, u):
		return [(v.x-u.x), (v.y-u.y)]


	# calculates the direction vector
	def __dir_vector(self, X):
		Y = [0.0, 0.0]

		if X[0] != 0:
			Y[0] = ( X[0]/abs(X[0]) )

		if X[1] != 0:
			Y[1] = ( X[1]/abs(X[1]) )

		return Y


	# calculates the euclidean distance
	def __euclid_dist(self, dx, dy):
		return sqrt( pow(dx,2) + pow(dy,2) )


