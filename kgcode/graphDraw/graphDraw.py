#
#	graphDraw module
#
#	 
#	draws the graph defined by the nodes in vertex_list and the edges in edge_list	
#


try:
	from PygameFrame import PygameFrame
except ImportError:
	print 'graphDraw -- (!) module do not found '	
	exit()


def draw(graph):

	pygameFrame = PygameFrame(graph)

	pygameFrame.loop()
