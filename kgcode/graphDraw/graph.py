#
# graph module
#
# (!) only undirected
#
# contains graph component classes
#

try:
	from pygame.draw import circle
	from pygame.draw import line
	from pygame import font

	import Config as Config
except ImportError:
	print 'graph -- (!) module do not found '	
	exit()


#################################################################################

class Vertex:

	def __init__(self, label, weight, (x,y)=(0,0), color=Config.vertex_color, width=Config.vertex_width):

		self.x = x
		self.y = y
		self.label = label
		self.weight = weight
		self.color = color
		self.width = width

		self.disp = [0.0, 0.0]		
		self.display_weight = Config.vertex_min_radius

		font.init()


	def display(self, surface):

		myfont = font.Font(None, 2*self.display_weight)
		label = myfont.render(self.label, 1, Config.vertex_label_color)

		d_pos = ( int(self.x) + (Config.frameWidth/2), int(self.y) + (Config.frameHeight/2) )
		circle(surface, self.color, d_pos, self.display_weight, self.width)

		surface.blit(label, (d_pos[0]+self.display_weight+5,d_pos[1]))



#################################################################################

class Edge:

	def __init__(self, v, u, color=Config.edge_color, width=Config.edge_width):

		if v < u:
			self.v = v
			self.u = u
		else:
			self.v = u
			self.u = v

		self.id = (self.v.label, self.u.label)

		self.color = color
		self.width = width


	def display(self, surface):

		line(surface, self.color, (int(self.v.x)+(Config.frameWidth/2), int(self.v.y)+(Config.frameHeight/2)), (int(self.u.x)+(Config.frameWidth/2), int(self.u.y)+(Config.frameHeight/2)), self.width)


##################################################################################


class Graph:

	def __init__(self, vertex_list=[], edge_list=[]):

		self.vertex_index = {}
		self.adj_list = {}

		for vertex in vertex_list:
			self.add_vertex( vertex.label, vertex.weight )

		for edge in edge_list:
			self.add_edge( edge.v.label, edge.u.label )		


	def add_vertex(self, label, weight):
		if label not in self.vertex_index:
			vertex = Vertex(label, weight)
			self.vertex_index[vertex.label] = vertex
			self.adj_list[vertex.label] = []
		else:
			print 'graph -- this vertex already exists in this graph'


	def add_edge(self, label_v, label_u):
	
		if (label_v in self.adj_list) and (label_u in self.adj_list):

			if label_u not in self.adj_list[label_v]:
				self.adj_list[label_v].append( label_u )

			if label_v not in self.adj_list[label_u]:
				self.adj_list[label_u].append( label_v )
		else:
			print 'graph -- a vertex or the vertices of this edge do not exist in graph'


	def vertices(self):
		return self.vertex_index.values()

	
	def edges(self):
		
		edges = {}

		for vertex in self.vertices():
			for neighbour in self.neighbours(vertex):
				edge = Edge(vertex, neighbour)

				if edge.id not in edges:
					edges[edge.id] = edge

		return edges.values()


	def neighbours(self, vertex):
		return [ self.vertex_index[label] for label in self.adj_list[vertex.label] ]


	def display(self, surface):

		for e in self.edges():
			e.display(surface)

		for v in self.vertices():
			v.display(surface)


	def normalize_view(self):	
		
		weights = [v.weight for v in self.vertices()]

		weight_min = min(weights)
		weight_max = max(weights)

		if (weight_min - weight_max) == 0:
			return

		for v in self.vertices():
			v.display_weight = self.__min_max_normalization(v.weight, weight_min, weight_max, Config.vertex_min_radius, Config.vertex_max_radius)


	def __min_max_normalization(self, x, x_min, x_max, pref_min, pref_max):

		norm_x = ( (x - x_min) / float(x_max - x_min) ) * ( pref_max - pref_min ) + pref_min

		return int(norm_x)




