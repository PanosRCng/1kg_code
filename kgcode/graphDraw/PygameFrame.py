#
#
#	PyGame class
#
#
#	initializes and handles a pygame window
#
#
#	runs the graph placement algorithm
#	displays the graph placement at the end of each iteration
#
#



try:
	import pygame
	from sys import exit
	from pygame.locals import *

	import Config as Config
	from ForceDirected import ForceDirected

except ImportError:
	print 'PygameFrame -- (!) module do not found '	
	exit()


class PygameFrame:

	def __init__(self, graph, frameWidth=Config.frameWidth, frameHeight=Config.frameHeight):

		self.graph = graph
		self.frameWidth = frameWidth
		self.frameHeight = frameHeight

		self.__init()



	def __init(self):

		pygame.init()
		self.screen = pygame.display.set_mode((self.frameWidth, self.frameHeight))
		pygame.display.set_caption(Config.frameName)
		self.screen.fill(Config.background_color)


	def loop(self):

		self.forceDirected = ForceDirected(self.graph)

		self.graph.normalize_view()

		while True:

			self.__handleEvent()

			self.forceDirected.iteration()

			self.__display()


	def __display(self):

		self.screen.fill(Config.background_color)

		# display graph
		self.forceDirected.G.display(self.screen)

		pygame.display.update()


	# handle input events
	def __handleEvent(self):

		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit()
				exit()
				return

			if event.type == KEYDOWN:
				key = pygame.key.get_pressed()

				# quit if escape is pressed
				if key[K_ESCAPE]:
					pygame.quit()
					exit()
					return


