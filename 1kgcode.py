
try:	
	from kgcode.Collection import Collection
	from kgcode.graphDraw.graph import Graph
	from kgcode.graphDraw import graphDraw

except ImportError:
	print '1kgcode -- (!) module do not found '	
	exit()



# set the json input file
input_file = 'input.json'



def main():

	collection = Collection(input_file)
	collection.read()

	skills = collection.skills()
	conjunctions = collection.conjunctions()


	graph = Graph()

	for skill in skills:
		graph.add_vertex( skill, skills[skill])

	for skill in conjunctions:
		for conjunction in conjunctions[skill]: 
			graph.add_edge( skill, conjunction )

	graphDraw.draw(graph)



if __name__ == "__main__":

	main()


